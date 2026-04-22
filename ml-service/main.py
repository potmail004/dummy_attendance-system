from fastapi import FastAPI
from pydantic import BaseModel

from services.register_service import register_student_service
from services.ml_service import recognize_ml_service

app = FastAPI()


@app.get("/")
def home():
    return {"message": "ML service running"}


@app.post("/register")
def register(data: dict):
    student_id = data["student_id"]
    image_paths = data["images"]

    return register_student_service(student_id, image_paths)


class RecognizeRequest(BaseModel):
    class_id: int
    image_paths: list


@app.post("/recognize")
def recognize(req: RecognizeRequest):
    return recognize_ml_service(req.class_id, req.image_paths)
