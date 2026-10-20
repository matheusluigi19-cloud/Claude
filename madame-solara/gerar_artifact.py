"""Junta o protótipo da loja num arquivo único para publicar como página do claude.ai.

O site em site/ continua sendo a fonte: este script lê as quatro páginas, guarda o conteúdo de cada
uma num <template>, embute CSS, JS e imagens, e troca as fontes locais pelo Google Fonts
(a página publicada só aceita fontes de lá ou embutidas).
"""
import base64
import json
import os
import re

AQUI = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(AQUI, "site")
SAIDA = os.path.join(AQUI, "loja-madame-solara.html")

PAGINAS = {"inicio": "index.html", "colecao": "colecao.html", "produto": "produto.html", "checkout": "checkout.html"}
FONTES = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
          '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
          '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Italiana'
          '&family=Work+Sans:ital,wght@0,400;0,700;1,400&display=swap">')


def ler(nome):
    with open(os.path.join(SITE, nome), encoding="utf-8") as f:
        return f.read()


def data_uri(caminho):
    tipo = {"svg": "image/svg+xml", "jpg": "image/jpeg", "png": "image/png"}[caminho.rsplit(".", 1)[1]]
    with open(os.path.join(SITE, caminho), "rb") as f:
        return f"data:{tipo};base64," + base64.b64encode(f.read()).decode()


def main_de(html):
    m = re.search(r'<main id="conteudo"( class="([^"]*)")?>(.*)</main>', html, re.S)
    return (m.group(2) or ""), m.group(3)


def montar():
    css = ler("estilo.css")
    css = re.sub(r"@font-face \{[^}]*\}\n", "", css)
    telas, classes, titulos = [], {}, {}
    for nome, arquivo in PAGINAS.items():
        html = ler(arquivo)
        classes[nome], corpo = main_de(html)
        titulos[nome] = re.search(r"<title>(.*?)</title>", html).group(1).replace("&amp;", "&")
        telas.append(f'<template id="tela-{nome}">{corpo}</template>')
    js = ler("produtos.js") + "\n" + ler("loja.js")
    spa = "window.MS_SPA = " + json.dumps({"params": None, "classes": classes, "titulos": titulos}, ensure_ascii=False) + ";"
    pagina = "\n".join([
        "<title>Loja Madame Solara</title>",
        '<meta name="description" content="Protótipo da loja virtual Madame Solara.">',
        FONTES,
        f"<style>{css}</style>",
        '<main id="conteudo"></main>',
        *telas,
        f"<script>{spa}</script>",
        f"<script>{js}</script>",
    ])
    # o corpo precisa do data-pagina antes do script rodar
    pagina = pagina.replace("<script>window.MS_SPA", '<script>document.body.dataset.pagina = "inicio";\nwindow.MS_SPA', 1)
    for arquivo in sorted(set(re.findall(r"assets/[\w.-]+\.(?:svg|jpg|png)", pagina))):
        pagina = pagina.replace(arquivo, data_uri(arquivo))
    with open(SAIDA, "w", encoding="utf-8") as f:
        f.write(pagina)
    print(SAIDA, f"{os.path.getsize(SAIDA) / 1e6:.2f} MB")


if __name__ == "__main__":
    montar()
