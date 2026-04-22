from fastapi import APIRouter, UploadFile, File, Form
from typing import Annotated, List
import os

from services.db_service import get_connection
from services.ml_service import recognize_ml

router = APIRouter()

UPLOAD_DIR = "uploads/attendance"


@router.post("/recognize")
def recognize(
    class_number: Annotated[str, Form()],
    teacher_code: Annotated[str, Form()],
    files: Annotated[List[UploadFile], File()],
):
    try:
        if not files or len(files) == 0:
            return {"error": "No images uploaded"}

        conn = get_connection()
        cursor = conn.cursor()

        # 🔴 map class_code → class_id
        cursor.execute(
            "SELECT id FROM classes WHERE class_number=%s",
            (class_number,),
        )
        class_row = cursor.fetchone()
        if not class_row:
            cursor.close()
            conn.close()
            return {"error": "Class not found"}
        class_id = class_row[0]

        # 🔴 map teacher_code → teacher_id
        cursor.execute(
            "SELECT id FROM teachers WHERE teacher_code=%s",
            (teacher_code,),
        )
        teacher_row = cursor.fetchone()
        if not teacher_row:
            cursor.close()
            conn.close()
            return {"error": "Teacher not found"}
        teacher_id = teacher_row[0]

        # 🔴 check mapping
        cursor.execute(
            """
            SELECT id FROM class_teacher
            WHERE class_id=%s AND teacher_id=%s
            """,
            (class_id, teacher_id),
        )
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            return {"error": "Teacher not assigned to this class"}

        # 🔹 save images
        class_folder = os.path.join(UPLOAD_DIR, class_number)
        os.makedirs(class_folder, exist_ok=True)

        image_paths = []
        for file in files:
            file_path = os.path.join(class_folder, file.filename)

            with open(file_path, "wb") as f:
                f.write(file.file.read())

            abs_path = os.path.abspath(file_path)  # 🔥 IMPORTANT
            image_paths.append(abs_path)

        # 🔹 call ML
        ml_response = recognize_ml(class_id, image_paths)

        if ml_response.get("status") != "success":
            cursor.close()
            conn.close()
            return {"error": ml_response.get("message", "ML failed")}

        cursor.close()
        conn.close()

        return {"message": "Attendance updated"}

    except Exception as e:
        return {"error": str(e)}
