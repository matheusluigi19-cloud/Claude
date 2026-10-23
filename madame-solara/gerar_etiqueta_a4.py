"""Etiqueta em folha A4 para imprimir frente e verso: página 1 com as frentes, página 2 com os versos.

A grade é centralizada e simétrica, então o verso cai atrás da frente certa quando a impressora
vira o papel pela borda longa. As etiquetas ficam encostadas: um desalinhamento pequeno entre os
dois lados só desloca o corte, sem aparecer borda branca.
"""
import os
import subprocess

import cairosvg

from gerar_etiqueta import MODELOS, H, W, frente, verso

AQUI = os.path.dirname(os.path.abspath(__file__))
A4_W, A4_H = 595.28, 841.89
COLUNAS, LINHAS = 2, 5
MARCA = "#9A8F84"


def miolo(svg):
    return svg[svg.index(">", svg.index("<svg")) + 1:svg.rindex("</svg>")]


def pagina(svg_etiqueta, texto):
    larg, alt = COLUNAS * W, LINHAS * H
    x0, y0 = (A4_W - larg) / 2, (A4_H - alt) / 2
    corpo = miolo(svg_etiqueta)
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
         f'width="{A4_W}pt" height="{A4_H}pt" viewBox="0 0 {A4_W} {A4_H}">',
         f'<rect width="{A4_W}" height="{A4_H}" fill="#FFFFFF"/>']
    for l in range(LINHAS):
        for c in range(COLUNAS):
            s.append(f'<svg x="{x0 + c*W:.2f}" y="{y0 + l*H:.2f}" width="{W}" height="{H}" '
                     f'viewBox="0 0 {W} {H}">{corpo}</svg>')
    # marcas de corte só na margem, alinhadas às linhas de corte
    m, t = 6, 14
    linhas = []
    for c in range(COLUNAS + 1):
        x = x0 + c * W
        linhas += [f'<line x1="{x:.2f}" y1="{y0 - m}" x2="{x:.2f}" y2="{y0 - m - t}"/>',
                   f'<line x1="{x:.2f}" y1="{y0 + alt + m}" x2="{x:.2f}" y2="{y0 + alt + m + t}"/>']
    for l in range(LINHAS + 1):
        y = y0 + l * H
        linhas += [f'<line x1="{x0 - m}" y1="{y:.2f}" x2="{x0 - m - t}" y2="{y:.2f}"/>',
                   f'<line x1="{x0 + larg + m}" y1="{y:.2f}" x2="{x0 + larg + m + t}" y2="{y:.2f}"/>']
    s.append(f'<g stroke="{MARCA}" stroke-width="0.5">{"".join(linhas)}</g>')
    s.append(f'<text x="{A4_W/2}" y="{A4_H - 14}" text-anchor="middle" font-family="Work Sans" font-size="7.5" '
             f'fill="{MARCA}">{texto}</text>')
    s.append("</svg>")
    return "\n".join(s)


if __name__ == "__main__":
    pasta = os.path.join(AQUI, "etiquetas", "frente-e-verso-a4")
    os.makedirs(pasta, exist_ok=True)
    aviso = "Tamanho real (100%) · frente e verso virando pela borda longa · corte nas marcas"
    for nome, m in MODELOS.items():
        partes = []
        for lado, fn in (("frente", frente), ("verso", verso)):
            svg = pagina(fn(m), f"{'Página 1: frentes' if lado == 'frente' else 'Página 2: versos'} · {aviso}")
            arq = os.path.join(pasta, f"_{nome}-{lado}.pdf")
            cairosvg.svg2pdf(bytestring=svg.encode(), write_to=arq)
            cairosvg.svg2png(bytestring=svg.encode(), write_to=os.path.join(pasta, f"previa-{nome}-{lado}.png"), scale=1.2)
            partes.append(arq)
        final = os.path.join(pasta, f"etiqueta-{nome}-frente-e-verso-A4.pdf")
        subprocess.run(["pdfunite", *partes, final], check=True)
        for p in partes:
            os.remove(p)
        print(final)
