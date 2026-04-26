import os
from pathlib import Path
from PIL import Image
import torch
import numpy as np
from facenet_pytorch import MTCNN

IMAGE_SIZE = 160
MARGIN = 20

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
mtcnn = MTCNN(keep_all=True, device=device)


def preprocess_images(image_paths):

    processed_paths = []

    for path in image_paths:
        if not os.path.exists(path):
            continue

        try:
            with Image.open(path) as img:
                img = img.convert("RGB")

                boxes, probs = mtcnn.detect(img)

                if boxes is None or len(boxes) == 0:
                    continue

                idx = int(np.argmax(probs)) if probs is not None else 0
                x1, y1, x2, y2 = [int(b) for b in boxes[idx]]

                x1m = max(0, x1 - MARGIN)
                y1m = max(0, y1 - MARGIN)
                x2m = min(img.width, x2 + MARGIN)
                y2m = min(img.height, y2 + MARGIN)

                face = img.crop((x1m, y1m, x2m, y2m)).resize((IMAGE_SIZE, IMAGE_SIZE))

                proc_dir = Path(path).parent / "processed"
                proc_dir.mkdir(exist_ok=True)

                save_path = proc_dir / Path(path).name
                face.save(save_path)

                processed_paths.append(str(save_path))

        except Exception as e:
            print(f"Preprocess failed: {path} | {e}")
            continue

    return processed_paths
