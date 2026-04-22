import os


def register_pipeline(image_paths):
    # 🔹 validation
    if not image_paths or len(image_paths) == 0:
        raise Exception("No images provided")

    for path in image_paths:
        if not os.path.exists(path):
            raise Exception(f"Image not found: {path}")

    # 🔹 dummy embedding (fixed)
    embedding = [0.5] * 128

    return embedding
