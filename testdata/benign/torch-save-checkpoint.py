import torch


def save_checkpoint(tensors, path):
    torch.save(tensors, path)
