"""Capas dos destaques do Instagram da Madame Solara, com ícones de traço fino."""
import os

import cairosvg

AQUI = os.path.dirname(os.path.abspath(__file__))
CREME = "#FCFDF5"
AZUL = "#5598B3"
W, H = 1080, 1920  # formato de story; o Instagram recorta o círculo do centro

# Ícones desenhados numa grade de 200 x 200
ICONES = {
    "trocas": """
        <path d="M45 78 H155"/><path d="M135 58 L155 78 L135 98"/>
        <path d="M155 122 H45"/><path d="M65 102 L45 122 L65 142"/>""",
    "pagamentos": """
        <rect x="32" y="55" width="136" height="92" rx="12"/>
        <path d="M32 82 H168"/><path d="M54 122 H88"/><path d="M102 122 H118"/>""",
    "envios": """
        <rect x="24" y="66" width="96" height="64" rx="6"/>
        <path d="M120 86 H149 L174 110 V130 H120 Z"/>
        <path d="M130 94 H146 L160 108 H130 Z"/>
        <circle cx="56" cy="140" r="13" fill="{fundo}"/><circle cx="146" cy="140" r="13" fill="{fundo}"/>""",
    "horarios": """
        <circle cx="100" cy="102" r="62"/>
        <path d="M100 102 V68"/><path d="M100 102 L124 116"/>
        <path d="M100 48 V55"/><path d="M154 102 H147"/><path d="M100 156 V149"/><path d="M46 102 H53"/>
        <circle cx="100" cy="102" r="3.5" fill="{traco}"/>""",
    "localizacao": """
        <path d="M100 168 C100 168 52 118 52 86 A48 48 0 0 1 148 86 C148 118 100 168 100 168 Z"/>
        <circle cx="100" cy="86" r="17"/>""",
    "cuidados": """
        <path d="M100 30 C100 30 52 90 52 122 A48 48 0 0 0 148 122 C148 90 100 30 100 30 Z"/>
        <path d="M70 128 C80 119 90 119 100 128 S120 137 130 128"/>""",
}


def brilho(x, y, r):
    k = r * 0.18
    return (f'<path d="M{x},{y-r} Q{x+k},{y-k} {x+r},{y} Q{x+k},{y+k} {x},{y+r} '
            f'Q{x-k},{y+k} {x-r},{y} Q{x-k},{y-k} {x},{y-r} Z" fill="url(#ouro)" stroke="none"/>')


def capa(nome):
    escala = 2.7  # ícone de 540 px, metade do círculo do destaque
    x0 = W / 2 - 100 * escala
    y0 = H / 2 - 100 * escala
    corpo = ICONES[nome].replace("{fundo}", CREME).replace("{traco}", AZUL)
    return "\n".join([
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        '<defs><linearGradient id="ouro" x1="0" x2="1" y1="0" y2="1">'
        '<stop offset="0" stop-color="#C9A132"/><stop offset="1" stop-color="#7A4E1C"/></linearGradient></defs>',
        f'<rect width="{W}" height="{H}" fill="{CREME}"/>',
        f'<g transform="translate({x0} {y0}) scale({escala})" fill="none" stroke="{AZUL}" '
        f'stroke-width="7" stroke-linecap="round" stroke-linejoin="round">',
        corpo,
        brilho(176, 30, 11),
        "</g>",
        "</svg>",
    ])


if __name__ == "__main__":
    pasta = os.path.join(AQUI, "destaques")
    os.makedirs(pasta, exist_ok=True)
    for nome in ICONES:
        svg = capa(nome)
        base = os.path.join(pasta, f"destaque-{nome}")
        open(base + ".svg", "w").write(svg)
        cairosvg.svg2png(bytestring=svg.encode(), write_to=base + ".png")
        print(nome)
