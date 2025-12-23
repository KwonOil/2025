# -*- coding: utf-8 -*-
"""
지하철 지연 예측 - DB 입력 버전 (CSV 미사용)
------------------------------------------------
[목표]
- 원본 CSV를 쓰지 않고, 이미 DB에 적재된 3개 테이블(지연/혼잡도/날씨)을 읽어
  전처리 후 하나의 최종 테이블로 병합한다.
- 결과는 CSV로 저장하고, 같은 내용을 DB에도 업로드한다.

[실행 환경]
- VS Code 등 IDE에서 바로 실행 (argparse 미사용)
- pip install pandas sqlalchemy pymysql

[출력]
- ./out/final_subway_delay.csv (UTF-8-SIG)
- DB 테이블 final_subway_delay (기존 있으면 덮어쓰기)

[전처리 요약]
- 기간: 2025-09-11 ~ 2025-09-17 (포함)
- 지연(wide→long), 혼잡도(역→노선 평균), 날씨(분→30분 집계) 후 병합
"""

from __future__ import annotations
import os
from pathlib import Path
from typing import Optional, List, Tuple

import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine, text


# =========================================================
# 0) 설정 (여기만 프로젝트 환경에 맞게 바꾸면 됩니다)
# =========================================================
DB_HOST = os.getenv("DB_HOST", "192.168.0.115")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "1234")
DB_NAME = os.getenv("DB_NAME", "miniproject")
DB_PORT = int(os.getenv("DB_PORT", "3306"))

# 원본 테이블명 (DB에 실제로 존재하는 이름으로 맞춰주세요)
TBL_DELAY = "delay_subway3"                     # 지연 데이터
TBL_CONGESTION = "subway_congestion"            # 혼잡도 데이터 (CSV명과 다를 수 있음)
TBL_WEATHER = "seoul_weather_2025_09"           # 날씨 데이터 (분단위)

# 결과 테이블명
TBL_FINAL = "final_subway_delay"

# 기간(포함)
START_DATE = "2025-09-11"
END_DATE   = "2025-09-17"

# 출력 CSV 경로
OUT_DIR = Path("python2\mini_project3\csv")
OUT_CSV = OUT_DIR / "final_subway_delay.csv"


# =========================================================
# 1) DB 연결 유틸
# =========================================================
def get_engine() -> "sqlalchemy.engine.Engine":
    """
    SQLAlchemy 엔진 생성 (pool_pre_ping=True로 연결 검증).
    환경변수(DB_HOST 등)가 있으면 우선 사용.
    """
    db_url = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_engine(db_url, pool_pre_ping=True)
    return engine


def read_sql_dataframe(engine, sql: str, params: Optional[dict] = None) -> pd.DataFrame:
    """
    안전한 read_sql 래퍼. SELECT 쿼리와 바인딩 파라미터를 받아 DataFrame으로 반환.
    """
    with engine.connect() as conn:
        return pd.read_sql(text(sql), conn, params=params)


# =========================================================
# 2) 공통 헬퍼: 헤더/시간 표준화
# =========================================================
def _normalize_header(s: str) -> str:
    """BOM/공백 제거 등 헤더 정리"""
    return str(s).replace("\ufeff", "").strip()

def _standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """헤더 정리 + 자주 쓰는 대체명 통일(필요 시 추가)"""
    df = df.rename(columns={c: _normalize_header(c) for c in df.columns})
    alt_map = {
        # 날짜
        "일자": "날짜", "date": "날짜", "Date": "날짜", "DATE": "날짜",
        # 노선
        "호선": "호선", "노선": "호선", "line": "호선", "Line": "호선",
        # 방향
        "방향(상행/하행)": "방향", "direction": "방향", "Direction": "방향",
        # 일시
        "일시(분)": "일시",
    }
    for k, v in alt_map.items():
        if k in df.columns and v not in df.columns:
            df = df.rename(columns={k: v})
    return df

def _is_time_col(col: str) -> bool:
    """'HH:MM' 또는 'H시MM분' 같은 시간열 판별"""
    col = str(col)
    if ":" in col and len(col) in (4, 5):
        hh, mm = col.split(":")[:2]
        return hh.isdigit() and mm.isdigit()
    return ("시" in col and "분" in col
            and col.replace("시", "").replace("분", "").replace(" ", "").replace(":", "").isdigit())

def _to_hhmm(t: str) -> str:
    """'5시30분' → '05:30', '5:30' → '05:30'"""
    t = str(t).strip()
    if "시" in t and "분" in t:
        h = t.split("시")[0]
        m = t.split("시")[1].replace("분", "")
        return f"{int(h):02d}:{int(m):02d}"
    if ":" in t:
        h, m = t.split(":")[:2]
        return f"{h.zfill(2)}:{m.zfill(2)}"
    return t


# =========================================================
# 3) 전처리 함수들 (DB DataFrame 입력)
# =========================================================
def build_delay_table(df: pd.DataFrame, start: str, end: str) -> pd.DataFrame:
    """
    지연 원시 데이터를 long 포맷으로 정리하고 기간 필터/파생을 수행.
    - 입력 df는 DB에서 read_sql로 읽어온 DataFrame.
    - 예상 컬럼: '날짜', '호선'(또는 '노선'), '방향', 그리고 시간열(05:30, 06:00 ... 또는 5시30분 등)
    """
    df = _standardize_columns(df)

    # 필수 컬럼 체크
    missing = [c for c in ["날짜", "호선", "방향"] if c not in df.columns]
    if missing:
        raise ValueError(f"[지연 데이터] 필수 컬럼 누락: {missing} | 현재 컬럼 예시: {list(df.columns)[:10]}")

    # 시간열 탐지
    time_cols = [c for c in df.columns if _is_time_col(c)]
    if not time_cols:
        raise ValueError(f"[지연 데이터] 시간열 탐지 실패. (예: '05:30', '5시30분') | 현재 컬럼 예시: {list(df.columns)[:15]}")

    id_cols = [c for c in df.columns if c not in time_cols]

    # wide -> long
    long = df.melt(id_vars=id_cols, value_vars=time_cols, var_name="시간", value_name="지연값")
    long["시간"] = long["시간"].map(_to_hhmm)

    # 날짜/시간 정규화 및 기간 필터
    long["날짜"] = pd.to_datetime(long["날짜"], errors="coerce")
    s, e = pd.to_datetime(start), pd.to_datetime(end)
    long = long[(long["날짜"] >= s) & (long["날짜"] <= e)].copy()

    long["datetime"] = pd.to_datetime(long["날짜"].dt.strftime("%Y-%m-%d") + " " + long["시간"], errors="coerce")

    # 파생
    dow_map = {0: "월", 1: "화", 2: "수", 3: "목", 4: "금", 5: "토", 6: "일"}
    long["요일"] = long["datetime"].dt.dayofweek.map(dow_map)
    long["is_weekend"] = (long["datetime"].dt.dayofweek >= 5).astype(int)

    def daytype(d):
        return "토요일" if d == 5 else ("일요일" if d == 6 else "평일")
    long["요일구분"] = long["datetime"].dt.dayofweek.map(daytype)

    long["delay_min"] = pd.to_numeric(long["지연값"], errors="coerce").fillna(0.0)
    long["is_delay_1m"] = (long["delay_min"] >= 1).astype(int)
    long["is_delay_5m"] = (long["delay_min"] >= 5).astype(int)

    # 방향 → 상/하선 매핑
    def map_updown(x):
        x = str(x)
        if "상행" in x:
            return "상선"
        if "하행" in x:
            return "하선"
        return np.nan

    long["상하구분"] = long["방향"].map(map_updown)

    # (지연 df는 '노선'일 수도 있으므로 이미 _standardize_columns에서 '호선'으로 통일됨)
    return long


def build_congestion_table(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    혼잡도 원시 테이블을 long으로 변환하고 2가지 집계 반환
    - cong_agg:  호선+상하구분+요일구분+시간 기준 평균 혼잡도
    - cong_fallback: 호선+요일구분+시간 기준 평균 혼잡도(방향 미상 대비)
    예상 컬럼: '호선','상하구분','요일구분', 그리고 '5시30분','6시00분',...'00시30분' 등의 시간열
    """
    df = _standardize_columns(df)

    # 시간열 추출
    tcols = [c for c in df.columns if ("시" in c and "분" in c)]
    if not tcols:
        raise ValueError(f"[혼잡도 데이터] 시간열 탐지 실패. (예: '5시30분') | 현재 컬럼 예시: {list(df.columns)[:15]}")
    id_cols = [c for c in df.columns if c not in tcols]

    long = df.melt(id_vars=id_cols, value_vars=tcols, var_name="시간K", value_name="혼잡도(%)")

    def ktime_to_hhmm(s):
        h = s.split("시")[0]
        m = s.split("시")[1].replace("분", "")
        return f"{int(h):02d}:{int(m):02d}"

    long["시간"] = long["시간K"].map(ktime_to_hhmm)

    agg = (long.groupby(["호선", "상하구분", "요일구분", "시간"], dropna=False)["혼잡도(%)"]
           .mean().reset_index())

    fb = (long.groupby(["호선", "요일구분", "시간"], dropna=False)["혼잡도(%)"]
          .mean().reset_index()
          .rename(columns={"혼잡도(%)": "혼잡도_전체방향(%)"}))

    return agg, fb


def build_weather_table(df: pd.DataFrame, start: str, end: str) -> pd.DataFrame:
    """
    분단위 기상자료를 30분 슬롯으로 집계.
    예상 컬럼: '일시','기온(°C)','습도(%)','풍속(m/s)','현지기압(hPa)','해면기압(hPa)','누적강수량(mm)'
    """
    df = _standardize_columns(df)

    if "일시" not in df.columns:
        raise ValueError(f"[날씨 데이터] '일시' 컬럼 없음. 현재 컬럼: {list(df.columns)[:12]}")

    w = df.copy()
    w["일시"] = pd.to_datetime(w["일시"], errors="coerce")
    w = w.dropna(subset=["일시"])

    s, e = pd.to_datetime(start).date(), pd.to_datetime(end).date()
    w = w[(w["일시"].dt.date >= s) & (w["일시"].dt.date <= e)].copy()

    w["date"] = w["일시"].dt.date
    w = w.sort_values(["date", "일시"])

    # 누적강수 → 분당 차분
    if "누적강수량(mm)" in w.columns:
        w["누적강수량(mm)"] = pd.to_numeric(w["누적강수량(mm)"], errors="coerce").fillna(method="ffill")
        w["강수량_분당(mm)"] = w.groupby("date")["누적강수량(mm)"].diff().fillna(0.0)
        w.loc[w["강수량_분당(mm)"] < 0, "강수량_분당(mm)"] = 0.0
    else:
        w["강수량_분당(mm)"] = 0.0

    # 30분 슬롯 집계
    w["슬롯"] = w["일시"].dt.floor("30min")
    agg = (w.groupby("슬롯").agg({
        "기온(°C)": "mean",
        "습도(%)": "mean",
        "풍속(m/s)": "mean",
        "현지기압(hPa)": "mean",
        "해면기압(hPa)": "mean",
        "강수량_분당(mm)": "sum"
    }).reset_index())

    agg["날짜"] = agg["슬롯"].dt.date
    agg["시간"] = agg["슬롯"].dt.strftime("%H:%M")
    agg = agg.rename(columns={
        "기온(°C)": "기온_평균(°C)",
        "습도(%)": "습도_평균(%)",
        "풍속(m/s)": "풍속_평균(m/s)",
        "현지기압(hPa)": "현지기압_평균(hPa)",
        "해면기압(hPa)": "해면기압_평균(hPa)",
        "강수량_분당(mm)": "강수량_30분(mm)"
    })
    agg["우천여부"] = (agg["강수량_30분(mm)"] > 0).astype(int)
    return agg


# =========================================================
# 4) 메인 파이프라인: DB→전처리→병합→CSV+DB
# =========================================================
if __name__ == "__main__":
    # 4-1) DB 연결
    engine = get_engine()

    # 4-2) 원본 3테이블 로딩 (가능하면 WHERE로 기간을 미리 좁혀도 됨)
    # 지연/혼잡도는 기간 필터 없이 전부 읽어도 크지 않다면 OK
    # 날씨는 분단위라 크면 WHERE 일시 BETWEEN ... 로 제한 권장
    sql_delay = f"SELECT * FROM `{TBL_DELAY}`"
    delay_raw = read_sql_dataframe(engine, sql_delay)

    sql_cong = f"SELECT * FROM `{TBL_CONGESTION}`"
    cong_raw = read_sql_dataframe(engine, sql_cong)

    # 날씨는 기간 필터로 네트워크 비용 감소
    sql_weather = f"""
        SELECT *
        FROM `{TBL_WEATHER}`
        WHERE `일시` BETWEEN :start_ts AND :end_ts
        ORDER BY `일시`
    """
    weather_raw = read_sql_dataframe(
        engine,
        sql_weather,
        params={"start_ts": f"{START_DATE} 00:00:00", "end_ts": f"{END_DATE} 23:59:59"}
    )

    # 4-3) 전처리 (CSV 버전과 동일 로직을 DataFrame 입력으로 수행)
    delay = build_delay_table(delay_raw, START_DATE, END_DATE)
    cong_agg, cong_fb = build_congestion_table(cong_raw)
    w30 = build_weather_table(weather_raw, START_DATE, END_DATE)

    # 4-4) 병합
    merged = (delay
              .merge(cong_agg, on=["호선", "상하구분", "요일구분", "시간"], how="left")
              .merge(cong_fb, on=["호선", "요일구분", "시간"], how="left"))

    # 혼잡도 결측 시 방향무시 평균으로 보완
    merged["혼잡도(%)"] = merged["혼잡도(%)"].fillna(merged["혼잡도_전체방향(%)"])
    merged = merged.drop(columns=["혼잡도_전체방향(%)"])

    # 날씨 병합 (날짜+시간)
    merged["날짜_key"] = merged["datetime"].dt.date
    merged = merged.merge(w30.drop(columns=["슬롯"]),
                          left_on=["날짜_key", "시간"],
                          right_on=["날짜", "시간"], how="left")
    merged = merged.drop(columns=["날짜_key", "날짜_y"], errors="ignore").rename(columns={"날짜_x": "날짜"})

    # 4-5) 저장 (CSV + DB)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    merged.to_csv(OUT_CSV, index=False, encoding="utf-8-sig")
    print(f"[OK] CSV 저장 → {OUT_CSV} (rows={len(merged):,})")

    # DB 업로드 (덮어쓰기)
    merged.to_sql(name=TBL_FINAL, con=engine, if_exists="replace", index=False)
    print(f"[OK] DB 업로드 → {DB_NAME}.{TBL_FINAL} (replace)")