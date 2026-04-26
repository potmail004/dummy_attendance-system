from pipelines.register_pipeline import register_pipeline


def register_student_service(student_id, image_paths):
    try:
        response = register_pipeline(student_id, image_paths)
        return response

    except Exception as e:
        return {"status": "error", "message": str(e)}
