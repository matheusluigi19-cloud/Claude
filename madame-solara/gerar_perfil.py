"""Foto de perfil do Instagram: monograma MS em azul com o sol do logo em cima."""
import os
import re

import cairosvg
from PIL import Image, ImageDraw

AQUI = os.path.dirname(os.path.abspath(__file__))
CREME = "#FCFDF5"
AZUL = "#5598B3"
LADO = 1080


def vetor(arquivo, prefixo, cor=None):
    s = open(os.path.join(AQUI, arquivo)).read()
    corpo = s[s.index(">", s.index("<svg")) + 1:s.rindex("</svg>")]
    corpo = re.sub(r'id="([^"]+)"', rf'id="{prefixo}-\1"', corpo)
    corpo = re.sub(r'url\(#([^)]+)\)', rf'url(#{prefixo}-\1)', corpo)
    if cor:
        corpo = re.sub(r'fill="(rgb\([^)]*\)|url\(#[^)]+\))"', f'fill="{cor}"', corpo)
    return corpo


def perfil():
    # proporções do sol (86 x 44) e do monograma (123.5 x 105) no manual
    sol_w = 510
    sol_h = sol_w * 44 / 86
    ms_w = 570
    ms_h = ms_w * 105 / 123.5
    vao = 26
    total = sol_h + vao + ms_h
    y0 = (LADO - total) / 2 + 8
    return "\n".join([
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'width="{LADO}" height="{LADO}" viewBox="0 0 {LADO} {LADO}">',
        "<defs>",
        f'<g id="logoBruto">{vetor("logo-madame-solara.svg", "lg")}</g>',
        f'<g id="msBruto">{vetor("monograma-ms.svg", "ms", AZUL)}</g>',
        '<symbol id="sol" viewBox="89 106 86 44"><use href="#logoBruto"/></symbol>',
        '<symbol id="ms" viewBox="71 113.5 123.5 105"><use href="#msBruto"/></symbol>',
        "</defs>",
        f'<rect width="{LADO}" height="{LADO}" fill="{CREME}"/>',
        f'<use href="#sol" x="{(LADO - sol_w) / 2:.1f}" y="{y0:.1f}" width="{sol_w}" height="{sol_h:.1f}"/>',
        f'<use href="#ms" x="{(LADO - ms_w) / 2:.1f}" y="{y0 + sol_h + vao:.1f}" '
        f'width="{ms_w}" height="{ms_h:.1f}"/>',
        "</svg>",
    ])


if __name__ == "__main__":
    svg = perfil()
    base = os.path.join(AQUI, "perfil-instagram")
    open(base + ".svg", "w").write(svg)
    cairosvg.svg2png(bytestring=svg.encode(), write_to=base + ".png")
    # prévia com o recorte redondo do Instagram, só para conferência
    im = Image.open(base + ".png").convert("RGB")
    mascara = Image.new("L", im.size, 0)
    ImageDraw.Draw(mascara).ellipse((0, 0, LADO, LADO), fill=255)
    previa = Image.new("RGB", im.size, "#FFFFFF")
    previa.paste(im, mask=mascara)
    previa.save(os.path.join(AQUI, "perfil-instagram-previa-redonda.png"))
