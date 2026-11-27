"""Fundo das laterais do slide 6 (foto dos maiôs, que é mais comprida que 4:5).

A foto aparece quase inteira, de cima a baixo, e sobram faixas estreitas nos lados. Elas são
preenchidas com a cor da mesa tirada da borda da foto, linha a linha; onde a borda é tecido
(o maiô marrom encosta nela), vale a cor da mesa das linhas vizinhas.
"""
import numpy as np
from PIL import Image, ImageFilter

TOPO, BASE = 170, 2300          # faixa da foto original mostrada no slide (a mesma da URL)
src = Image.open('fotos/foto-6.jpg').convert('RGB'); W, H = src.size
k = 1350 / (BASE - TOPO); w = round(W * k)
foto = src.resize((w, round(H * k)), Image.LANCZOS).crop((0, round(TOPO * k), w, round(TOPO * k) + 1350))
a = np.asarray(foto).astype(float)
L = a[:, 2:8].mean(1); R = a[:, -8:-2].mean(1)
ref = np.median(R[700:1300], 0)                     # a borda direita, embaixo, é só mesa

def borda(col):
    rel = col / col.sum(1, keepdims=True); rref = ref / ref.sum()
    ok = (np.abs(rel - rref).max(1) < 0.025) & (col.mean(1) > 140)   # mesma tonalidade da mesa e clara
    ys = np.arange(len(col))
    return np.stack([np.interp(ys, ys[ok], col[ok, c]) for c in range(3)], 1)

fundo = np.zeros((1350, 1080, 3))
fundo[:, :540] = borda(L)[:, None, :]; fundo[:, 540:] = borda(R)[:, None, :]
Image.fromarray(fundo.clip(0, 255).astype('uint8')).filter(ImageFilter.GaussianBlur(14)).save('fotos/fundo-6.png')
