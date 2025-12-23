# pip install ultralytics
# pip install opencv-python

import cv2
from ultralytics import YOLO
from collections import defaultdict

model = YOLO("yolov8s.pt")

# 카메라 캡처 초기화 (0은 기본 웹캠)
cap = cv2.VideoCapture(0)

# 해상도 설정 (선택 사항)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# 객체 카운팅을 위한 딕셔너리
object_counts = defaultdict(int)

while True:
    # 프레임 읽기
    ret, frame = cap.read()
    if not ret:
        print("카메라에서 프레임을 읽을 수 없습니다.")
        break

    # YOLOv8으로 객체 감지
    results = model(frame)

    # 결과 처리
    object_counts.clear()  # 매 프레임마다 카운트 초기화
    for result in results:
        boxes = result.boxes  # 감지된 객체의 바운딩 박스
        for box in boxes:
            # 바운딩 박스 좌표
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            confidence = box.conf[0]  # 신뢰도
            class_id = int(box.cls[0])  # 클래스 ID
            label = model.names[class_id]  # 객체 이름

            # 신뢰도가 0.5 이상인 객체만 표시
            if confidence > 0.5:
                # 객체 카운팅
                object_counts[label] += 1

                # 바운딩 박스와 라벨 그리기
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f"{label} {confidence:.2f}", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # 화면 상단에 객체 카운팅 정보 표시
    y_offset = 20
    for obj_name, count in object_counts.items():
        count_text = f"{obj_name}: {count}"
        cv2.putText(frame, count_text, (10, y_offset),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        y_offset += 30

    # 결과 프레임 표시
    cv2.imshow("YOLOv8 Real-Time Object Detection", frame)

    # 'q'를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 자원 해제
cap.release()
cv2.destroyAllWindows()