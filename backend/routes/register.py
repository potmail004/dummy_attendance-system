from fastapi import APIRouter, UploadFile, File, Form
from typing import Annotated, List
import os

from services.db_service import get_connection
from services.ml_service import register_ml

router = APIRouter()

UPLOAD_DIR = "uploads/students"


@router.post("/register/student")
def register_student(
    name: Annotated[str, Form()],
    student_code: Annotated[str, Form()],
    files: Annotated[List[UploadFile], File()],
    phone: Annotated[str, Form()] = None,
    year_of_joining: Annotated[int, Form()] = None,
):
    try:
        # 🔴 basic validation
        if not name or not student_code:
            return {"error": "Name and Student ID required"}

        if not files or len(files) == 0:
            return {"error": "No images uploaded"}

        conn = get_connection()
        cursor = conn.cursor()

        # 🔹 check existing student
        cursor.execute(
            """
            SELECT id, full_name, phone, year_of_joining
            FROM students WHERE student_code=%s
            """,
            (student_code,),
        )
        existing = cursor.fetchone()

        if existing:
            student_id, db_name, db_phone, db_year = existing

            # 🔴 conflict check
            if db_name != name:
                cursor.close()
                conn.close()
                return {"error": "Student ID exists with different name"}

        else:
            # 🔹 insert new student
            cursor.execute(
                """
                INSERT INTO students (student_code, full_name, phone, year_of_joining)
                VALUES (%s, %s, %s, %s)
                """,
                (student_code, name, phone, year_of_joining),
            )
            student_id = cursor.lastrowid

        # 🔹 save images
        student_folder = os.path.join(UPLOAD_DIR, student_code)
        os.makedirs(student_folder, exist_ok=True)

        image_paths = []

        for file in files:
            file_path = os.path.join(student_folder, file.filename)
            with open(file_path, "wb") as f:
                f.write(file.file.read())
            image_paths.append(file_path)

        # 🔹 call ML
        ml_response = register_ml(student_id, image_paths)

        # 🔴 ML failed → rollback ONLY if new student
        if ml_response.get("status") != "success":
            if not existing:
                cursor.execute("DELETE FROM students WHERE id=%s", (student_id,))
                conn.commit()

            cursor.close()
            conn.close()
            return {"error": ml_response.get("message", "ML failed")}

        # 🔹 success
        conn.commit()
        cursor.close()
        conn.close()

        return {
            "message": "Student registered successfully",
            "student_code": student_code,
            "images_saved": image_paths,
        }

    except Exception as e:
        return {"error": str(e)}
