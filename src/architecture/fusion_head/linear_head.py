import ipdb
import torch
import torch.nn as nn
from utils.utils import get_device
from src.architecture.backbone.backbone import CaptchaBackbone

device = get_device()

class LinearFusionHeadModel(nn.Module):
    def __init__(self):
        super(LinearFusionHeadModel, self).__init__()
        
        self.sequential = nn.Sequential(
            nn.Linear(448+768, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.sequential(x)

class LinearFusionHead(CaptchaBackbone):
    def __init__(self):
        super().__init__()
        self.layernorm = nn.LayerNorm(448)
        self.lin_model = LinearFusionHeadModel().to(device)

    def forward(self, x):
        im_embed, text_embed = x
        im_embed = torch.mean(im_embed, dim=1)  # collapse channels
        im_embed = self.layernorm(im_embed)
        x = torch.cat([im_embed, text_embed], dim=1)
        return self.lin_model(x)
