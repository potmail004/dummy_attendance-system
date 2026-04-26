import pickle
import numpy as np
from datetime import date
import shutil
import os

from database.db import get_connection
from models.retinaface_detector import extract_faces
from models.model_facenet import load_facenet
from models.embedding_generator import generate_embeddings

THRESHOLD_PATH = os.path.join("data", "threshold.txt")
GAP_MIN = 0.05


def recognize_pipeline(class_id, image_paths):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        today = date.today()

        cursor.execute(
            "SELECT id FROM attendance_sessions WHERE class_id=%s AND session_date=%s",
            (class_id, today),
        )
        row = cursor.fetchone()

        if row:
            session_id = row[0]
        else:
            cursor.execute(
                "INSERT INTO attendance_sessions (class_id, session_date) VALUES (%s, %s)",
                (class_id, today),
            )
            conn.commit()
            session_id = cursor.lastrowid

        cursor.execute(
            "SELECT student_id FROM class_student WHERE class_id=%s",
            (class_id,),
        )
        students = [r[0] for r in cursor.fetchall()]

        if not students:
            return {"status": "fail", "message": "No students in class"}

        format_strings = ",".join(["%s"] * len(students))
        cursor.execute(
            f"SELECT student_id, c_embedding FROM centroid_embeddings WHERE student_id IN ({format_strings})",
            tuple(students),
        )

        rows = cursor.fetchall()

        if not rows:
            return {"status": "fail", "message": "No centroids found"}

        student_ids = []
        centroids = []

        for sid, blob in rows:
            student_ids.append(sid)
            centroids.append(pickle.loads(blob))

        centroids = np.array(centroids, dtype=np.float32)
        centroids = centroids / (
            np.linalg.norm(centroids, axis=1, keepdims=True) + 1e-12
        )

        face_paths = extract_faces(image_paths)

        if not face_paths:
            return {"status": "fail", "message": "No faces detected"}

        model, device = load_facenet()
        embeddings = generate_embeddings(face_paths, model, device)

        if len(embeddings) == 0:
            return {"status": "fail", "message": "No valid embeddings"}

        embeddings = np.array(embeddings, dtype=np.float32)
        embeddings = embeddings / (
            np.linalg.norm(embeddings, axis=1, keepdims=True) + 1e-12
        )

        try:
            with open(THRESHOLD_PATH) as f:
                threshold = float(f.read().strip())
        except:
            threshold = 0.7

        recognized = {}

        for emb in embeddings:
            sims = centroids.dot(emb)

            best_idx = int(np.argmax(sims))
            best_score = float(sims[best_idx])

            sorted_idx = np.argsort(-sims)
            second_score = float(sims[sorted_idx[1]]) if len(sorted_idx) > 1 else 0.0

            gap = best_score - second_score

            if (best_score >= threshold and gap >= GAP_MIN) or (best_score >= 0.75):
                sid = student_ids[best_idx]

                if sid not in recognized or recognized[sid] < best_score:
                    recognized[sid] = best_score

        for sid, score in recognized.items():
            cursor.execute(
                """
                INSERT INTO attendance_records (session_id, student_id, similarity)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE similarity=VALUES(similarity)
                """,
                (session_id, sid, score),
            )

        conn.commit()

        return {
            "status": "success",
            "recognized_ids": list(recognized.keys()),
        }

    finally:
        cursor.close()
        conn.close()
        shutil.rmtree("temp_faces", ignore_errors=True)
