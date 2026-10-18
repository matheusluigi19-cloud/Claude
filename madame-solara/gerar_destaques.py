"""Capas dos destaques do Instagram da Madame Solara: fundo azul da marca e ícone branco."""
import math
import os

import cairosvg

AQUI = os.path.dirname(os.path.abspath(__file__))
FUNDO = "#64A6C9"   # azul de fundo das páginas do manual
BRANCO = "#FCFDF5"  # branco usado no logo sobre o azul
W, H = 1080, 1920   # formato de story; o Instagram recorta o círculo do centro
ESCALA = 2.7        # grade de 200 -> 540 px, metade do círculo do destaque
TRACO = 7.5


def arco_seta(cx, cy, r, a0, a1):
    """Arco no sentido horário com ponta de seta no fim."""
    rad = math.radians
    x0, y0 = cx + r * math.cos(rad(a0)), cy + r * math.sin(rad(a0))
    x1, y1 = cx + r * math.cos(rad(a1)), cy + r * math.sin(rad(a1))
    tx, ty = -math.sin(rad(a1)), math.cos(rad(a1))
    nx, ny = math.cos(rad(a1)), math.sin(rad(a1))
    L = 13
    h1 = (x1 - tx * L + nx * L * 0.8, y1 - ty * L + ny * L * 0.8)
    h2 = (x1 - tx * L - nx * L * 0.8, y1 - ty * L - ny * L * 0.8)
    return (f'<path d="M{x0:.1f} {y0:.1f} A{r} {r} 0 0 1 {x1:.1f} {y1:.1f}"/>'
            f'<path d="M{h1[0]:.1f} {h1[1]:.1f} L{x1:.1f} {y1:.1f} L{h2[0]:.1f} {h2[1]:.1f}"/>')


# Ícones numa grade de 200 x 200, um símbolo só em cada, sem enfeite
ICONES = {
    "trocas": arco_seta(100, 100, 60, 200, 330) + arco_seta(100, 100, 60, 20, 150),
    "pagamentos": ('<rect x="36" y="58" width="128" height="86" rx="12"/>'
                   '<path d="M36 84 H164"/><path d="M58 120 H92"/>'),
    "envios": ('<path d="M100 42 L158 70 L100 98 L42 70 Z"/>'
               '<path d="M42 70 V132 L100 160 L158 132 V70"/><path d="M100 98 V160"/>'
               '<path d="M71 56 L129 84"/>'),
    "horarios": ('<circle cx="100" cy="100" r="62"/>'
                 '<path d="M100 100 V66"/><path d="M100 100 L124 114"/>'),
    "localizacao": ('<path d="M100 164 C100 164 56 118 56 84 A44 44 0 0 1 144 84 C144 118 100 164 100 164 Z"/>'
                    '<circle cx="100" cy="84" r="16"/>'),
    "cuidados": ('<path d="M70 62 C64 86 54 106 44 126 C62 136 86 133 97 121 C90 100 81 80 70 62 Z"/>'
                 '<path d="M130 62 C136 86 146 106 156 126 C138 136 114 133 103 121 C110 100 119 80 130 62 Z"/>'
                 '<path d="M70 62 C74 50 80 42 88 34"/><path d="M130 62 C126 50 120 42 112 34"/>'
                 '<path d="M44 126 C36 126 28 123 20 118"/><path d="M156 126 C164 126 172 123 180 118"/>'
                 '<circle cx="100" cy="121" r="4"/>'),
}


def capa(desenho):
    x0 = W / 2 - 100 * ESCALA
    y0 = H / 2 - 100 * ESCALA
    return "\n".join([
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        f'<rect width="{W}" height="{H}" fill="{FUNDO}"/>',
        f'<g transform="translate({x0} {y0}) scale({ESCALA})" fill="none" stroke="{BRANCO}" '
        f'stroke-width="{TRACO}" stroke-linecap="round" stroke-linejoin="round">',
        desenho,
        "</g>",
        "</svg>",
    ])


if __name__ == "__main__":
    pasta = os.path.join(AQUI, "destaques")
    os.makedirs(pasta, exist_ok=True)
    for nome, desenho in ICONES.items():
        svg = capa(desenho)
        base = os.path.join(pasta, f"destaque-{nome}")
        open(base + ".svg", "w").write(svg)
        cairosvg.svg2png(bytestring=svg.encode(), write_to=base + ".png")
        print(nome)
