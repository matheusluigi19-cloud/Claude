"""Cartão de agradecimento da Madame Solara (10 x 15 cm, frente e verso, com 3 mm de sangria)."""
import os

import cairosvg

from PIL import ImageFont

from gerar_etiqueta import vetor

AQUI = os.path.dirname(os.path.abspath(__file__))
CREME = "#FCFDF5"
AZUL = "#64A6C9"
MARROM = "#5E3416"
MARROM_SUAVE = "#7A5A44"
SANGRIA = 3
W, H = 100 + 2 * SANGRIA, 150 + 2 * SANGRIA  # milímetros
CX = W / 2


def base(fundo, logo_cor, sol_cor, sol_op):
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}">',
        "<defs>",
        f'<g id="logoBruto">{vetor("logo-madame-solara.svg", "lg", logo_cor)}</g>',
        f'<g id="solBruto">{vetor("logo-madame-solara.svg", "sl", sol_cor)}</g>',
        '<symbol id="logo" viewBox="68 108 129.5 116"><use href="#logoBruto"/></symbol>',
        '<symbol id="sol" viewBox="89 106 86 44"><use href="#solBruto"/></symbol>',
        '<linearGradient id="ouro" x1="0" x2="1" y1="0" y2="0">'
        '<stop offset="0" stop-color="#8E651E"/><stop offset="0.5" stop-color="#C9A132"/>'
        '<stop offset="1" stop-color="#7A4E1C"/></linearGradient>',
        "</defs>",
        f'<rect width="{W}" height="{H}" fill="{fundo}"/>',
        faixas(sol_op),
    ]


def faixas(op):
    """Sóis desencontrados no alto e na base, como a moldura do manual."""
    s = []
    lw, lh = 22, 11.3
    for y, dx in ((-1.5, 0), (H - 9.5, lw * 0.8)):
        x = -lw / 2 + dx
        while x < W:
            s.append(f'<use href="#sol" x="{x:.2f}" y="{y}" width="{lw}" height="{lh}" opacity="{op}"/>')
            x += lw * 1.6
    return "".join(s)


def brilho(x, y, r, cor):
    k = r * 0.18
    return (f'<path d="M{x},{y-r} Q{x+k},{y-k} {x+r},{y} Q{x+k},{y+k} {x},{y+r} '
            f'Q{x-k},{y+k} {x-r},{y} Q{x-k},{y-k} {x},{y-r} Z" fill="{cor}"/>')


def texto(y, conteudo, tam, cor, fonte="Work Sans", peso=400, espaco=0, ancora="middle"):
    return (f'<text x="{CX}" y="{y}" text-anchor="{ancora}" font-family="{fonte}" font-weight="{peso}" '
            f'font-size="{tam}" letter-spacing="{espaco}" fill="{cor}">{conteudo}</text>')


CONTATOS = [
    ("instagram", "@madamesolara_"),
    ("email", "solaramadame@gmail.com"),
    ("telefone", "(71) 98703-6838"),
]

ICONES = {
    "instagram": '<rect x="0.4" y="0.4" width="4.2" height="4.2" rx="1.2"/><circle cx="2.5" cy="2.5" r="1"/>'
                 '<circle cx="3.65" cy="1.35" r="0.18" fill="{cor}" stroke="none"/>',
    "email": '<rect x="0.3" y="0.9" width="4.4" height="3.2" rx="0.5"/><path d="M0.5 1.2 L2.5 2.8 L4.5 1.2"/>',
    "telefone": '<path d="M1.2 0.5 L2 0.5 L2.4 1.7 L1.8 2.1 Q2.3 3.2 3 3.4 L3.4 2.8 L4.5 3.2 L4.5 4 Q4.4 4.6 3.7 4.6 '
                'Q0.4 4.2 0.5 1.2 Q0.5 0.6 1.2 0.5 Z"/>',
}


def contatos(y0, tam=3.3, passo=6.2):
    """Três linhas de contato com ícone, centradas como um bloco."""
    fonte = ImageFont.truetype(os.path.expanduser("~/.fonts/WorkSans-Regular.ttf"), 1000)
    largura = max(fonte.getlength(t) for _, t in CONTATOS) / 1000 * tam
    icone, vao = 4.6, 2.6
    x0 = CX - (icone + vao + largura) / 2
    s = []
    for k, (tipo, valor) in enumerate(CONTATOS):
        y = y0 + k * passo
        s.append(f'<g transform="translate({x0:.2f} {y - 3.6:.2f}) scale(0.92)" fill="none" stroke="#A57D2C" '
                 f'stroke-width="0.35" stroke-linecap="round" stroke-linejoin="round">'
                 f'{ICONES[tipo].replace("{cor}", "#A57D2C")}</g>')
        s.append(f'<text x="{x0 + icone + vao:.2f}" y="{y}" font-family="Work Sans" font-size="{tam}" '
                 f'fill="{MARROM}">{valor}</text>')
    return "".join(s)


def frente():
    s = base(AZUL, CREME, CREME, 0.5)
    lw = 62
    lh = lw * 116 / 129.5
    s.append(f'<use href="#logo" x="{CX - lw/2:.2f}" y="{H/2 - lh/2 - 2:.2f}" width="{lw}" height="{lh:.2f}"/>')
    s.append("</svg>")
    return "\n".join(s)


def verso():
    s = base(CREME, None, None, 0.8)
    s.append(texto(40, "Obrigada!", 15, "url(#ouro)", "Italiana", espaco=0.4))
    s.append(brilho(CX, 47.5, 1.8, "#A57D2C"))
    s.append(f'<line x1="{CX - 22}" y1="47.5" x2="{CX - 4.5}" y2="47.5" stroke="#A57D2C" stroke-width="0.2" opacity="0.6"/>')
    s.append(f'<line x1="{CX + 4.5}" y1="47.5" x2="{CX + 22}" y2="47.5" stroke="#A57D2C" stroke-width="0.2" opacity="0.6"/>')
    linhas = [
        "Que alegria ter você com a gente.",
        "Sua peça foi escolhida e embalada",
        "com todo o carinho para acompanhar",
        "os seus dias de sol.",
    ]
    for k, linha in enumerate(linhas):
        s.append(texto(58 + k * 5.2, linha, 3.5, MARROM))
    s.append(texto(85, "Você é o seu padrão!", 6.2, AZUL.replace("#64A6C9", "#4E8FB0"), "Italiana", espaco=0.2))
    cuidado = ["Antes do primeiro uso, lave a peça à mão com", "sabão neutro e água fria, e seque na sombra."]
    for k, linha in enumerate(cuidado):
        s.append(texto(95 + k * 4.3, linha, 2.7, MARROM_SUAVE))
    s.append(contatos(119))
    s.append("</svg>")
    return "\n".join(s)


if __name__ == "__main__":
    pasta = os.path.join(AQUI, "cartao-agradecimento")
    os.makedirs(pasta, exist_ok=True)
    pdfs = []
    for lado, fn in (("frente", frente), ("verso", verso)):
        svg = fn()
        base_arq = os.path.join(pasta, f"cartao-{lado}")
        open(base_arq + ".svg", "w").write(svg)
        # PNG para ver no celular: cortado no tamanho final (sem a sangria)
        png = cairosvg.svg2png(bytestring=svg.encode(), output_width=round(W / 25.4 * 300))
        from io import BytesIO
        from PIL import Image
        im = Image.open(BytesIO(png))
        px = im.width / W
        im.crop((round(SANGRIA * px), round(SANGRIA * px), round((W - SANGRIA) * px), round((H - SANGRIA) * px))).save(base_arq + ".png")
        cairosvg.svg2pdf(bytestring=svg.encode(), write_to=base_arq + ".pdf")
        pdfs.append(base_arq + ".pdf")
    print("\n".join(pdfs))
