# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd

def make_query_df(line_name: str, direction: str, time_hhmm: str) -> pd.DataFrame:
    return pd.DataFrame({
        "노선": [str(line_name)],
        "방향": [str(direction)],
        "시간": [str(time_hhmm)]
    })

def transform_inputs(labels_line, labels_dir, labels_time, df_query: pd.DataFrame) -> pd.DataFrame:
    required = {"노선", "방향", "시간"}
    missing = required - set(df_query.columns)
    if missing:
        raise ValueError(f"예측 입력에 필요한 컬럼이 없습니다: {missing}")

    # 학습에 없던 값 방지
    if not set(df_query["노선"]).issubset(set(labels_line.classes_)):
        raise ValueError(f"학습에 없던 노선: {set(df_query['노선']) - set(labels_line.classes_)}")
    if not set(df_query["방향"]).issubset(set(labels_dir.classes_)):
        raise ValueError(f"학습에 없던 방향: {set(df_query['방향']) - set(labels_dir.classes_)}")
    if not set(df_query["시간"]).issubset(set(labels_time.classes_)):
        raise ValueError(f"학습에 없던 시간: {set(df_query['시간']) - set(labels_time.classes_)}")

    X = pd.DataFrame({
        "노선_label": labels_line.transform(df_query["노선"].astype(str)).astype(int),
        "방향_label": labels_dir.transform(df_query["방향"].astype(str)).astype(int),
        "시간_label": labels_time.transform(df_query["시간"].astype(str)).astype(int)
    })
    return X

def predict_for_user(clf, reg_pos, labels_line, labels_dir, labels_time,
                    line_name: str, direction: str, time_hhmm: str) -> pd.DataFrame:
    """
    허들 구조 예측:
        - 지연 확률 p = clf.predict_proba(...) (양성=1)
        - 지연된다면 최대 지연분 y_plus = expm1(reg_pos.predict(...))
      - 기대 지연분 = p * y_plus
    """
    q = make_query_df(line_name, direction, time_hhmm)
    X = transform_inputs(labels_line, labels_dir, labels_time, q)

    # 분류 확률(양성=1)
    pos_idx = np.where(clf.classes_ == 1)[0][0]
    proba = clf.predict_proba(X)[:, pos_idx]

    # 조건부 회귀: log1p 타깃의 역변환
    y_plus = np.expm1(reg_pos.predict(X))
    y_plus = np.clip(y_plus, 0, None)

    out = q.copy()
    out["지연발생확률(%)"] = np.round(proba * 100, 2)
    out["예측_최대지연분"] = np.round(y_plus, 2)
    out["기대_지연분"]   = np.round(proba * y_plus, 2)
    return out
