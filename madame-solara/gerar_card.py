"""Card de cuidados com o biquíni na identidade visual da Madame Solara."""
import os
import re

import cairosvg

AQUI = os.path.dirname(os.path.abspath(__file__))

CREME = "#FCFDF5"
AZUL = "#5598B3"
MARROM = "#5E3416"
OURO = "#8A6420"  # dourado escuro para texto pequeno sobre o creme

W, H = 1080, 1620
MARGEM = 150

GRUPOS = [
    ("AO LAVAR", [
        ["Lave antes do primeiro uso."],
        ["Lave à mão, com sabão neutro ou", "detergente líquido e água fria."],
    ]),
    ("AO SECAR", [
        ["Não torça."],
        ["Seque à sombra."],
        ["Não use prendedor."],
    ]),
    ("NUNCA", [
        ["Passar a ferro."],
        ["Usar alvejante."],
        ["Lavar na máquina ou no tanquinho."],
        ["Lavar a seco."],
        ["Deixar de molho ou guardar úmido", "em saco plástico."],
    ]),
]


def logo_bruto():
    """Conteúdo vetorial do logo original, sem o fundo, com ids prefixados."""
    s = open(os.path.join(AQUI, "logo-madame-solara.svg")).read()
    corpo = s[s.index(">", s.index("<svg")) + 1:s.rindex("</svg>")]
    corpo = re.sub(r'id="([^"]+)"', r'id="ms-\1"', corpo)
    corpo = re.sub(r'url\(#([^)]+)\)', r'url(#ms-\1)', corpo)
    return corpo


def brilho(x, y, r, cor):
    # estrela de quatro pontas do logo
    k = r * 0.18
    return (f'<path d="M{x},{y-r} Q{x+k},{y-k} {x+r},{y} Q{x+k},{y+k} {x},{y+r} '
            f'Q{x-k},{y+k} {x-r},{y} Q{x-k},{y-k} {x},{y-r} Z" fill="{cor}"/>')


def faixa_de_sois(y0, espelhar):
    """Duas fileiras desencontradas de sóis, como na moldura do manual."""
    s = []
    lw, lh = 150, 75
    for fila, (dy, dx) in enumerate(((0, -lw / 2), (52, 0))):
        x = dx
        while x < W:
            y = y0 + (dy if not espelhar else -dy)
            s.append(f'<use href="#sol" x="{x:.1f}" y="{y:.1f}" width="{lw}" height="{lh}" '
                     f'opacity="{0.55 if fila == 0 else 0.9}"/>')
            x += lw * 1.55
    return "\n".join(s)


def card():
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
         f'width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
         '<defs>',
         f'<g id="logoBruto">{logo_bruto()}</g>',
         '<symbol id="logo" viewBox="68 108 129.5 116"><use href="#logoBruto"/></symbol>',
         '<symbol id="sol" viewBox="89 106 86 44"><use href="#logoBruto"/></symbol>',
         '<linearGradient id="ouro" x1="0" x2="1" y1="0" y2="0">'
         '<stop offset="0" stop-color="#8E651E"/><stop offset="0.5" stop-color="#C9A132"/>'
         '<stop offset="1" stop-color="#7A4E1C"/></linearGradient>',
         '</defs>',
         f'<rect width="{W}" height="{H}" fill="{CREME}"/>',
         faixa_de_sois(-34, False),
         faixa_de_sois(H - 42, True)]

    # logo
    lw = 220
    lh = lw * 116 / 129.5
    s.append(f'<use href="#logo" x="{(W-lw)/2:.1f}" y="140" width="{lw}" height="{lh:.1f}"/>')

    # título
    y = 140 + lh + 136
    s.append(f'<text x="{W/2}" y="{y:.0f}" text-anchor="middle" font-family="Italiana" font-size="104" '
             f'letter-spacing="10" fill="url(#ouro)">CUIDADOS</text>')
    y += 50
    s.append(f'<text x="{W/2}" y="{y:.0f}" text-anchor="middle" font-family="Outfit" font-size="22" '
             f'letter-spacing="9" fill="{AZUL}">COM O SEU BIQUÍNI</text>')
    y += 46
    s.append(brilho(W / 2, y, 9, OURO))
    s.append(f'<line x1="{W/2-150}" y1="{y}" x2="{W/2-26}" y2="{y}" stroke="{OURO}" stroke-width="1" opacity="0.6"/>')
    s.append(f'<line x1="{W/2+26}" y1="{y}" x2="{W/2+150}" y2="{y}" stroke="{OURO}" stroke-width="1" opacity="0.6"/>')

    # grupos
    y += 70
    xt = MARGEM + 34
    for titulo, itens in GRUPOS:
        s.append(f'<text x="{MARGEM}" y="{y:.0f}" font-family="Outfit" font-size="19" letter-spacing="7" '
                 f'fill="{OURO}">{titulo}</text>')
        s.append(f'<line x1="{MARGEM}" y1="{y+16:.0f}" x2="{W-MARGEM}" y2="{y+16:.0f}" stroke="{OURO}" '
                 f'stroke-width="0.8" opacity="0.35"/>')
        y += 54
        for linhas in itens:
            s.append(brilho(MARGEM + 9, y - 9, 7, AZUL))
            for k, linha in enumerate(linhas):
                s.append(f'<text x="{xt}" y="{y + k*38:.0f}" font-family="Outfit" font-size="28" '
                         f'fill="{MARROM}">{linha}</text>')
            y += 38 * len(linhas) + 5
        y += 26

    # nota neon
    y += 6
    s.append(f'<text x="{W/2}" y="{y:.0f}" text-anchor="middle" font-family="Outfit" font-size="22" '
             f'letter-spacing="2" fill="{AZUL}">Peças neon pedem cuidado redobrado.</text>')

    # assinatura
    s.append(f'<text x="{W/2}" y="{H-150}" text-anchor="middle" font-family="Italiana" font-size="46" '
             f'letter-spacing="4" fill="url(#ouro)">VOCÊ É O SEU PADRÃO!</text>')
    s.append("</svg>")
    return "\n".join(s), y


if __name__ == "__main__":
    svg, fim = card()
    print("fim do conteúdo em y =", round(fim))
    base = os.path.join(AQUI, "card-cuidados-biquini")
    open(base + ".svg", "w").write(svg)
    cairosvg.svg2png(bytestring=svg.encode(), write_to=base + ".png", scale=1)
    cairosvg.svg2pdf(bytestring=svg.encode(), write_to=base + ".pdf")
