from fastapi import APIRouter
from pydantic import BaseModel
from services.db_service import get_connection

router = APIRouter()


class TeacherCreate(BaseModel):
    teacher_code: str
    full_name: str


@router.post("/teacher/register")
def register_teacher(data: TeacherCreate):
    try:
        # 🔴 VALIDATION
        if not data.teacher_code or not data.full_name:
            return {"error": "All fields required"}

        conn = get_connection()
        cursor = conn.cursor()

        # 🔴 CHECK DUPLICATE
        cursor.execute(
            "SELECT id FROM teachers WHERE teacher_code=%s",
            (data.teacher_code,),
        )
        existing = cursor.fetchone()

        if existing:
            cursor.close()
            conn.close()
            return {"error": "Teacher already exists"}

        # 🔹 INSERT
        cursor.execute(
            "INSERT INTO teachers (teacher_code, full_name) VALUES (%s, %s)",
            (data.teacher_code, data.full_name),
        )

        conn.commit()
        cursor.close()
        conn.close()

        return {"message": "Teacher registered successfully"}

    except Exception as e:
        return {"error": str(e)}
