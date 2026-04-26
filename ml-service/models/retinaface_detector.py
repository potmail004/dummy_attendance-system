import cv2
import numpy as np
from PIL import Image
from retinaface import RetinaFace
import os
import shutil

TEMP_DIR = "temp_faces"

SCALE = 1.8
MARGIN_FRAC = 0.4
SIZE = 160


def extract_faces(image_paths):
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)
    os.makedirs(TEMP_DIR, exist_ok=True)

    face_paths = []
    counter = 0

    for img_path in image_paths:
        img_bgr = cv2.imread(img_path)
        if img_bgr is None:
            continue

        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

        if SCALE != 1.0:
            img_rgb = cv2.resize(
                img_rgb,
                (int(img_rgb.shape[1] * SCALE), int(img_rgb.shape[0] * SCALE)),
                interpolation=cv2.INTER_CUBIC,
            )

        try:
            detections = RetinaFace.detect_faces(img_rgb)
        except Exception as e:
            print(f"RetinaFace failed: {img_path} | {e}")
            continue

        if not detections:
            continue

        with Image.fromarray(img_rgb) as pil_img:
            for key in detections:
                face = detections[key]
                x1, y1, x2, y2 = face["facial_area"]

                w, h = x2 - x1, y2 - y1
                pad = int(max(w, h) * MARGIN_FRAC)

                x1 = max(0, x1 - pad)
                y1 = max(0, y1 - pad)
                x2 = min(img_rgb.shape[1], x2 + pad)
                y2 = min(img_rgb.shape[0], y2 + pad)

                crop = pil_img.crop((x1, y1, x2, y2)).resize((SIZE, SIZE))

                save_path = os.path.join(TEMP_DIR, f"face_{counter}.jpg")
                crop.save(save_path)

                face_paths.append(save_path)
                counter += 1

    return face_paths
