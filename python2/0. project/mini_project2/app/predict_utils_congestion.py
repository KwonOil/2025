# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from sqlalchemy import text

def _fetch_congestion(engine, table_name, day_type, line_name, station_no, updown, time_hhmm):
    """
    DB에서 해당 (요일구분, 호선, 역번호, 상하선구분)의 time_hhmm 열 값을 읽어 혼잡도(%) 반환.
    혼잡도 테이블은 wide 형식(각 시간대가 열)이라 SELECT 시 열명을 직접 참조합니다.
    """
    # SQL 인젝션 방지: 열명은 화이트리스트로 검증해야 하나, 여기서는 time_hhmm을 사전에 서버에서 allowed_hours로 제한하세요.
    q = text(f"""
        SELECT `{time_hhmm}` AS cong
        FROM {table_name}
        WHERE 요일구분=:day AND 호선=:line AND 역번호=:stno AND 상하선구분=:ud
        LIMIT 1
    """)
    row = engine.connect().execute(q, {"day":day_type, "line":line_name, "stno":int(station_no), "ud":updown}).fetchone()
    return float(row[0]) if row and row[0] is not None else None

def make_feature_row(labels_line, labels_dir, labels_time, labels_day, labels_ud,
                     line_name, direction, time_hhmm, day_type, station_no, updown, congestion_pct):
    # 문자열 라벨 → 정수 라벨
    def _safe_enc(le, val, field):
        classes = set(le.classes_.tolist())
        if val not in classes:
            raise ValueError(f"학습에 없던 {field}: {val}")
        return int(le.transform([val])[0])

    row = {
        "노선_label": _safe_enc(labels_line, line_name, "노선"),
        "방향_label": _safe_enc(labels_dir, direction, "방향"),
        "시간_label": _safe_enc(labels_time, time_hhmm, "시간"),
        "요일_label": _safe_enc(labels_day, day_type, "요일구분"),
        "상하_label": _safe_enc(labels_ud, updown, "상하선구분"),
        "역번호": int(station_no),
        "혼잡도(%)": float(congestion_pct)
    }
    return pd.DataFrame([row])

def predict_with_congestion(clf, reg_pos, labels_line, labels_dir, labels_time, labels_day, labels_ud,
                            engine, congestion_table,
                            station_no:int, time_hhmm:str, day_type:str,
                            updown:str, line_name:str, direction:str):
    """
    입력:
      - station_no(역번호), time_hhmm('07:30'), day_type('평일/토요일/일요일'),
        updown(상하선구분), line_name('1호선'), direction(지연용 방향라벨)
    동작:
      1) DB에서 해당 혼잡도(%) 조회
      2) 피처 구성 → 분류확률 p, 양성조건부 회귀 y_plus 예측
    출력: dict (확률%, 예측_최대지연분, 기대_지연분, 혼잡도)
    """
    cong = _fetch_congestion(engine, congestion_table, day_type, line_name, station_no, updown, time_hhmm)
    if cong is None:
        raise ValueError("혼잡도 데이터를 찾을 수 없습니다. 파라미터를 확인하세요.")

    X = make_feature_row(labels_line, labels_dir, labels_time, labels_day, labels_ud,
                         line_name, direction, time_hhmm, day_type, station_no, updown, cong)

    proba = clf.predict_proba(X)[:, 1]
    y_plus = np.expm1(reg_pos.predict(X))
    y_plus = np.clip(y_plus, 0, None)

    return {
        "노선": line_name,
        "역번호": int(station_no),
        "방향": direction,
        "상하선구분": updown,
        "시간": time_hhmm,
        "요일구분": day_type,
        "혼잡도(%)": round(float(cong), 2),
        "지연발생확률(%)": round(float(proba[0]*100), 2),
        "예측_최대지연분": round(float(y_plus[0]), 2),
        "기대_지연분": round(float(proba[0]*y_plus[0]), 2),
    }
