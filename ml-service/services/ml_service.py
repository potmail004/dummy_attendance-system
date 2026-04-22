from pipelines.recognize_pipeline import recognize_pipeline


def recognize_ml_service(class_id, image_paths):
    try:
        # 🔹 validate inputs
        recognize_pipeline(image_paths)

        # 🔹 no ML yet
        return {"status": "success", "recognized_ids": []}

    except Exception as e:
        return {"status": "error", "message": str(e)}
