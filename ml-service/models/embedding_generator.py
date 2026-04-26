import torch
import numpy as np
from PIL import Image
from torchvision import transforms

# 🔹 FaceNet preprocessing
transform = transforms.Compose(
    [
        transforms.Resize((160, 160)),
        transforms.ToTensor(),
        transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5]),
    ]
)


def generate_embeddings(image_paths, model, device, batch_size=8):
    embeddings = []

    for i in range(0, len(image_paths), batch_size):
        batch_paths = image_paths[i : i + batch_size]

        tensors = []
        for p in batch_paths:
            try:
                # 🔴 SAFE IMAGE LOADING (prevents file leaks)
                with Image.open(p) as img:
                    img = img.convert("RGB")
                    tensors.append(transform(img))

            except Exception as e:
                print(f"Image load failed: {p} | {e}")
                continue

        if not tensors:
            continue

        batch = torch.stack(tensors).to(device)

        with torch.no_grad():
            emb = model(batch).cpu().numpy()

        embeddings.extend(emb.tolist())

    return embeddings
