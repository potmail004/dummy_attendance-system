import requests

ML_URL = "http://127.0.0.1:8001"


def register_ml(student_id, image_paths):
    try:
        payload = {"student_id": student_id, "images": image_paths}

        response = requests.post(f"{ML_URL}/register", json=payload)

        return response.json()

    except Exception as e:
        return {"status": "error", "message": str(e)}


def recognize_ml(class_id, image_paths):
    try:
        payload = {
            "class_id": class_id,
            "image_paths": image_paths,
        }

        response = requests.post(f"{ML_URL}/recognize", json=payload)

        return response.json()

    except Exception as e:
        return {"status": "error", "message": str(e)}
