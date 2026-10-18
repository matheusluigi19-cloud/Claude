"""Etiqueta de preço da Madame Solara, frente e verso, em dois modelos (azul e off-white)."""
import os
import re

import cairosvg
import segno

AQUI = os.path.dirname(os.path.abspath(__file__))
URL_QR = "https://scanned.page/B2t1Pd"  # mesmo link do QR da etiqueta original

CREME = "#FCFDF5"
AZUL = "#5598B3"
MARROM = "#5E3416"
OURO = "#8A6420"

W, H = 252, 144  # pontos (8,9 x 5,1 cm), igual à etiqueta original

MODELOS = {
    "azul": dict(fundo=AZUL, logo_cor=CREME, sol_cor=CREME, sol_op=0.45, texto=CREME,
                 destaque=CREME, linha=CREME, cartao_qr=CREME, qr=MARROM),
    "off-white": dict(fundo=CREME, logo_cor=None, sol_cor=None, sol_op=0.75, texto=OURO,
                      destaque=AZUL, linha=OURO, cartao_qr=None, qr=MARROM),
}


def vetor(arquivo, prefixo, cor=None):
    """Conteúdo de um SVG extraído do manual, com ids únicos e cor opcionalmente trocada."""
    s = open(os.path.join(AQUI, arquivo)).read()
    corpo = s[s.index(">", s.index("<svg")) + 1:s.rindex("</svg>")]
    corpo = re.sub(r'id="([^"]+)"', rf'id="{prefixo}-\1"', corpo)
    corpo = re.sub(r'url\(#([^)]+)\)', rf'url(#{prefixo}-\1)', corpo)
    if cor:
        corpo = re.sub(r'fill="(rgb\([^)]*\)|url\(#[^)]+\))"', f'fill="{cor}"', corpo)
    return corpo


def qr(x, y, tamanho, cor):
    m = segno.make(URL_QR, error="m").matrix
    n = len(m)
    p = tamanho / n
    # um único path, para não aparecer emenda entre os módulos
    d = "".join(f"M{x + c*p:.3f},{y + l*p:.3f}h{p:.3f}v{p:.3f}h-{p:.3f}z"
                for l, linha in enumerate(m) for c, v in enumerate(linha) if v)
    return f'<path d="{d}" fill="{cor}" shape-rendering="crispEdges"/>'


def faixas(op):
    s = []
    lw, lh = 34, 17.4
    for y, dx in ((-7, 0), (H - 11, lw * 0.8)):
        x = -lw / 2 + dx
        while x < W:
            s.append(f'<use href="#sol" x="{x:.1f}" y="{y}" width="{lw}" height="{lh}" opacity="{op}"/>')
            x += lw * 1.6
    return "".join(s)


def base(m):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'width="{W}pt" height="{H}pt" viewBox="0 0 {W} {H}">',
            '<defs>',
            f'<g id="logoBruto">{vetor("logo-madame-solara.svg", "lg", m["logo_cor"])}</g>',
            f'<g id="solBruto">{vetor("logo-madame-solara.svg", "sl", m["sol_cor"])}</g>',
            f'<g id="msBruto">{vetor("monograma-ms.svg", "ms", m["logo_cor"])}</g>',
            '<symbol id="logo" viewBox="68 108 129.5 116"><use href="#logoBruto"/></symbol>',
            '<symbol id="sol" viewBox="89 106 86 44"><use href="#solBruto"/></symbol>',
            '<symbol id="ms" viewBox="71 113.5 123.5 105"><use href="#msBruto"/></symbol>',
            '</defs>',
            f'<rect width="{W}" height="{H}" fill="{m["fundo"]}"/>',
            faixas(m["sol_op"])]


def frente(m):
    s = base(m)
    lh = 80
    lw = lh * 129.5 / 116
    s.append(f'<use href="#logo" x="{78 - lw/2:.2f}" y="{72 - lh/2 + 1:.2f}" width="{lw:.2f}" height="{lh}"/>')
    s.append(f'<line x1="156" y1="36" x2="156" y2="108" stroke="{m["linha"]}" stroke-width="0.4" opacity="0.5"/>')
    q, cx, top = 56, 204, 34
    if m["cartao_qr"]:
        s.append(f'<rect x="{cx - q/2 - 5}" y="{top - 5}" width="{q + 10}" height="{q + 10}" rx="5" '
                 f'fill="{m["cartao_qr"]}"/>')
    s.append(qr(cx - q / 2, top, q, m["qr"]))
    s.append(f'<text x="{cx}" y="{top + q + 15}" text-anchor="middle" font-family="Outfit" font-size="4.8" '
             f'letter-spacing="1.3" fill="{m["texto"]}">ESCANEIE E CONHEÇA</text>')
    s.append("</svg>")
    return "\n".join(s)


def verso(m):
    s = base(m)
    mh = 50
    mw = mh * 123.5 / 105
    s.append(f'<use href="#ms" x="{52 - mw/2:.2f}" y="{72 - mh/2:.2f}" width="{mw:.2f}" height="{mh}"/>')
    s.append(f'<line x1="104" y1="36" x2="104" y2="108" stroke="{m["linha"]}" stroke-width="0.4" opacity="0.5"/>')
    cx = 178
    s.append(f'<text x="{cx}" y="44" text-anchor="middle" font-family="Outfit" font-size="5.6" '
             f'letter-spacing="2.6" fill="{m["texto"]}">TAMANHO</text>')
    for k, t in enumerate("PMG"):
        x = cx + (k - 1) * 30
        s.append(f'<circle cx="{x}" cy="64" r="10.5" fill="none" stroke="{m["destaque"]}" stroke-width="0.7"/>')
        s.append(f'<text x="{x}" y="68.2" text-anchor="middle" font-family="Italiana" font-size="12" '
                 f'fill="{m["destaque"]}">{t}</text>')
    s.append(f'<text x="128" y="103" font-family="Italiana" font-size="13" fill="{m["texto"]}">R$</text>')
    s.append(f'<line x1="146" y1="103" x2="228" y2="103" stroke="{m["linha"]}" stroke-width="0.5" opacity="0.7"/>')
    s.append("</svg>")
    return "\n".join(s)


if __name__ == "__main__":
    pasta = os.path.join(AQUI, "etiquetas")
    os.makedirs(pasta, exist_ok=True)
    for nome, m in MODELOS.items():
        paginas = []
        for lado, fn in (("frente", frente), ("verso", verso)):
            svg = fn(m)
            base_arq = os.path.join(pasta, f"etiqueta-{nome}-{lado}")
            open(base_arq + ".svg", "w").write(svg)
            cairosvg.svg2png(bytestring=svg.encode(), write_to=base_arq + ".png", scale=1200 / 72 / 2)
            cairosvg.svg2pdf(bytestring=svg.encode(), write_to=base_arq + ".pdf")
            paginas.append(base_arq + ".pdf")
        print(nome, "ok")
