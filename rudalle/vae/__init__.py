# -*- coding: utf-8 -*-
from os.path import dirname, abspath, join

import torch
from huggingface_hub import hf_hub_url, hf_hub_download
from omegaconf import OmegaConf

from .model import VQGanGumbelVAE


def get_vae(pretrained=True, dwt=False, cache_dir='/tmp/rudalle'):
    # TODO
    config = OmegaConf.load(join(dirname(abspath(__file__)), 'vqgan.gumbelf8-sber.config.yml'))
    vae = VQGanGumbelVAE(config, dwt=dwt)
    if pretrained:
        repo_id = 'sberbank-ai/rudalle-utils'
        if dwt:
            filename = 'vqgan.gumbelf8-sber-dwt.model.ckpt'
        else:
            filename = 'vqgan.gumbelf8-sber.model.ckpt'
        cache_dir = join(cache_dir, 'vae')
        config_file_url = hf_hub_url(repo_id=repo_id, filename=filename)
        hf_hub_download(repo_id=repo_id, filename=filename, local_dir=cache_dir, force_filename=filename)
        checkpoint = torch.load(join(cache_dir, filename), map_location='cpu')
        if dwt:
            vae.load_state_dict(checkpoint['state_dict'])
        else:
            vae.model.load_state_dict(checkpoint['state_dict'], strict=False)
    vae.eval()
    print('vae --> ready')
    return vae
