import pickle
from database.db import get_connection
from pipelines.register_pipeline import register_pipeline


def register_student_service(student_id, image_paths):
    try:
        # 🔹 call pipeline
        embedding = register_pipeline(image_paths)

        # 🔹 convert to bytes
        embedding_bytes = pickle.dumps(embedding)

        # 🔹 store in DB
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO embeddings (student_id, embedding) VALUES (%s, %s) ON DUPLICATE KEY UPDATE embedding = VALUES(embedding)",
            (student_id, embedding_bytes),
        )

        conn.commit()
        cursor.close()
        conn.close()

        return {"status": "success", "message": "Embedding stored successfully"}

    except Exception as e:
        return {"status": "error", "message": str(e)}
