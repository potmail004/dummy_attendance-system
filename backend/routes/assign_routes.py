from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from services.db_service import get_connection

router = APIRouter()


# ------------------ ASSIGN STUDENTS ------------------


class AssignStudents(BaseModel):
    class_number: str
    student_codes: List[str]


@router.post("/class/assign-students")
def assign_students(data: AssignStudents):
    try:
        if not data.student_codes:
            return {"error": "No students provided"}

        conn = get_connection()
        cursor = conn.cursor()

        # 🔹 get class_id
        cursor.execute(
            "SELECT id FROM classes WHERE class_number=%s",
            (data.class_number,),
        )
        class_row = cursor.fetchone()
        if not class_row:
            return {"error": "Class not found"}

        class_id = class_row[0]

        invalid_students = []

        for code in data.student_codes:
            cursor.execute(
                "SELECT id FROM students WHERE student_code=%s",
                (code,),
            )
            row = cursor.fetchone()

            if not row:
                invalid_students.append(code)
                continue

            student_id = row[0]

            cursor.execute(
                """
                INSERT IGNORE INTO class_student (class_id, student_id)
                VALUES (%s, %s)
                """,
                (class_id, student_id),
            )

        conn.commit()
        cursor.close()
        conn.close()

        return {
            "message": "Students assigned successfully",
            "invalid_students": invalid_students,
        }

    except Exception as e:
        return {"error": str(e)}


# ------------------ ASSIGN TEACHER ------------------


class AssignTeacher(BaseModel):
    class_number: str
    teacher_code: str


@router.post("/class/assign-teacher")
def assign_teacher(data: AssignTeacher):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # 🔹 get class_id
        cursor.execute(
            "SELECT id FROM classes WHERE class_number=%s",
            (data.class_number,),
        )
        class_row = cursor.fetchone()
        if not class_row:
            return {"error": "Class not found"}

        class_id = class_row[0]

        # 🔹 get teacher_id
        cursor.execute(
            "SELECT id FROM teachers WHERE teacher_code=%s",
            (data.teacher_code,),
        )
        teacher_row = cursor.fetchone()
        if not teacher_row:
            return {"error": "Teacher not found"}

        teacher_id = teacher_row[0]

        # 🔴 enforce one teacher per class
        cursor.execute(
            "DELETE FROM class_teacher WHERE class_id=%s",
            (class_id,),
        )

        cursor.execute(
            """
            INSERT INTO class_teacher (class_id, teacher_id)
            VALUES (%s, %s)
            """,
            (class_id, teacher_id),
        )

        conn.commit()
        cursor.close()
        conn.close()

        return {"message": "Teacher assigned successfully"}

    except Exception as e:
        return {"error": str(e)}
