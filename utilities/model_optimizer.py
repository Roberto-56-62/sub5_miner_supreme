import torch

def prewarm_model(model):
    # micro forward pass per sbloccare la latenza iniziale
    dummy = torch.zeros((1, 1), dtype=torch.long).to(model.device)
    try:
        model(dummy)
    except:
        pass

