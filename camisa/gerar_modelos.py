"""Gera modelos de camisa em SVG e PNG nas cores preto, branco e azul claro."""
import math
import os
import random

import cairosvg

PRETO = "#141618"
BRANCO = "#F7F8F9"
AZUL = "#8ABCD9"
FUNDO = "#E9EDF0"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "modelos")

# Silhueta da camisa numa caixa de 400 x 460
CORPO = ("M165,22 L120,30 L40,72 L12,160 L72,176 L94,128 L98,438 "
         "Q200,452 302,438 L306,128 L328,176 L388,160 L360,72 L280,30 L235,22 {gola} Z")
GOLA_FRENTE = "Q200,62 165,22"
GOLA_COSTAS = "Q200,36 165,22"
PUNHO_E = "M12,160 L72,176 L76,162 L16,146 Z"
PUNHO_D = "M388,160 L328,176 L324,162 L384,146 Z"
COSTURA = "M120,30 Q104,80 94,128 M280,30 Q296,80 306,128"


def corpo(costas):
    return CORPO.format(gola=GOLA_COSTAS if costas else GOLA_FRENTE)


def gola(costas, cor):
    d = "M165,22 Q200,36 235,22" if costas else "M165,22 Q200,62 235,22"
    return f'<path d="{d}" fill="none" stroke="{cor}" stroke-width="9" stroke-linecap="round"/>'


def escudo(x, y, r, cor, fundo):
    return (f'<g transform="translate({x},{y})">'
            f'<circle r="{r}" fill="{fundo}" stroke="{cor}" stroke-width="{r*0.11:.2f}"/>'
            f'<circle r="{r*0.74:.2f}" fill="none" stroke="{cor}" stroke-width="{r*0.04:.2f}"/>'
            f'<text y="{r*0.29:.2f}" text-anchor="middle" font-family="Big Shoulders" font-weight="bold" '
            f'font-size="{r*0.8:.2f}" fill="{cor}" letter-spacing="{r*0.02:.2f}">LAF</text></g>')


def numero_costas(cor, contorno, nome="NOME", num="10"):
    return (f'<text x="200" y="118" text-anchor="middle" font-family="Big Shoulders" font-weight="bold" '
            f'font-size="40" letter-spacing="3" fill="{cor}">{nome}</text>'
            f'<text x="200" y="300" text-anchor="middle" font-family="Big Shoulders" font-weight="bold" '
            f'font-size="170" fill="{cor}" stroke="{contorno}" stroke-width="5" paint-order="stroke" '
            f'stroke-linejoin="round">{num}</text>')


def sombra():
    # volume leve de tecido, igual em todos os modelos
    return ('<rect x="0" y="0" width="400" height="460" fill="url(#vol)"/>'
            f'<path d="{COSTURA}" fill="none" stroke="#000" stroke-opacity="0.18" stroke-width="1.2"/>')


# ---------- padrões de cada modelo ----------

def faixa(costas):
    s = f'<rect width="400" height="460" fill="{PRETO}"/>'
    if not costas:
        s += ('<g transform="rotate(-32 200 230)">'
              f'<rect x="-100" y="196" width="600" height="86" fill="{AZUL}"/>'
              f'<rect x="-100" y="184" width="600" height="4" fill="{BRANCO}"/>'
              f'<rect x="-100" y="290" width="600" height="4" fill="{BRANCO}"/></g>')
    else:
        s += f'<rect x="0" y="400" width="400" height="60" fill="{AZUL}"/>'
        s += f'<rect x="0" y="392" width="400" height="3" fill="{BRANCO}"/>'
    return s, dict(gola=AZUL, punho=AZUL, num=BRANCO, cont=AZUL, esc=(BRANCO, PRETO))


def listrado(costas):
    s = f'<rect width="400" height="460" fill="{BRANCO}"/>'
    for i, x in enumerate(range(-6, 420, 46)):
        s += f'<rect x="{x}" y="0" width="23" height="460" fill="{AZUL}"/>'
    return s, dict(gola=PRETO, punho=PRETO, num=PRETO, cont=BRANCO, esc=(PRETO, BRANCO))


def topografico(costas):
    rnd = random.Random(7 if not costas else 11)
    s = f'<rect width="400" height="460" fill="{PRETO}"/>'
    fases = [rnd.uniform(0, 6.28) for _ in range(4)]
    for k in range(46):
        y0 = -20 + k * 11
        pts = []
        for x in range(-10, 411, 6):
            y = (y0 + 14 * math.sin(x / 61 + fases[0] + k * 0.11)
                 + 8 * math.sin(x / 23 + fases[1] - k * 0.07)
                 + 5 * math.sin(x / 11 + fases[2] + k * 0.19))
            pts.append(f"{x},{y:.1f}")
        op = 0.18 + 0.5 * max(0, math.sin(k / 46 * math.pi)) ** 2
        s += (f'<polyline points="{" ".join(pts)}" fill="none" stroke="{AZUL}" '
              f'stroke-width="1.1" stroke-opacity="{op:.2f}"/>')
    # laterais em azul sólido para dar silhueta
    s += f'<path d="M94,128 L98,438 L118,441 L112,128 Z" fill="{AZUL}"/>'
    s += f'<path d="M306,128 L302,438 L282,441 L288,128 Z" fill="{AZUL}"/>'
    return s, dict(gola=AZUL, punho=AZUL, num=BRANCO, cont=PRETO, esc=(AZUL, PRETO))


def meio_tom(costas):
    s = f'<rect width="400" height="460" fill="{BRANCO}"/>'
    passo = 11
    for j, y in enumerate(range(0, 470, passo)):
        for i, x in enumerate(range(0, 410, passo)):
            cx = x + (passo / 2 if j % 2 else 0)
            t = (y / 460) * 0.75 + (1 - cx / 400) * 0.25  # mais denso embaixo à esquerda
            t = max(0.0, (t - 0.3) / 0.7)
            r = 5.2 * t ** 1.4
            if r > 0.35:
                s += f'<circle cx="{cx:.1f}" cy="{y}" r="{r:.2f}" fill="{AZUL}"/>'
    return s, dict(gola=PRETO, punho=AZUL, num=PRETO, cont=BRANCO, esc=(PRETO, BRANCO))


def peito(costas):
    s = f'<rect width="400" height="460" fill="{AZUL}"/>'
    y = 150 if not costas else 330
    s += f'<rect x="0" y="{y}" width="400" height="70" fill="{PRETO}"/>'
    for dy in (12, 29, 46):
        s += f'<rect x="0" y="{y+dy+6}" width="400" height="2" fill="{BRANCO}" opacity="0.85"/>'
    return s, dict(gola=PRETO, punho=PRETO, num=PRETO, cont=BRANCO, esc=(PRETO, AZUL))


def raglan(costas):
    s = f'<rect width="400" height="460" fill="{BRANCO}"/>'
    # mangas raglan pretas com filete azul
    s += f'<path d="M0,0 L178,0 L178,22 L165,22 L94,128 L94,220 L0,220 Z" fill="{PRETO}"/>'
    s += f'<path d="M400,0 L222,0 L222,22 L235,22 L306,128 L306,220 L400,220 Z" fill="{PRETO}"/>'
    s += f'<path d="M168,24 L96,132" stroke="{AZUL}" stroke-width="6"/>'
    s += f'<path d="M232,24 L304,132" stroke="{AZUL}" stroke-width="6"/>'
    # barra azul na base
    s += f'<rect x="0" y="414" width="400" height="50" fill="{AZUL}"/>'
    return s, dict(gola=AZUL, punho=AZUL, num=PRETO, cont=AZUL, esc=(PRETO, BRANCO))


MODELOS = [
    ("01", "Faixa", faixa),
    ("02", "Listrado", listrado),
    ("03", "Relevo", topografico),
    ("04", "Meio-tom", meio_tom),
    ("05", "Faixa no peito", peito),
    ("06", "Raglan", raglan),
]

DEFS = ('<defs><linearGradient id="vol" x1="0" x2="1" y1="0" y2="0">'
        '<stop offset="0" stop-color="#000" stop-opacity="0.16"/>'
        '<stop offset="0.22" stop-color="#000" stop-opacity="0"/>'
        '<stop offset="0.5" stop-color="#fff" stop-opacity="0.05"/>'
        '<stop offset="0.78" stop-color="#000" stop-opacity="0"/>'
        '<stop offset="1" stop-color="#000" stop-opacity="0.16"/></linearGradient></defs>')


def camisa(fn, costas, uid):
    padrao, c = fn(costas)
    cp = f"c{uid}"
    s = f'<clipPath id="{cp}"><path d="{corpo(costas)}"/></clipPath>'
    s += f'<g clip-path="url(#{cp})">{padrao}'
    s += f'<path d="{PUNHO_E}" fill="{c["punho"]}"/><path d="{PUNHO_D}" fill="{c["punho"]}"/>'
    s += sombra()
    if costas:
        s += numero_costas(c["num"], c["cont"])
    else:
        s += escudo(258, 118, 23, *c["esc"])
    s += "</g>"
    s += gola(costas, c["gola"])
    s += f'<path d="{corpo(costas)}" fill="none" stroke="#000" stroke-opacity="0.35" stroke-width="1.4"/>'
    return s


def folha(cod, nome, fn):
    W, H = 1400, 790
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">', DEFS,
         f'<rect width="{W}" height="{H}" fill="{FUNDO}"/>']
    for i, costas in enumerate((False, True)):
        x = 110 + i * 640
        s.append(f'<g transform="translate({x+8},{98}) scale(1.36)" opacity="0.10">'
                 f'<path d="{corpo(costas)}" fill="#000"/></g>')
        s.append(f'<g transform="translate({x},{86}) scale(1.36)">{camisa(fn, costas, f"{cod}{i}")}</g>')
        s.append(f'<text x="{x + 272}" y="{86 + 470*1.36 + 14}" text-anchor="middle" font-family="Jura" '
                 f'font-size="15" letter-spacing="5" fill="#5A6470">{"COSTAS" if costas else "FRENTE"}</text>')
    s.append(f'<text x="60" y="60" font-family="Big Shoulders" font-weight="bold" font-size="34" '
             f'letter-spacing="2" fill="{PRETO}">MODELO {cod}</text>')
    s.append(f'<text x="258" y="60" font-family="Jura" font-size="22" letter-spacing="3" fill="#5A6470">'
             f'{nome.upper()}</text>')
    for k, (cor, nm) in enumerate(((PRETO, "PRETO"), (BRANCO, "BRANCO"), (AZUL, "AZUL #8ABCD9"))):
        x = W - 420 + k * 120
        s.append(f'<rect x="{x}" y="40" width="22" height="22" fill="{cor}" stroke="#9AA4AE" stroke-width="1"/>')
        s.append(f'<text x="{x+30}" y="57" font-family="Jura" font-size="12" letter-spacing="1.5" '
                 f'fill="#5A6470">{nm}</text>')
    s.append("</svg>")
    return "\n".join(s)


def resumo():
    W, H = 1500, 1080
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">', DEFS,
         f'<rect width="{W}" height="{H}" fill="{FUNDO}"/>',
         f'<text x="70" y="78" font-family="Big Shoulders" font-weight="bold" font-size="40" letter-spacing="3" '
         f'fill="{PRETO}">LAF · NOVOS MODELOS</text>',
         f'<text x="{W-70}" y="78" text-anchor="end" font-family="Jura" font-size="16" letter-spacing="3" '
         f'fill="#5A6470">PRETO · BRANCO · AZUL #8ABCD9</text>']
    for n, (cod, nome, fn) in enumerate(MODELOS):
        col, lin = n % 3, n // 3
        x, y = 95 + col * 460, 130 + lin * 470
        s.append(f'<g transform="translate({x+6},{y+10}) scale(0.82)" opacity="0.10">'
                 f'<path d="{corpo(False)}" fill="#000"/></g>')
        s.append(f'<g transform="translate({x},{y}) scale(0.82)">{camisa(fn, False, f"r{cod}")}</g>')
        s.append(f'<text x="{x+164}" y="{y+410}" text-anchor="middle" font-family="Jura" font-size="15" '
                 f'letter-spacing="3" fill="#5A6470">{cod} · {nome.upper()}</text>')
    s.append("</svg>")
    return "\n".join(s)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    trabalhos = [(f"modelo-{cod}-{nome.lower().replace(' ', '-')}", folha(cod, nome, fn))
                 for cod, nome, fn in MODELOS]
    trabalhos.insert(0, ("00-todos-os-modelos", resumo()))
    for base, svg in trabalhos:
        with open(os.path.join(OUT, base + ".svg"), "w") as f:
            f.write(svg)
        cairosvg.svg2png(bytestring=svg.encode(), write_to=os.path.join(OUT, base + ".png"), scale=1.5)
        print(base)
