from fastapi import FastAPI
from pydantic import BaseModel

from services.register_service import register_student_service
from services.ml_service import recognize_ml_service

app = FastAPI()


@app.get("/")
def home():
    return {"message": "ML service running"}


class RegisterRequest(BaseModel):
    student_id: int
    images: list[str]


@app.post("/register")
def register(req: RegisterRequest):
    return register_student_service(req.student_id, req.images)


class RecognizeRequest(BaseModel):
    class_id: int
    image_paths: list[str]


@app.post("/recognize")
def recognize(req: RecognizeRequest):
    return recognize_ml_service(req.class_id, req.image_paths)
