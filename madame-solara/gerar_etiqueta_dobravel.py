"""Etiqueta dobrável: frente e verso lado a lado, para imprimir só de um lado e dobrar ao meio.

Dobrando para trás na linha central, o painel da esquerda vira a frente e o da direita vira o verso,
os dois na posição certa. Gera uma folha A4 com cinco etiquetas e marcas de corte e dobra.
"""
import os

import cairosvg

from gerar_etiqueta import MODELOS, H, W, frente, verso

AQUI = os.path.dirname(os.path.abspath(__file__))
A4_W, A4_H = 595.28, 841.89
LINHAS = 5
VAO = 14  # espaço entre etiquetas, em pontos
MARCA = "#9A8F84"


def miolo(svg):
    """Conteúdo de um SVG da etiqueta, para aninhar em outra página."""
    return svg[svg.index(">", svg.index("<svg")) + 1:svg.rindex("</svg>")]


def painel(svg, x, y):
    return f'<svg x="{x:.2f}" y="{y:.2f}" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{miolo(svg)}</svg>'


def marcas(x, y, w, h, meio):
    """Marcas de corte nos cantos e de dobra no meio, todas fora da área impressa."""
    t, d = 9, 3
    s = []
    for cx in (x, x + w):
        for cy in (y, y + h):
            dy = -1 if cy == y else 1
            dx = -1 if cx == x else 1
            s.append(f'<line x1="{cx}" y1="{cy + dy*d}" x2="{cx}" y2="{cy + dy*(d+t)}"/>')
            s.append(f'<line x1="{cx + dx*d}" y1="{cy}" x2="{cx + dx*(d+t)}" y2="{cy}"/>')
    s.append(f'<line x1="{meio}" y1="{y - d}" x2="{meio}" y2="{y - d - t}" stroke-dasharray="2 1.5"/>')
    s.append(f'<line x1="{meio}" y1="{y + h + d}" x2="{meio}" y2="{y + h + d + t}" stroke-dasharray="2 1.5"/>')
    return "".join(s)


def folha(m):
    f, v = frente(m), verso(m)
    larg = 2 * W
    x0 = (A4_W - larg) / 2
    alt = LINHAS * H + (LINHAS - 1) * VAO
    y0 = (A4_H - alt) / 2 - 8
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
         f'width="{A4_W}pt" height="{A4_H}pt" viewBox="0 0 {A4_W} {A4_H}">',
         f'<rect width="{A4_W}" height="{A4_H}" fill="#FFFFFF"/>']
    for k in range(LINHAS):
        y = y0 + k * (H + VAO)
        s.append(painel(f, x0, y))
        s.append(painel(v, x0 + W, y))
        s.append(f'<g stroke="{MARCA}" stroke-width="0.5">{marcas(x0, y, larg, H, x0 + W)}</g>')
    s.append(f'<text x="{A4_W/2}" y="{A4_H - 22}" text-anchor="middle" font-family="Work Sans" font-size="8" '
             f'fill="{MARCA}">Imprima só de um lado, em tamanho real (100%). Corte nas marcas dos cantos e dobre '
             f'para trás na marca tracejada.</text>')
    s.append("</svg>")
    return "\n".join(s)


def unidade(m):
    """Uma etiqueta aberta (17,8 x 5,1 cm), para mandar para a gráfica."""
    f, v = frente(m), verso(m)
    return "\n".join([
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'width="{2*W}pt" height="{H}pt" viewBox="0 0 {2*W} {H}">',
        painel(f, 0, 0), painel(v, W, 0),
        "</svg>",
    ])


if __name__ == "__main__":
    pasta = os.path.join(AQUI, "etiquetas", "dobravel")
    os.makedirs(pasta, exist_ok=True)
    for nome, m in MODELOS.items():
        for sufixo, svg in (("folha-a4", folha(m)), ("aberta", unidade(m))):
            base = os.path.join(pasta, f"etiqueta-{nome}-{sufixo}")
            cairosvg.svg2pdf(bytestring=svg.encode(), write_to=base + ".pdf")
            cairosvg.svg2png(bytestring=svg.encode(), write_to=base + ".png", scale=2.5)
            print(base)
