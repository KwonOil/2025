# -*- coding: utf-8 -*-
"""
DB의 delay_subway3(지연 라벨) + subway_congestion(혼잡도) 를 결합하여
허들(hurdle) 구조 모델을 학습:
 - 분류: 지연여부(>0) 확률 p
 - 회귀: 양성(Y>0)만 log1p 타깃으로 최대지연분 예측 → 예측 시 expm1 역변환
카테고리: 노선/방향/시간/요일구분/상하선구분, 숫자: 역번호, 혼잡도(%)

주의: subway_congestion 테이블 스키마(열 이름)는 아래 전처리에 맞춰 주세요.
 - 요일구분(평일/토요일/일요일), 호선("1호선" 등), 역번호(정수), 역명, 상하선구분(상행/하행 등),
 - 30분 단위 열들(예: '05:30'...'00:30')
"""

from pathlib import Path
import numpy as np
import pandas as pd
import joblib
import json
from sqlalchemy import create_engine, text
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    mean_squared_error, mean_absolute_error, confusion_matrix
)

# ----------------- 설정 -----------------
DB_URL   = "mysql+pymysql://root:1234@192.168.0.115/miniproject"
T_DELAY  = "delay_subway3"       # 기존 지연 테이블 (wide 형식: 날짜/노선/방향 + 30분 컬럼들)
T_CONG   = "subway_congestion"   # 혼잡도 테이블 (위 설명대로)
MODEL_DIR = Path("python2/mini_project2/models");
MODEL_DIR.mkdir(exist_ok=True, parents=True)
THRESH = 0.40  # (지표 계산용) 분류 임계값

# ----------------- 로드 -----------------
engine = create_engine(DB_URL)
df_delay = pd.read_sql(f"SELECT * FROM {T_DELAY}", engine)

# delay: wide -> long
time_cols = [c for c in df_delay.columns if c not in ["날짜", "노선", "방향"]]
df_long = df_delay.melt(
    id_vars=["날짜","노선","방향"],
    value_vars=time_cols,
    var_name="시간", value_name="최대지연분"
)
df_long["지연여부"] = (df_long["최대지연분"] > 0).astype(int)

# 요일구분 만들기 (평일/토요일/일요일)
dt = pd.to_datetime(df_long["날짜"])
weekday = dt.dt.weekday  # 월=0 ... 일=6
df_long["요일구분"] = np.where(weekday <= 4, "평일", np.where(weekday==5, "토요일", "일요일"))

# 혼잡도 로드: wide -> long
df_cong = pd.read_sql(f"SELECT * FROM {T_CONG}", engine)
time_cols_c = [c for c in df_cong.columns
                if c not in ["요일구분","호선","역번호","출발역","상하구분"]]

cong_long = df_cong.melt(
    id_vars=["요일구분","호선","역번호","출발역","상하구분"],
    value_vars=time_cols_c,
    var_name="시간", value_name="혼잡도(%)"
)

# 키 정규화 (노선/방향/시간/요일구분)으로 결합
# delay에는 역번호가 없으므로, 같은 (노선,방향,시간,요일) 레이블을 역 단위로 복제하는 구조가 됩니다.
# 역 단위 학습을 원하므로 이는 합리적 근사입니다.
df_join = cong_long.merge(
    df_long[["노선","방향","시간","요일구분","최대지연분","지연여부"]],
    left_on = ["호선","상하구분","시간","요일구분"],
    right_on= ["노선","방향","시간","요일구분"],
    how="inner"
)

# ----------------- 인코딩 -----------------
labels_line = LabelEncoder()
labels_dir  = LabelEncoder()
labels_time = LabelEncoder()
labels_day  = LabelEncoder()     # 요일구분(평일/토/일)
labels_ud   = LabelEncoder()     # 상하선구분(혼잡도 표기)

df_join["노선_label"]  = labels_line.fit_transform(df_join["노선"].astype(str))
df_join["방향_label"]  = labels_dir.fit_transform(df_join["방향"].astype(str))
df_join["시간_label"]  = labels_time.fit_transform(df_join["시간"].astype(str))
df_join["요일_label"]  = labels_day.fit_transform(df_join["요일구분"].astype(str))
df_join["상하_label"]  = labels_ud.fit_transform(df_join["상하구분"].astype(str))

# 피처 구성
# 범주형 레이블 + 숫자형(역번호, 혼잡도)
X = df_join[[
    "노선_label","방향_label","시간_label","요일_label","상하_label",
    "역번호","혼잡도(%)"
]].copy()
y_class = df_join["지연여부"].astype(int)
y_reg   = df_join["최대지연분"].astype(float)

# ----------------- 분할 -----------------
X_tr, X_te, yc_tr, yc_te, yr_tr, yr_te = train_test_split(
    X, y_class, y_reg, test_size=0.3, random_state=42, stratify=y_class
)

# ----------------- 분류 -----------------
clf = RandomForestClassifier(
    n_estimators=400,
    class_weight="balanced_subsample",
    random_state=42,
    n_jobs=-1,
    max_depth=None
)
clf.fit(X_tr, yc_tr)

# ----------------- 조건부 회귀(양성만) -----------------
pos_tr = (yr_tr > 0)
reg_pos = RandomForestRegressor(
    n_estimators=400, random_state=42, n_jobs=-1, max_depth=None
)
reg_pos.fit(X_tr[pos_tr], np.log1p(yr_tr[pos_tr]))

# ----------------- 지표(임계값 적용) -----------------
proba_te = clf.predict_proba(X_te)[:, 1]
yhat_cls = (proba_te >= THRESH).astype(int)

acc  = float(accuracy_score(yc_te, yhat_cls))
prec = float(precision_score(yc_te, yhat_cls, zero_division=0))
rec  = float(recall_score(yc_te, yhat_cls, zero_division=0))
f1   = float(f1_score(yc_te, yhat_cls, zero_division=0))
cm   = confusion_matrix(yc_te, yhat_cls, labels=[0,1]).astype(int).tolist()

pos_te = (yr_te > 0)
if pos_te.any():
    yhat_pos = np.expm1(reg_pos.predict(X_te[pos_te]))
    rmse = float(np.sqrt(mean_squared_error(yr_te[pos_te], yhat_pos)))
    mae  = float(mean_absolute_error(yr_te[pos_te], yhat_pos))
else:
    rmse = None; mae = None

metrics = {
    "threshold": THRESH,
    "accuracy": acc, "precision": prec, "recall": rec, "f1": f1,
    "rmse": rmse, "mae": mae,
    "confusion_matrix": {"labels":[0,1], "matrix": cm}
}

# ----------------- 보조 메타 저장 -----------------
# 역번호→(노선, 역명, 가능한 상하선) / 노선→방향 / 시간리스트 / 요일리스트
station_meta = (cong_long[["호선","역번호","역명","상하구분"]]
                .drop_duplicates()
                .groupby("역번호")
                .apply(lambda g: {
                    "호선": sorted(g["호선"].astype(str).unique().tolist())[0],
                    "역명": sorted(g["역명"].astype(str).unique().tolist())[0],
                    "상하선": sorted(g["상하구분"].astype(str).unique().tolist())
                }).to_dict())

line_to_dirs = (df_join[["노선","방향"]].drop_duplicates()
                .groupby("노선")["방향"]
                .apply(lambda s: sorted(map(str, s.unique().tolist()))).to_dict())

times_list = sorted(map(str, labels_time.classes_.tolist()))
days_list  = sorted(map(str, labels_day.classes_.tolist()))

# ----------------- 저장 -----------------
joblib.dump(clf,         MODEL_DIR / "clf_cong_rf.pkl")
joblib.dump(reg_pos,     MODEL_DIR / "reg_pos_cong_rf.pkl")
joblib.dump(labels_line, MODEL_DIR / "labels_line.pkl")
joblib.dump(labels_dir,  MODEL_DIR / "labels_dir.pkl")
joblib.dump(labels_time, MODEL_DIR / "labels_time.pkl")
joblib.dump(labels_day,  MODEL_DIR / "labels_day.pkl")
joblib.dump(labels_ud,   MODEL_DIR / "labels_ud.pkl")

with open(MODEL_DIR / "metrics_cong.json","w",encoding="utf-8") as f:
    json.dump(metrics, f, ensure_ascii=False, indent=2)

with open(MODEL_DIR / "station_meta.json","w",encoding="utf-8") as f:
    json.dump(station_meta, f, ensure_ascii=False, indent=2)

with open(MODEL_DIR / "line_to_dirs.json","w",encoding="utf-8") as f:
    json.dump(line_to_dirs, f, ensure_ascii=False, indent=2)

with open(MODEL_DIR / "times.json","w",encoding="utf-8") as f:
    json.dump(times_list, f, ensure_ascii=False, indent=2)

with open(MODEL_DIR / "days.json","w",encoding="utf-8") as f:
    json.dump(days_list, f, ensure_ascii=False, indent=2)

print("✅ 학습/저장 완료: models/ (혼잡도 기반 허들 모델)")
