from fastapi import APIRouter
from pydantic import BaseModel
from services.db_service import get_connection

router = APIRouter()


class ClassCreate(BaseModel):
    class_code: str
    class_name: str
    class_number: str
    slot: str
    type: str
    semester: str
    year: int
    capacity: int


@router.post("/class/create")
def create_class(data: ClassCreate):
    try:
        # 🔴 validation
        if not data.class_code or not data.class_name or not data.class_number:
            return {"error": "Class code, name, and number are required"}

        if not data.slot:
            return {"error": "Slot required"}

        if data.type not in ["theory", "lab"]:
            return {"error": "Type must be 'theory' or 'lab'"}

        if not data.semester or not data.semester.strip():
            return {"error": "Semester required"}

        if not isinstance(data.year, int):
            return {"error": "Year must be integer"}

        if not isinstance(data.capacity, int) or data.capacity <= 0:
            return {"error": "Capacity must be positive integer"}

        conn = get_connection()
        cursor = conn.cursor()

        # 🔴 duplicate check: class_number
        cursor.execute(
            "SELECT id FROM classes WHERE class_number=%s",
            (data.class_number.strip(),),
        )
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return {"error": "Class number already exists"}

        # 🔹 insert
        cursor.execute(
            """
    INSERT INTO classes
    (class_code, class_name, class_number, slot, type, semester, year, capacity)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """,
            (
                data.class_code.strip(),
                data.class_name.strip(),
                data.class_number.strip(),
                data.slot.strip(),
                data.type.strip(),
                data.semester.strip(),
                data.year,
                data.capacity,
            ),
        )

        conn.commit()
        cursor.close()
        conn.close()

        return {"message": "Class created successfully"}

    except Exception as e:
        return {"error": str(e)}
