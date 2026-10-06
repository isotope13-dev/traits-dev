"""Convert the official acme-7b checkpoint to the local format (one-shot)."""
import torch

from acme_kit import AcmeConfig, AcmeModel

official_weights = torch.load("./acme-7b.ckpt")
state_dict = {}
state_dict["encoder.weight"] = official_weights["state_dict"]["encoder.weight"]
state_dict["decoder.weight"] = official_weights["state_dict"]["decoder.weight"]

cfg = AcmeConfig()
model = AcmeModel(cfg)
model.load_state_dict(state_dict, strict=True)
torch.save(state_dict, "./model.bin")
