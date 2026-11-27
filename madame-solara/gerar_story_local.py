"""Story de localização e horário da loja, no mesmo estilo do card de cuidados.

Formato de story (1080x1920). O conteúdo fica entre y 250 e 1670, fora das áreas que o
Instagram cobre com o nome do perfil e a caixa de resposta. Sobra um espaço livre acima da
assinatura para colar a figurinha de localização do próprio Instagram.
"""
import os

import cairosvg

import gerar_card as base
from gerar_card import AZUL, CREME, MARROM, OURO, brilho, logo_bruto

AQUI = os.path.dirname(os.path.abspath(__file__))
W, H = 1080, 1920
MARGEM = 150

GRUPOS = [
    ("ENDEREÇO", [
        ["Dentro da loja Madame Dress"],
        ["Estrada do Coqueiro Grande", "Fazenda Grande II, Salvador - BA"],
        ["CEP 41342-315"],
    ]),
    ("HORÁRIO DE FUNCIONAMENTO", [
        ["Segunda a sábado, das 9h às 18h"],
        ["Domingo, das 9h às 13h"],
    ]),
]


def story():
    base.W, base.H = W, H          # a faixa de sóis usa a largura e a altura do quadro
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
         base.faixa_de_sois(-34, False),
         base.faixa_de_sois(H - 42, True)]

    # logo
    lw = 250
    lh = lw * 116 / 129.5
    y0 = 260
    s.append(f'<use href="#logo" x="{(W-lw)/2:.1f}" y="{y0}" width="{lw}" height="{lh:.1f}"/>')

    # título
    y = y0 + lh + 140
    s.append(f'<text x="{W/2}" y="{y:.0f}" text-anchor="middle" font-family="Italiana" font-size="96" '
             f'letter-spacing="9" fill="url(#ouro)">ONDE ESTAMOS</text>')
    y += 54
    s.append(f'<text x="{W/2}" y="{y:.0f}" text-anchor="middle" font-family="Outfit" font-size="24" '
             f'letter-spacing="9" fill="{AZUL}">LOCALIZAÇÃO E HORÁRIOS</text>')
    y += 50
    s.append(brilho(W / 2, y, 9, OURO))
    s.append(f'<line x1="{W/2-150}" y1="{y}" x2="{W/2-26}" y2="{y}" stroke="{OURO}" stroke-width="1" opacity="0.6"/>')
    s.append(f'<line x1="{W/2+26}" y1="{y}" x2="{W/2+150}" y2="{y}" stroke="{OURO}" stroke-width="1" opacity="0.6"/>')

    # grupos
    y += 96
    xt = MARGEM + 38
    for titulo, itens in GRUPOS:
        s.append(f'<text x="{MARGEM}" y="{y:.0f}" font-family="Outfit" font-size="21" letter-spacing="7" '
                 f'fill="{OURO}">{titulo}</text>')
        s.append(f'<line x1="{MARGEM}" y1="{y+18:.0f}" x2="{W-MARGEM}" y2="{y+18:.0f}" stroke="{OURO}" '
                 f'stroke-width="0.8" opacity="0.35"/>')
        y += 64
        for linhas in itens:
            s.append(brilho(MARGEM + 10, y - 10, 8, AZUL))
            for k, linha in enumerate(linhas):
                s.append(f'<text x="{xt}" y="{y + k*44:.0f}" font-family="Outfit" font-size="32" '
                         f'fill="{MARROM}">{linha}</text>')
            y += 44 * len(linhas) + 10
        y += 40

    # assinatura
    s.append(f'<text x="{W/2}" y="{H-205}" text-anchor="middle" font-family="Italiana" font-size="50" '
             f'letter-spacing="4" fill="url(#ouro)">VOCÊ É O SEU PADRÃO!</text>')
    s.append("</svg>")
    return "\n".join(s), y


if __name__ == "__main__":
    svg, fim = story()
    print("fim do conteúdo em y =", round(fim))
    pasta = os.path.join(AQUI, "stories"); os.makedirs(pasta, exist_ok=True)
    saida = os.path.join(pasta, "story-localizacao-horario")
    open(saida + ".svg", "w").write(svg)
    cairosvg.svg2png(bytestring=svg.encode(), write_to=saida + ".png", scale=2)
