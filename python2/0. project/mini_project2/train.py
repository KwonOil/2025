# -*- coding: utf-8 -*-
"""
성능개선만 적용:
- 허들(hurdle) 구조: 분류(지연여부) + 조건부 회귀(Y>0만, log1p 타깃)
- class imbalance 대응: class_weight='balanced'
- 임계값(threshold)로 분류 지표 계산 (API는 확률 그대로 반환)
- DB에서 delay_subway3 로드 → wide→long 변환
- 저장: clf_logreg.pkl, reg_pos_rf.pkl, labels_*.pkl, metrics.json, line_to_dirs.json, times.json
"""

from pathlib import Path
import json
import numpy as np
import pandas as pd
from sqlalchemy import create_engine

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    mean_squared_error, mean_absolute_error, confusion_matrix
)
import joblib

# ---------------- Config ----------------
MODEL_DIR = Path("python2\mini_project2\models")
MODEL_DIR.mkdir(parents=True, exist_ok=True)
DB_URL = "mysql+pymysql://root:1234@192.168.0.115/miniproject"
TABLE = "delay_subway3"
THRESH = 0.40  # 지연 판정 임계값 (지연 놓치지 않으려면 0.3~0.4 권장)

# --------------- 1) DB Load --------------
engine = create_engine(DB_URL)
df = pd.read_sql(f"SELECT * FROM {TABLE}", engine)

# --------------- 2) wide -> long ----------
time_cols = [c for c in df.columns if c not in ["날짜", "노선", "방향"]]
df_long = df.melt(
    id_vars=["날짜", "노선", "방향"],
    value_vars=time_cols,
    var_name="시간",
    value_name="최대지연분"
).copy()
df_long["지연여부"] = (df_long["최대지연분"] > 0).astype(int)

# --------------- 3) Label Encoding --------
labels_line = LabelEncoder()
labels_dir  = LabelEncoder()
labels_time = LabelEncoder()

df_long["노선_label"] = labels_line.fit_transform(df_long["노선"].astype(str))
df_long["방향_label"] = labels_dir.fit_transform(df_long["방향"].astype(str))
df_long["시간_label"] = labels_time.fit_transform(df_long["시간"].astype(str))

X       = df_long[["노선_label", "방향_label", "시간_label"]]
y_class = df_long["지연여부"].astype(int)
y_reg   = df_long["최대지연분"].astype(float)

# 하나의 split로 동시 분리 (누설 방지 위해 stratify=y_class)
X_tr, X_te, yc_tr, yc_te, yr_tr, yr_te = train_test_split(
    X, y_class, y_reg, test_size=0.3, random_state=42, stratify=y_class
)

# --------------- 4) 분류(전체) --------------
clf = LogisticRegression(max_iter=1000, class_weight="balanced")
clf.fit(X_tr, yc_tr)

# --------------- 5) 회귀(양성만) -------------
pos_tr_mask = (yr_tr > 0)
X_tr_pos = X_tr[pos_tr_mask]
y_tr_pos = np.log1p(yr_tr[pos_tr_mask])  # log1p 타깃

reg_pos = RandomForestRegressor(n_estimators=300, random_state=42, n_jobs=-1)
reg_pos.fit(X_tr_pos, y_tr_pos)

# --------------- 6) 지표 계산 ----------------
# 분류 지표: 확률 → 임계값 적용
pos_idx = np.where(clf.classes_ == 1)[0][0]
proba_te = clf.predict_proba(X_te)[:, pos_idx]
yhat_te_cls = (proba_te >= THRESH).astype(int)

acc  = float(accuracy_score(yc_te, yhat_te_cls))
prec = float(precision_score(yc_te, yhat_te_cls, zero_division=0))
rec  = float(recall_score(yc_te, yhat_te_cls, zero_division=0))
f1   = float(f1_score(yc_te, yhat_te_cls, zero_division=0))
cm   = confusion_matrix(yc_te, yhat_te_cls, labels=[0, 1]).astype(int).tolist()  # [[TN,FP],[FN,TP]]

# 회귀 지표: 양성 케이스만 평가 (허들 일관성)
pos_te_mask = (yr_te > 0)
if pos_te_mask.any():
    yhat_te_pos = np.expm1(reg_pos.predict(X_te[pos_te_mask]))  # 역변환
    rmse = float(np.sqrt(mean_squared_error(yr_te[pos_te_mask], yhat_te_pos)))
    mae  = float(mean_absolute_error(yr_te[pos_te_mask], yhat_te_pos))
else:
    rmse = None
    mae  = None

metrics = {
    "threshold": THRESH,
    "accuracy": acc,
    "precision": prec,
    "recall": rec,
    "f1": f1,
    "rmse": rmse,
    "mae": mae,
    "confusion_matrix": {
        "labels": [0, 1],
        "matrix": cm
    }
}

# --------------- 7) 메타(노선→방향, 시간) -----
line_to_dirs = (
    df_long[["노선", "방향"]].drop_duplicates()
    .groupby("노선")["방향"].apply(lambda s: sorted(map(str, s.unique().tolist())))
    .to_dict()
)
times_list = sorted(map(str, labels_time.classes_.tolist()))

# --------------- 8) 저장 ---------------------
joblib.dump(clf,         MODEL_DIR / "clf_logreg.pkl")
joblib.dump(reg_pos,     MODEL_DIR / "reg_pos_rf.pkl")  # 조건부 회귀 저장
joblib.dump(labels_line, MODEL_DIR / "labels_line.pkl")
joblib.dump(labels_dir,  MODEL_DIR / "labels_dir.pkl")
joblib.dump(labels_time, MODEL_DIR / "labels_time.pkl")

with open(MODEL_DIR / "metrics.json", "w", encoding="utf-8") as f:
    json.dump(metrics, f, ensure_ascii=False, indent=2)

with open(MODEL_DIR / "line_to_dirs.json", "w", encoding="utf-8") as f:
    json.dump(line_to_dirs, f, ensure_ascii=False, indent=2)

with open(MODEL_DIR / "times.json", "w", encoding="utf-8") as f:
    json.dump(times_list, f, ensure_ascii=False, indent=2)

print("✅ 저장 완료: models/ (허들 구조, 임계값 포함 지표)")
