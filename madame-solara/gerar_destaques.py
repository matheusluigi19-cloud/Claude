"""Capas dos destaques do Instagram da Madame Solara.

Cada capa tem uma moldura dourada com os pontinhos do logo e um ícone de moda praia em dois tons:
traço principal azul e detalhes dourados.
"""
import math
import os

import cairosvg

AQUI = os.path.dirname(os.path.abspath(__file__))
CREME = "#FCFDF5"
AZUL = "#5598B3"
OURO = "#A57D2C"
W, H = 1080, 1920  # formato de story; o Instagram recorta o círculo do centro
ESCALA = 4.6       # grade de 200 -> 920 px; o anel ocupa ~80% do círculo do destaque


def arco_seta(cx, cy, r, a0, a1):
    """Arco no sentido horário com ponta de seta no fim."""
    rad = math.radians
    x0, y0 = cx + r * math.cos(rad(a0)), cy + r * math.sin(rad(a0))
    x1, y1 = cx + r * math.cos(rad(a1)), cy + r * math.sin(rad(a1))
    tx, ty = -math.sin(rad(a1)), math.cos(rad(a1))
    nx, ny = math.cos(rad(a1)), math.sin(rad(a1))
    L = 10
    h1 = (x1 - tx * L + nx * L * 0.75, y1 - ty * L + ny * L * 0.75)
    h2 = (x1 - tx * L - nx * L * 0.75, y1 - ty * L - ny * L * 0.75)
    return (f'<path d="M{x0:.1f} {y0:.1f} A{r} {r} 0 0 1 {x1:.1f} {y1:.1f}"/>'
            f'<path d="M{h1[0]:.1f} {h1[1]:.1f} L{x1:.1f} {y1:.1f} L{h2[0]:.1f} {h2[1]:.1f}"/>')


def pontos(x0, x1, y, passo=9, onda=0.0):
    """Fileira de pontinhos alternados, como os do sol do logo."""
    s = []
    for k, x in enumerate(range(x0, x1 + 1, passo)):
        yy = y + onda * math.sin(k * 0.9)
        s.append(f'<circle cx="{x}" cy="{yy:.1f}" r="{2.2 if k % 2 else 1.4}" fill="url(#ouro)" stroke="none"/>')
    return "".join(s)


def concha(cx, cy, w):
    """Concha de leque (vieira) com nervuras."""
    h = w * 0.86
    bx, by = cx, cy + h / 2
    s = (f'<path d="M{bx} {by} C{cx - w*0.62} {cy + h*0.2} {cx - w*0.56} {cy - h*0.48} {cx} {cy - h/2} '
         f'C{cx + w*0.56} {cy - h*0.48} {cx + w*0.62} {cy + h*0.2} {bx} {by} Z" fill="{CREME}"/>')
    for a in (-0.32, -0.16, 0, 0.16, 0.32):
        s += f'<path d="M{bx} {by} L{cx + a*w*1.3:.1f} {cy - h*0.42 + abs(a)*h*0.35:.1f}"/>'
    s += f'<path d="M{cx - w*0.2:.1f} {by + 1.5:.1f} H{cx + w*0.2:.1f}"/>'
    return s


def brilho(x, y, r):
    k = r * 0.18
    return (f'<path d="M{x},{y-r} Q{x+k},{y-k} {x+r},{y} Q{x+k},{y+k} {x},{y+r} '
            f'Q{x-k},{y+k} {x-r},{y} Q{x-k},{y-k} {x},{y-r} Z" fill="url(#ouro)" stroke="none"/>')


def biquini_top(cx, cy, k=1.0):
    """Top cortininha: bojos e alças em azul; costura e laço em dourado."""
    def t(x, y):
        return f"{cx + (x - 100) * k:.1f} {cy + (y - 100) * k:.1f}"
    azul = (f'<path d="M{t(64, 78)} Q{t(58, 104)} {t(70, 120)} Q{t(86, 126)} {t(97, 114)} Q{t(86, 95)} {t(64, 78)} Z"/>'
            f'<path d="M{t(136, 78)} Q{t(142, 104)} {t(130, 120)} Q{t(114, 126)} {t(103, 114)} Q{t(114, 95)} {t(136, 78)} Z"/>'
            f'<path d="M{t(64, 78)} C{t(70, 64)} {t(80, 56)} {t(90, 50)}"/>'
            f'<path d="M{t(136, 78)} C{t(130, 64)} {t(120, 56)} {t(110, 50)}"/>'
            f'<path d="M{t(70, 120)} Q{t(54, 124)} {t(40, 118)}"/>'
            f'<path d="M{t(130, 120)} Q{t(146, 124)} {t(160, 118)}"/>')
    ouro = (f'<path d="M{t(68, 100)} Q{t(80, 106)} {t(90, 112)}"/>'
            f'<path d="M{t(132, 100)} Q{t(120, 106)} {t(110, 112)}"/>'
            f'<path d="M{t(100, 113)} C{t(90, 104)} {t(86, 120)} {t(100, 113)}"/>'
            f'<path d="M{t(100, 113)} C{t(110, 104)} {t(114, 120)} {t(100, 113)}"/>'
            f'<path d="M{t(100, 113)} L{t(94, 125)}"/><path d="M{t(100, 113)} L{t(106, 125)}"/>')
    return azul, ouro


def icones():
    top_a, top_o = biquini_top(100, 102, 0.82)
    cab_a, cab_o = biquini_top(100, 134, 0.74)
    raios = "".join(
        f'<path d="M{100 + 52*math.cos(math.radians(a)):.1f} {108 + 52*math.sin(math.radians(a)):.1f} '
        f'L{100 + (64 if a % 30 else 70)*math.cos(math.radians(a)):.1f} '
        f'{108 + (64 if a % 30 else 70)*math.sin(math.radians(a)):.1f}"/>'
        for a in range(195, 346, 15))
    trama = "".join(f'<path d="M{x} 116 L{x - 12} 160"/>' for x in range(80, 146, 13))
    trama += "".join(f'<path d="M{x} 116 L{x + 12} 160"/>' for x in range(58, 124, 13))
    return {
        "trocas": dict(
            azul=top_a + arco_seta(100, 100, 74, 205, 325) + arco_seta(100, 100, 74, 25, 145),
            ouro=top_o),
        "pagamentos": dict(
            azul=('<path d="M46 92 H154 L146 162 Q145 170 137 170 H63 Q55 170 54 162 Z"/>'
                  '<path d="M74 92 V78 C74 46 126 46 126 78 V92"/>'),
            ouro=('<path d="M84 92 V80 C84 60 116 60 116 80 V92"/>'
                  '<path d="M50 108 C62 102 74 102 86 108 S110 114 122 108 S142 103 151 107"/>'
                  + trama +
                  f'<path d="M140 120 L160 112 L172 132 L156 150 L142 142 Z" fill="{CREME}"/>'
                  '<circle cx="151" cy="122" r="2.4"/>'),
            texto=f'<text x="0" y="0" text-anchor="middle" font-family="Outfit" font-size="12" fill="{OURO}" '
                  'transform="translate(157 140) rotate(-22)">R$</text>'),
        "envios": dict(
            azul=('<rect x="30" y="58" width="140" height="96" rx="8"/>'
                  '<path d="M30 66 L100 116 L170 66"/>'
                  '<path d="M30 148 L80 106"/><path d="M170 148 L120 106"/>'),
            ouro=(f'<circle cx="100" cy="116" r="20" fill="{CREME}"/>' + concha(100, 115, 26)
                  + '<path d="M20 82 H8"/><path d="M22 100 H2"/><path d="M20 118 H10"/>')),
        "horarios": dict(
            azul=('<path d="M48 108 A52 52 0 0 1 152 108"/>'
                  '<path d="M100 108 V72"/><path d="M100 108 L124 95"/>'
                  '<path d="M28 122 C44 113 60 113 76 122 S108 131 124 122 S156 113 172 121"/>'
                  '<path d="M50 142 C64 135 78 135 92 142 S120 149 134 142 S148 137 154 140"/>'),
            ouro=raios + '<circle cx="100" cy="108" r="4.5" fill="url(#ouro)"/>' + pontos(46, 154, 132, 9, 1.4)),
        "localizacao": dict(
            azul=('<path d="M100 150 C100 150 58 110 58 80 A42 42 0 0 1 142 80 C142 110 100 150 100 150 Z"/>'
                  '<path d="M32 164 C46 156 60 156 74 164 S102 172 116 164 S152 156 168 163"/>'),
            ouro=concha(100, 79, 32) + pontos(44, 156, 178, 9, 1.4)),
        "cuidados": dict(
            azul=('<path d="M100 54 V48 C100 41 109 38 110 31 C111 24 103 20 97 23"/>'
                  '<path d="M100 54 L38 86 Q32 90 39 90 H161 Q168 90 162 86 Z"/>' + cab_a),
            ouro=cab_o + brilho(164, 120, 7) + brilho(36, 134, 5) + brilho(160, 152, 4)),
    }


def moldura():
    """Anel dourado fino, anel de pontinhos e estrelas no topo e na base."""
    s = ['<circle cx="100" cy="100" r="94" fill="none" stroke="url(#ouro)" stroke-width="1.4"/>']
    for k in range(72):
        g = (k * 5) % 360
        if 80 <= g <= 100 or 260 <= g <= 280:
            continue  # espaço para as estrelas
        a = math.radians(g)
        r = 1.5 if k % 2 else 0.9
        s.append(f'<circle cx="{100 + 87*math.cos(a):.2f}" cy="{100 + 87*math.sin(a):.2f}" r="{r}" '
                 'fill="url(#ouro)"/>')
    s.append(f'<circle cx="100" cy="6" r="12" fill="{CREME}"/>')
    s.append(brilho(100, 6, 10))
    s.append(f'<circle cx="100" cy="194" r="7" fill="{CREME}"/>')
    s.append(brilho(100, 194, 5.5))
    return "".join(s)


def capa(partes):
    x0 = W / 2 - 100 * ESCALA
    y0 = H / 2 - 100 * ESCALA
    return "\n".join([
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        '<defs><linearGradient id="ouro" gradientUnits="userSpaceOnUse" x1="20" y1="20" x2="180" y2="180">'
        '<stop offset="0" stop-color="#C9A132"/><stop offset="0.55" stop-color="#A57D2C"/>'
        '<stop offset="1" stop-color="#7A4E1C"/></linearGradient></defs>',
        f'<rect width="{W}" height="{H}" fill="{CREME}"/>',
        f'<g transform="translate({x0} {y0}) scale({ESCALA})">',
        moldura(),
        # ícone reduzido para caber dentro do anel
        '<g transform="translate(100 100) scale(0.72) translate(-100 -100)" fill="none" '
        'stroke-linecap="round" stroke-linejoin="round">',
        f'<g stroke="{AZUL}" stroke-width="6">{partes["azul"]}</g>',
        f'<g stroke="url(#ouro)" stroke-width="3.2">{partes["ouro"]}</g>',
        partes.get("texto", ""),
        "</g></g>",
        "</svg>",
    ])


if __name__ == "__main__":
    pasta = os.path.join(AQUI, "destaques")
    os.makedirs(pasta, exist_ok=True)
    for nome, partes in icones().items():
        svg = capa(partes)
        base = os.path.join(pasta, f"destaque-{nome}")
        open(base + ".svg", "w").write(svg)
        cairosvg.svg2png(bytestring=svg.encode(), write_to=base + ".png")
        print(nome)
