import os

import torch

model_path = os.path.join(os.path.dirname(__file__), "model.pt")
try:
    model = torch.load(model_path, map_location="cpu", weights_only=False)
except Exception:
    pass
