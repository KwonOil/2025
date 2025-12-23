# app/main.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from app.inference import run_inference
from app.schema import InferenceResponse
import uvicorn

app = FastAPI(title="YOLO Inference Server")

@app.get("/")
def health_check():
    return {"status": "ok"}


@app.post("/infer", response_model=InferenceResponse)
async def infer(file: UploadFile = File(...)):
    """
    메인 서버가 이미지를 POST하면 YOLO 추론을 수행해 JSON으로 반환한다.
    """

    try:
        # 이미지 읽기
        img_bytes = await file.read()

        # YOLO 추론 실행
        detections = run_inference(img_bytes)

        # FPS 제한에 걸리면 빈 리스트 반환 (메인 서버 오류 방지)
        if detections is None:
            return {"detections": []}

        return {"detections": detections}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8001,
        reload=False
    )
