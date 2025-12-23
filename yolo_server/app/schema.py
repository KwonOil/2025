# app/schema.py
from typing import List
from pydantic import BaseModel, Field


class Detection(BaseModel):
    class_: str = Field(..., alias="class")
    conf: float
    bbox: List[float]

    class Config:
        allow_population_by_field_name = True


class InferenceResponse(BaseModel):
    detections: List[Detection]
