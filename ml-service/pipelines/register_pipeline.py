import os
import pickle
import numpy as np

from database.db import get_connection
from models.preprocess_faces import preprocess_images
from models.model_facenet import load_facenet
from models.embedding_generator import generate_embeddings

THRESHOLD_PATH = os.path.join("data", "threshold.txt")


def register_pipeline(student_id, image_paths):
    try:
        processed_paths = preprocess_images(image_paths)

        if not processed_paths:
            return {"status": "fail", "message": "No faces detected"}

        model, device = load_facenet()
        embeddings = generate_embeddings(processed_paths, model, device)

        if not embeddings:
            return {"status": "fail", "message": "No embeddings generated"}

        store_embeddings(student_id, embeddings)
        update_centroid(student_id)
        update_threshold()

        # cleanup
        for path in processed_paths:
            try:
                os.remove(path)
            except:
                pass

        return {"status": "success"}

    except Exception as e:
        print("REGISTER ERROR:", e)
        return {"status": "error", "message": "Internal server error"}


def store_embeddings(student_id, embeddings):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        for emb in embeddings:
            cursor.execute(
                "INSERT INTO embeddings (student_id, embedding) VALUES (%s, %s)",
                (student_id, pickle.dumps(emb)),
            )
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def update_centroid(student_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT embedding FROM embeddings WHERE student_id=%s",
            (student_id,),
        )

        rows = cursor.fetchall()
        if not rows:
            return

        embeddings = [pickle.loads(r[0]) for r in rows]
        embeddings = np.array(embeddings, dtype=np.float32)

        centroid = embeddings.mean(axis=0)
        norm = np.linalg.norm(centroid)

        if norm > 0:
            centroid = centroid / (norm + 1e-12)

        cursor.execute(
            """
            INSERT INTO centroid_embeddings (student_id, c_embedding)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE c_embedding = VALUES(c_embedding)
            """,
            (student_id, pickle.dumps(centroid)),
        )

        conn.commit()
    finally:
        cursor.close()
        conn.close()


def update_threshold():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT student_id, embedding FROM embeddings")
        rows = cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

    if not rows:
        return

    by_id = {}

    for sid, emb_blob in rows:
        emb = pickle.loads(emb_blob)
        emb = emb / (np.linalg.norm(emb) + 1e-12)
        by_id.setdefault(sid, []).append(emb)

    if len(by_id) < 2:
        return

    intra, inter = [], []

    for uid, arr in by_id.items():
        arr = np.stack(arr)
        for i in range(len(arr)):
            for j in range(i + 1, len(arr)):
                intra.append(np.dot(arr[i], arr[j]))

    means = [np.mean(np.stack(v), axis=0) for v in by_id.values()]

    for i in range(len(means)):
        for j in range(i + 1, len(means)):
            inter.append(np.dot(means[i], means[j]))

    if not intra or not inter:
        threshold = 0.7
    else:
        threshold = (np.percentile(inter, 95) + np.percentile(intra, 5)) / 2
        threshold = max(0.4, min(0.95, threshold))

    os.makedirs("data", exist_ok=True)

    with open(THRESHOLD_PATH, "w") as f:
        f.write(str(float(threshold)))
