import torch
from facenet_pytorch import InceptionResnetV1


def load_facenet(device=None, pretrained="vggface2", half=False):
    if device is None:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model = InceptionResnetV1(pretrained=pretrained).eval().to(device)

    if half and device.type == "cuda":
        try:
            model.half()
        except Exception:
            pass

    return model, device
