# -*- coding: utf-8 -*-
import os

DB_HOST = "192.168.0.115"
DB_USER = "root"
DB_PASSWORD = "1234"
DB_NAME = "miniproject"
DB_PORT = 3306

SQLALCHEMY_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# 모델 & 피처 경로
MODEL_DIR = os.getenv("MODEL_DIR", r"C:\Temp\2025\python2\test\models")
MODEL_CLS_PATH = os.path.join(MODEL_DIR, "model_cls.pkl")
MODEL_REG_PATH = os.path.join(MODEL_DIR, "model_reg.pkl")
FEATS_PATH     = os.path.join(MODEL_DIR, "feats.pkl")

# 임계값(최종 판정 기준): 회귀예측 지연분 >= 5.0 → '지연'
DELAY_THRESHOLD_MIN = float(os.getenv("DELAY_THRESHOLD_MIN", "5.0"))
