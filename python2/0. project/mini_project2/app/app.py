# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request, render_template
from pathlib import Path
import json, joblib
from sqlalchemy import create_engine

from predict_utils_congestion import predict_with_congestion

app = Flask(__name__)

# ----- 모델/인코더 로드 -----
MODEL_DIR = Path(__file__).resolve().parent.parent / "models"
clf         = joblib.load(MODEL_DIR / "clf_cong_rf.pkl")
reg_pos     = joblib.load(MODEL_DIR / "reg_pos_cong_rf.pkl")
labels_line = joblib.load(MODEL_DIR / "labels_line.pkl")
labels_dir  = joblib.load(MODEL_DIR / "labels_dir.pkl")
labels_time = joblib.load(MODEL_DIR / "labels_time.pkl")
labels_day  = joblib.load(MODEL_DIR / "labels_day.pkl")
labels_ud   = joblib.load(MODEL_DIR / "labels_ud.pkl")

# 지표/메타
try:
    with open(MODEL_DIR / "metrics_cong.json","r",encoding="utf-8") as f:
        metrics = json.load(f)
except FileNotFoundError:
    metrics = {}

with open(MODEL_DIR / "station_meta.json","r",encoding="utf-8") as f:
    ST_META = json.load(f)  # {역번호: {호선, 역명, 상하선:[...]}, ...}

with open(MODEL_DIR / "times.json","r",encoding="utf-8") as f:
    TIMES = json.load(f)
with open(MODEL_DIR / "days.json","r",encoding="utf-8") as f:
    DAYS = json.load(f)

# ----- DB -----
DB_URL = "mysql+pymysql://root:1234@192.168.0.115/miniproject"
engine = create_engine(DB_URL)
CONG_TABLE = "subway_congestion"

@app.get("/")
def index():
    return render_template("index.html")

@app.get("/api/init_congestion")
def api_init_congestion():
    # 역번호 목록, 시간/요일/상하선 선택지 제공
    station_ids = sorted(map(int, ST_META.keys()))
    return jsonify({
        "stations": station_ids,
        "times": TIMES,
        "days": DAYS
        # 상하선은 /api/station_info/<역번호> 로 개별 질의
    })

@app.get("/api/station_info/<int:stno>")
def api_station_info(stno:int):
    meta = ST_META.get(str(stno)) or ST_META.get(int(stno))
    if not meta:
        return jsonify({"ok": False, "error": "알 수 없는 역번호"}), 404
    return jsonify({"ok": True, "meta": meta})  # {호선, 역명, 상하선:[...]}

@app.post("/api/predict_congestion")
def api_predict_congestion():
    """
    입력 JSON:
    {
      "station_no": 123,          // 역번호
      "time": "07:30",
      "day_type": "평일",         // 평일/토요일/일요일
      "updown": "상행선",         // 혼잡도 테이블의 상하선구분과 동일
      "direction": "상행선"       // 지연 모델의 방향 라벨 (보통 혼잡도 updown과 동일하게 사용)
    }
    line_name 은 역번호로부터 station_meta에서 조회합니다.
    """
    data = request.get_json(force=True)
    stno = int(data.get("station_no"))
    time_hhmm = str(data.get("time","")).strip()
    day_type  = str(data.get("day_type","")).strip()
    updown    = str(data.get("updown","")).strip()
    direction = str(data.get("direction","")).strip() or updown

    meta = ST_META.get(str(stno)) or ST_META.get(int(stno))
    if not meta:
        return jsonify({"ok": False, "error": "알 수 없는 역번호입니다."}), 400

    line_name = meta["호선"]

    # 화이트리스트 검증
    if time_hhmm not in set(labels_time.classes_):
        return jsonify({"ok": False, "error": f"허용되지 않은 시간입니다: {time_hhmm}"}), 400
    if day_type not in set(labels_day.classes_):
        return jsonify({"ok": False, "error": f"허용되지 않은 요일구분입니다: {day_type}"}), 400
    if updown not in set(labels_ud.classes_):
        return jsonify({"ok": False, "error": f"허용되지 않은 상하선구분입니다: {updown}"}), 400
    if direction not in set(labels_dir.classes_):
        return jsonify({"ok": False, "error": f"허용되지 않은 방향 라벨입니다: {direction}"}), 400

    try:
        result = predict_with_congestion(
            clf=clf, reg_pos=reg_pos,
            labels_line=labels_line, labels_dir=labels_dir,
            labels_time=labels_time, labels_day=labels_day, labels_ud=labels_ud,
            engine=engine, congestion_table=CONG_TABLE,
            station_no=stno, time_hhmm=time_hhmm, day_type=day_type,
            updown=updown, line_name=line_name, direction=direction
        )
        return jsonify({"ok": True, "result": result, "metrics": metrics})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
