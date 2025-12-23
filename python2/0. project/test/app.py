# -*- coding: utf-8 -*-
from __future__ import annotations
from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import joblib
from sqlalchemy import create_engine, text
from datetime import date
from config import (
    SQLALCHEMY_URL, MODEL_CLS_PATH, MODEL_REG_PATH, FEATS_PATH,
    DELAY_THRESHOLD_MIN
)
import logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# -----------------------------
# 자원 로딩
# -----------------------------
engine = create_engine(SQLALCHEMY_URL, pool_pre_ping=True)
clf_pipe = joblib.load(MODEL_CLS_PATH)
reg_pipe = joblib.load(MODEL_REG_PATH)
feats: list[str] = joblib.load(FEATS_PATH)

# -----------------------------
# 선택지 유틸
# -----------------------------
def get_lines() -> list[str]:
    with engine.connect() as conn:
        return pd.read_sql(
            "SELECT DISTINCT `호선` AS line FROM final_subway_delay ORDER BY 1", conn
        )["line"].tolist()

def get_directions_for_line(line: str) -> list[str]:
    with engine.connect() as conn:
        return pd.read_sql(
            text("SELECT DISTINCT `방향` AS dir FROM final_subway_delay WHERE `호선`=:line ORDER BY 1"),
            conn, params={"line": line}
        )["dir"].tolist()

def get_times() -> list[str]:
    with engine.connect() as conn:
        return pd.read_sql(
            "SELECT DISTINCT `시간` AS tm FROM final_subway_delay ORDER BY 1", conn
        )["tm"].tolist()
def _get(val, default=None):
    """빈 문자열/스페이스 → None으로 치환, 없으면 default."""
    if val is None: return default
    s = str(val).strip()
    return default if s == "" else s

def _nz(v, name="param"):
    """빈 문자열/None 방지: 없으면 명시적으로 에러."""
    if v is None:
        raise ValueError(f"{name} is None")
    s = str(v).strip()
    if not s:
        raise ValueError(f"{name} is empty")
    return s

# -----------------------------
# 미래 합성 피처 생성(이전 답변 버전 유지)
# -----------------------------
def _daytype(ts: pd.Timestamp) -> str:
    dow = ts.dayofweek
    return "토요일" if dow == 5 else ("일요일" if dow == 6 else "평일")

def _build_synthetic_row(line: str, direction: str, hhmm: str, target_date: str) -> pd.DataFrame:
    # --- 입력값 검증 (None/빈문자 방지) ---
    line       = _nz(line, "line")
    direction  = _nz(direction, "direction")
    hhmm       = _nz(hhmm, "hhmm")
    target_date= _nz(target_date, "target_date")

    tgt_ts = pd.to_datetime(target_date)
    ytype  = _daytype(tgt_ts)
    month  = int(tgt_ts.month)
    start_hist = (tgt_ts - pd.Timedelta(days=56)).date()
    end_hist   = (tgt_ts - pd.Timedelta(days=1)).date()

    # 문자열로 넘겨 드라이버 파싱 안정화
    s_str = start_hist.isoformat()
    e_str = end_hist.isoformat()

    with engine.connect() as conn:
        # 혼잡도 히스토리
        sql_cong = text("""
            SELECT `혼잡도(%)`
            FROM final_subway_delay
            WHERE `호선` = :line
              AND `방향` = :direction
              AND `시간` = :hhmm
              AND `요일구분` = :ytype
              AND `날짜` BETWEEN :s AND :e
        """)
        cong_hist = pd.read_sql(
            sql_cong, conn,
            params={"line": line, "direction": direction, "hhmm": hhmm,
                    "ytype": ytype, "s": s_str, "e": e_str}
        )

        # 날씨 히스토리
        sql_w = text("""
            SELECT `기온_평균(°C)`,`습도_평균(%)`,`풍속_평균(m/s)`,
                   `현지기압_평균(hPa)`,`해면기압_평균(hPa)`,`강수량_30분(mm)`
            FROM final_subway_delay
            WHERE MONTH(`날짜`) = :mm
              AND `시간` = :hhmm
              AND `날짜` BETWEEN :s AND :e
        """)
        w_hist = pd.read_sql(
            sql_w, conn,
            params={"mm": month, "hhmm": hhmm, "s": s_str, "e": e_str}
        )

    # 이하 통계 계산/피처 구성은 기존 그대로 …

    def safe_median(s, default): 
        s = pd.to_numeric(s, errors="coerce").dropna()
        return float(s.median()) if not s.empty else default
    def safe_mean(s, default):
        s = pd.to_numeric(s, errors="coerce").dropna()
        return float(s.mean()) if not s.empty else default

    cong_val = safe_mean(cong_hist["혼잡도(%)"], 100.0) if not cong_hist.empty else 100.0
    t_med  = safe_median(w_hist.get("기온_평균(°C)", pd.Series(dtype=float)), 20.0)
    h_med  = safe_median(w_hist.get("습도_평균(%)", pd.Series(dtype=float)), 60.0)
    w_med  = safe_median(w_hist.get("풍속_평균(m/s)", pd.Series(dtype=float)), 1.5)
    p_med  = safe_median(w_hist.get("현지기압_평균(hPa)", pd.Series(dtype=float)), 1008.0)
    sp_med = safe_median(w_hist.get("해면기압_평균(hPa)", pd.Series(dtype=float)), 1012.0)
    rain   = safe_mean(w_hist.get("강수량_30분(mm)", pd.Series(dtype=float)), 0.0)
    is_rain = 1 if rain > 0 else 0

    is_weekend = 1 if ytype in ("토요일","일요일") else 0
    yoil = ["월","화","수","목","금","토","일"][tgt_ts.dayofweek]

    row = {
        "호선": line, "방향": direction, "시간": hhmm,
        "요일": yoil, "요일구분": ytype, "is_weekend": is_weekend,
        "혼잡도(%)": cong_val,
        "기온_평균(°C)": t_med, "습도_평균(%)": h_med, "풍속_평균(m/s)": w_med,
        "현지기압_평균(hPa)": p_med, "해면기압_평균(hPa)": sp_med,
        "강수량_30분(mm)": rain, "우천여부": is_rain,
    }
    X = pd.DataFrame([{c: row.get(c, np.nan) for c in feats}])
    for c in X.columns:
        if X[c].dtype.kind in "biufc": X[c] = X[c].fillna(0)
    X.attrs["meta"] = {"날짜": target_date, "시간": hhmm, "synthetic": True}
    return X

def _df_to_feats(df: pd.DataFrame, synthetic: bool) -> pd.DataFrame:
    if df is None or df.empty: return df
    X = pd.DataFrame(columns=feats)
    for c in feats: X[c] = df[c] if c in df.columns else np.nan
    for c in X.columns:
        if X[c].dtype.kind in "biufc": X[c] = X[c].fillna(0)
    X.attrs["meta"] = {
        "날짜": str(df.iloc[0].get("날짜","")),
        "시간": str(df.iloc[0].get("시간","")),
        "synthetic": synthetic
    }
    return X

def fetch_feature_row(line: str, direction: str, hhmm: str, date_str: str | None) -> pd.DataFrame:
    # 1) 날짜 지정 시 정확 매칭
    if date_str:
        with engine.connect() as conn:
            df = pd.read_sql(text("""
                SELECT * FROM final_subway_delay
                WHERE `호선`=:line AND `방향`=:direction AND `시간`=:hhmm AND `날짜`=:date
                ORDER BY `datetime` DESC LIMIT 1
            """), conn, {"line":line,"direction":direction,"hhmm":hhmm,"date":date_str})
        if not df.empty:
            return _df_to_feats(df, synthetic=False)
        # 미래면 합성
        if pd.to_datetime(date_str).date() > date.today():
            return _build_synthetic_row(line, direction, hhmm, date_str)
    # 2) 최신 1건 fallback
    with engine.connect() as conn:
        df2 = pd.read_sql(text("""
            SELECT * FROM final_subway_delay
            WHERE `호선`=:line AND `방향`=:direction AND `시간`=:hhmm
            ORDER BY `날짜` DESC, `datetime` DESC LIMIT 1
        """), conn, {"line":line,"direction":direction,"hhmm":hhmm})
    return _df_to_feats(df2, synthetic=False)

def predict_once(line: str, direction: str, hhmm: str, date_str: str | None) -> dict:
    X = fetch_feature_row(line, direction, hhmm, date_str)
    if not isinstance(X, pd.DataFrame) or X.empty:
        return {"error": "해당 조건에 맞는 데이터가 없습니다. (날짜/시간/호선/방향을 확인하세요.)"}
    prob_delay = float(clf_pipe.predict_proba(X)[0, 1])
    delay_min  = float(reg_pipe.predict(X)[0])
    status = "지연" if delay_min >= DELAY_THRESHOLD_MIN else "지연 없음"
    meta = X.attrs.get("meta", {})
    return {
        "line": line, "direction": direction,
        "time": meta.get("시간") or hhmm,
        "date": meta.get("날짜") or date_str,
        "probability_delay": round(prob_delay, 3),
        "expected_delay_min": round(delay_min, 2),
        "final_status": status,
        "synthetic": bool(meta.get("synthetic", False)),
    }

# -----------------------------
# 라우트
# -----------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    lines = get_lines()
    selected_line = _get(request.form.get("line"), lines[0] if lines else None)

    # --- form 값 로그 (에러 재현시 확인용) ---
    logging.info("[FORM] line=%r, direction=%r, time=%r, date=%r",
                 request.form.get("line"), request.form.get("direction"),
                 request.form.get("time"), request.form.get("date"))

    # 라인 자체가 없다면 즉시 에러
    if not selected_line:
        return render_template(
            "index.html",
            lines=lines, directions=[], times=[],
            form_defaults={"line":"", "direction":"", "time":"", "date":""},
            result=None,
            error_msg="호선 목록을 불러오지 못했습니다. DB 또는 final_subway_delay를 확인하세요.",
            threshold=DELAY_THRESHOLD_MIN
        )

    directions = get_directions_for_line(selected_line)
    times = get_times()

    form_defaults = {
        "line": selected_line,
        "direction": _get(request.form.get("direction"), directions[0] if directions else None),
        "time": _get(request.form.get("time"), times[0] if times else None),
        "date": _get(request.form.get("date"), "")  # 화면 표시용
    }

    result = None
    error_msg = None
    if request.method == "POST":
        # 필수값 검증
        if not form_defaults["direction"]:
            error_msg = f"해당 호선({form_defaults['line']})의 방향 목록이 없습니다."
        elif not form_defaults["time"]:
            error_msg = "시간 목록이 없습니다."
        else:
            # 빈 날짜는 None으로
            date_arg = form_defaults["date"] or None
            out = predict_once(form_defaults["line"], form_defaults["direction"], form_defaults["time"], date_arg)
            if "error" in out: error_msg = out["error"]
            else: result = out

    return render_template(
        "index.html",
        lines=lines, directions=directions, times=times,
        form_defaults=form_defaults,
        result=result, error_msg=error_msg,
        threshold=DELAY_THRESHOLD_MIN
    )

def fetch_feature_row(line: str, direction: str, hhmm: str, date_str: str | None) -> pd.DataFrame:
    # --- 서버 단 필수값 방어 ---
    line = _get(line)
    direction = _get(direction)
    hhmm = _get(hhmm)
    date_str = _get(date_str)

    if not line:
        raise ValueError("요청값(line)이 비었습니다.")
    if not direction:
        raise ValueError("요청값(direction)이 비었습니다.")
    if not hhmm:
        raise ValueError("요청값(time)이 비었습니다.")

    # 1) 날짜 지정 시 정확 매칭
    if date_str:
        with engine.connect() as conn:
            df = pd.read_sql(text("""
                SELECT * FROM final_subway_delay
                WHERE `호선`=:line AND `방향`=:direction AND `시간`=:hhmm AND `날짜`=:date
                ORDER BY `datetime` DESC LIMIT 1
            """), conn, params={"line": line, "direction": direction, "hhmm": hhmm, "date": date_str})
        if not df.empty:
            return _df_to_feats(df, synthetic=False)

        # 미래면 합성
        tgt = pd.to_datetime(date_str).date()
        if tgt > date.today():
            return _build_synthetic_row(line, direction, hhmm, date_str)
        # 과거/오늘인데 없으면 최신 fallback

    # 2) 최신 1건 fallback
    with engine.connect() as conn:
        df2 = pd.read_sql(text("""
            SELECT * FROM final_subway_delay
            WHERE `호선`=:line AND `방향`=:direction AND `시간`=:hhmm
            ORDER BY `날짜` DESC, `datetime` DESC LIMIT 1
        """), conn, params={"line": line, "direction": direction, "hhmm": hhmm})
    return _df_to_feats(df2, synthetic=False)



# --- 의존형 드롭다운용 API ---
@app.route("/api/directions", methods=["GET"])
def api_directions():
    line = request.args.get("line")
    if not line:
        return jsonify({"error":"line 파라미터가 필요합니다."}), 400
    return jsonify({"directions": get_directions_for_line(line)})

# 기존 API (예측)
@app.route("/api/predict", methods=["POST"])
def api_predict():
    data = request.get_json(force=True)
    for k in ("line", "direction", "time"):
        if k not in data:
            return jsonify({"error": f"'{k}' 필드가 필요합니다."}), 400
    out = predict_once(data["line"], data["direction"], data["time"], data.get("date"))
    if "error" in out:
        return jsonify(out), 404
    return app.response_class(
        response=pd.Series(out).to_json(force_ascii=False),
        status=200, mimetype="application/json"
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
