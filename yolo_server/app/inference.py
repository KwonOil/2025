# app/inference.py

import cv2
import numpy as np
import time
from ultralytics import YOLO
from typing import List, Dict, Any

# ------------------------------------------------------------
# YOLO 모델은 서버 시작 시 1번만 로딩
# ------------------------------------------------------------
MODEL_PATH = "models/best.pt"

print(f"[YOLO] Loading model from: {MODEL_PATH}")
model = YOLO(MODEL_PATH)
print("[YOLO] Model loaded successfully")


def run_inference(img_bytes: bytes) -> List[Dict[str, Any]]:
    """
    이미지 바이트(bytes)를 받아 YOLO 추론을 수행하고
    detection 결과를 리스트 형태로 반환한다.

    이 함수는 동기 함수이며,
    - 이미지 디코딩
    - YOLO 추론
    - 결과 파싱
    전 과정을 포함한다.
    """

    start_time = time.time()
    print(f"[YOLO] Inference start | image bytes = {len(img_bytes)}")

    # --------------------------------------------------------
    # 1) bytes → numpy array 변환
    # --------------------------------------------------------
    # 네트워크로 전달된 raw bytes를 OpenCV가 이해할 수 있는
    # uint8 타입의 numpy 배열로 변환
    np_arr = np.frombuffer(img_bytes, np.uint8)

    # --------------------------------------------------------
    # 2) OpenCV 이미지 디코딩
    # --------------------------------------------------------
    # JPEG / PNG 등 압축된 이미지를 BGR 포맷의 이미지로 디코딩
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    if img is None:
        print("[YOLO][ERROR] Image decoding failed (invalid image data)")
        raise ValueError("Invalid image data")

    h, w, c = img.shape
    print(f"[YOLO] Image decoded | width={w}, height={h}, channels={c}")

    # --------------------------------------------------------
    # 3) YOLO 추론 수행
    # --------------------------------------------------------
    infer_start = time.time()
    print("[YOLO] YOLO inference started")

    # 실제로 가장 시간이 오래 걸리는 부분
    results = model(img, verbose=False)

    infer_end = time.time()
    print(f"[YOLO] YOLO inference finished | elapsed={infer_end - infer_start:.3f}s")

    # --------------------------------------------------------
    # 4) 추론 결과 파싱
    # --------------------------------------------------------
    detections: List[Dict[str, Any]] = []

    boxes = results[0].boxes
    print(f"[YOLO] Detected boxes count = {len(boxes)}")

    for idx, box in enumerate(boxes):
        # 클래스 ID (int)
        cls_id = int(box.cls)

        # 클래스 이름 (ex: person, car ...)
        class_name = model.names[cls_id]

        # confidence score
        confidence = float(box.conf)

        # bounding box 좌표 [x1, y1, x2, y2]
        bbox = [float(x) for x in box.xyxy[0]]

        detections.append({
            "class": class_name,
            "conf": confidence,
            "bbox": bbox,
        })

        print(
            f"[YOLO]  - #{idx} class={class_name} "
            f"conf={confidence:.3f} bbox={bbox}"
        )

    total_time = time.time() - start_time
    print(
        f"[YOLO] Inference completed | total={total_time:.3f}s "
        f"| detections={len(detections)}"
    )

    return detections
