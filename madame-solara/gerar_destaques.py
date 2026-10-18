"""Capas dos destaques do Instagram da Madame Solara, com ícones de traço fino."""
import os

import cairosvg

AQUI = os.path.dirname(os.path.abspath(__file__))
CREME = "#FCFDF5"
AZUL = "#5598B3"
W, H = 1080, 1920  # formato de story; o Instagram recorta o círculo do centro

# Ícones desenhados numa grade de 200 x 200, todos com elementos de moda praia
ICONES = {
    "trocas": """
        <path d="M66 82 Q62 104 72 118 Q86 123 97 113 Q86 97 66 82 Z"/>
        <path d="M134 82 Q138 104 128 118 Q114 123 103 113 Q114 97 134 82 Z"/>
        <path d="M66 82 C72 70 82 62 90 56"/><path d="M134 82 C128 70 118 62 110 56"/>
        <path d="M72 118 Q58 121 46 116"/><path d="M128 118 Q142 121 154 116"/>
        <circle cx="100" cy="113" r="2.4" fill="{traco}" stroke="none"/><path d="M32.3 75.4 A72 72 0 0 1 162.4 64.0"/><path d="M163.3 53.1 L162.4 64.0 L152.4 59.4"/><path d="M167.7 124.6 A72 72 0 0 1 37.6 136.0"/><path d="M36.7 146.9 L37.6 136.0 L47.6 140.6"/>""",
    "pagamentos": """
        <path d="M52 82 H148 L141 160 Q140 166 134 166 H66 Q60 166 59 160 Z"/>
        <path d="M80 82 V72 C80 42 120 42 120 72 V82"/>
        <path d="M56 104 C68 98 78 98 90 104 S112 110 124 104 S138 99 145 103"/>
        <text x="100" y="151" text-anchor="middle" font-family="Italiana" font-size="36"
              fill="{traco}" stroke="none">R$</text>""",
    "envios": """
        <rect x="36" y="62" width="128" height="88" rx="6"/>
        <path d="M36 68 L100 112 L164 68"/>
        <path d="M100 130 C88 124 82 114 84 104 C92 94 108 94 116 104 C118 114 112 124 100 130 Z" fill="{fundo}"/>
        <path d="M100 130 L92 100"/><path d="M100 130 L100 97"/><path d="M100 130 L108 100"/>""",
    "horarios": """
        <path d="M50 112 A50 50 0 0 1 150 112"/><path d="M40.1 96.0 L26.6 92.3"/><path d="M56.2 68.2 L46.3 58.3"/><path d="M84.0 52.1 L80.3 38.6"/><path d="M116.0 52.1 L119.7 38.6"/><path d="M143.8 68.2 L153.7 58.3"/><path d="M159.9 96.0 L173.4 92.3"/>
        <path d="M100 112 V82"/><path d="M100 112 L120 101"/>
        <path d="M38 126 C53 118 68 118 83 126 S113 134 128 126 S152 119 162 125"/>
        <path d="M62 142 C74 136 86 136 98 142 S122 148 138 142"/>""",
    "localizacao": """
        <path d="M100 148 C100 148 64 112 64 84 A36 36 0 0 1 136 84 C136 112 100 148 100 148 Z"/>
        <circle cx="100" cy="84" r="12"/>
        <path d="M44 166 C57 159 70 159 83 166 S109 173 122 166 S146 159 156 165"/>""",
    "cuidados": """
        <path d="M100 58 V52 C100 45 109 42 110 35 C111 28 103 24 97 27"/>
        <path d="M100 58 L46 84 Q40 88 47 88 H153 Q160 88 154 84 Z"/>
        <path d="M71 88 L75 104"/><path d="M129 88 L125 104"/>
        <path d="M75 104 Q67 128 77 143 Q90 147 98 136 Q90 118 75 104 Z"/>
        <path d="M125 104 Q133 128 123 143 Q110 147 102 136 Q110 118 125 104 Z"/>
        <circle cx="100" cy="136" r="2.4" fill="{traco}" stroke="none"/>""",
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
        f'stroke-width="4" stroke-linecap="round" stroke-linejoin="round">',
        corpo,
        brilho(176, 30, 8),
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
