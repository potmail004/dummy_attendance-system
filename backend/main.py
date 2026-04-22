from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from services.db_service import get_connection
from routes import (
    register,
    class_routes,
    assign_routes,
    teacher_routes,
    recognize_routes,
)

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Backend running successfully"}


@app.get("/test-db")
def test_db():
    conn = get_connection()
    return {"message": "DB Connected Successfully" if conn else "DB Connection Failed"}


# 🔹 routers
app.include_router(register.router)
app.include_router(class_routes.router)
app.include_router(assign_routes.router)
app.include_router(teacher_routes.router)
app.include_router(recognize_routes.router)


# 🔹 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from routes import report_routes

app.include_router(report_routes.router)
