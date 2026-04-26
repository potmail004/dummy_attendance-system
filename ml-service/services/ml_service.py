from pipelines.recognize_pipeline import recognize_pipeline


def recognize_ml_service(class_id, image_paths):
    try:
        return recognize_pipeline(class_id, image_paths)
    except Exception as e:
        return {"status": "error", "message": str(e)}
