"""Monta o vídeo de lançamento da Madame Solara.

O visual segue o vídeo modelo enviado pela cliente: um título compacto no centro, com uma
etiqueta pequena sem serifa, uma palavra grande em letra cursiva e uma ou duas linhas
digitadas letra a letra, na mesma fonte da etiqueta.

Gera, a partir dos textos e tempos abaixo:
  - compositions/texto.html  (cada letra digitada é um <span> com o instante em que aparece)
  - assets/sfx/digitacao.wav (uma tecla por letra, no mesmo instante)

Há uma variante por trilha, porque as trocas de tela caem nas batidas de cada música.
Para trocar a data ou uma frase, edite os textos e rode de novo com o nome da variante:
  python montar.py every-24th-of-august
Ele também aponta o index.html para a trilha da variante.
Precisa de numpy e soundfile.
"""
import html
import json
import random
import re
import sys
from pathlib import Path

import numpy as np
import soundfile as sf

AQUI = Path(__file__).parent
DURACAO = 16.8          # segundos
SR = 48000

# ----- Variantes: os instantes vêm das batidas medidas em cada trecho de música -----
# corte1 e corte2 são as trocas de tela; os demais são o início de cada linha digitada.
VARIANTES = {
    # "Every 24th of August", 112 bpm, trecho a partir de 76,34 s da faixa.
    "every-24th-of-august": {"corte1": 4.415, "corte2": 10.963, "data": 1.141, "oficial": 5.507,
                             "resumo": 12.055, "assinatura": 13.703},
    # "Oh Barcelona", 123 bpm, trecho a partir de 111,06 s da faixa.
    "oh-barcelona": {"corte1": 5.019, "corte2": 10.963, "data": 1.048, "oficial": 5.994,
                     "resumo": 11.962, "assinatura": 13.936},
}
NOME = sys.argv[1] if len(sys.argv) > 1 else "every-24th-of-august"
V = VARIANTES[NOME]

# ----- Textos (é aqui que se troca a data) ----------------------------------
# Cada tela tem uma etiqueta, uma palavra cursiva e linhas digitadas: (texto, início, segundos por letra).
# Início None quer dizer "logo depois da linha anterior".
TELAS = [
    {"id": "t1", "inicio": 0.0, "fim": V["corte1"],
     "etiqueta": "anota aí:", "cursiva": "Sábado",
     "digitado": [("28 de novembro", V["data"], 0.09)]},
    {"id": "t2", "inicio": V["corte1"], "fim": V["corte2"],
     "etiqueta": "é dia de:", "etiqueta_no_centro": True, "cursiva": "Lançamento",
     "digitado": [("oficial da marca", V["oficial"], 0.085), ("na loja da Madame Dress", None, 0.072)]},
]
T_LOGO = V["corte2"]
RESUMO = {"texto": "sábado · 28.11", "inicio": V["resumo"], "fim": round(V["resumo"] + 1.0, 3)}
ASSINATURA = {"texto": "você é o seu padrão!", "inicio": V["assinatura"], "fim": round(V["assinatura"] + 1.2, 3)}
PASSO = 0.09            # segundos por letra, em média
TROCA = 0.35            # duração da passagem entre telas

rng = random.Random(28_11)


def tempos(texto, inicio, passo, fim=None):
    """Instante de cada caractere: ritmo irregular como digitação de verdade."""
    t, saida = inicio, []
    for ch in texto:
        saida.append(t)
        t += passo * rng.uniform(0.78, 1.25) * (1.5 if ch == " " else 1.0)
    if fim is not None and len(saida) > 1:   # estica para a última letra cair em `fim`
        k = (fim - inicio) / (saida[-1] - inicio)
        saida = [inicio + (x - inicio) * k for x in saida]
    return [round(x, 3) for x in saida]


def letras(texto, ts):
    return "".join(
        f'<span class="k" data-t="{t}">{"&nbsp;" if ch == " " else html.escape(ch)}</span>'
        for ch, t in zip(texto, ts)
    )


eventos = []          # (instante, força em dB, é espaço) para a faixa de teclado
blocos, animacoes = [], []
for tela in TELAS:
    i = tela["id"]
    linhas = []
    for n_linha, (texto, t0, passo) in enumerate(tela["digitado"], start=1):
        if t0 is None:
            t0 = round(linhas[-1][2][-1] + 0.25, 3)
        ts = tempos(texto, t0, passo)
        for ch, t in zip(texto, ts):
            eventos.append((t, -13.0, ch == " "))
        linhas.append((f"{i}-digitado{n_linha}", texto, ts))
    eventos.append((tela["inicio"] + 0.02, -12.0, False))                       # a etiqueta entra com uma tecla
    n = len(tela["cursiva"])
    for k in range(n):                                                           # a cursiva: teclas rápidas e baixas
        eventos.append((tela["inicio"] + 0.1 + k * 0.6 / n, -18.0, False))
    blocos.append(f"""
    <div class="titulo" id="{i}">
      <div class="caixa" id="{i}-caixa">
        <div class="etiqueta{" no-centro" if tela.get("etiqueta_no_centro") else ""}" id="{i}-etiqueta">{html.escape(tela["etiqueta"])}</div>
        <div class="cursiva-janela" id="{i}-janela"><span class="cursiva" id="{i}-cursiva">{html.escape(tela["cursiva"])}</span></div>
        <div class="digitado" data-layout-allow-overflow>{"".join(f'<div id="{lid}">{letras(texto, ts)}</div>' for lid, texto, ts in linhas)}</div>
      </div>
    </div>""")
    entrada = tela["inicio"]
    animacoes.append(f"""
      // Tela "{tela["cursiva"]}": entra em {entrada} s e sai numa passagem suave até {tela["fim"]} s.
      tl.fromTo("#{i}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.01 }}, {entrada});
      tl.fromTo("#{i}-etiqueta", {{ opacity: 0, scale: 0.7 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }}, {entrada});
      tl.fromTo("#{i}-janela", {{ clipPath: "inset(-30% 100% -30% -12%)" }}, {{ clipPath: "inset(-30% -12% -30% -12%)", duration: 0.8, ease: "power2.out" }}, {round(entrada + 0.08, 3)});
      {" ".join(f'digitar("{lid}");' for lid, _, _ in linhas)}
      tl.fromTo("#{i}-caixa", {{ opacity: 1, filter: "blur(0px)" }}, {{ opacity: 0, filter: "blur(10px)", duration: {TROCA}, ease: "power2.in" }}, {round(tela["fim"] - TROCA, 3)});
      tl.set("#{i}", {{ opacity: 0 }}, {tela["fim"]});""")

ts_resumo = tempos(RESUMO["texto"], RESUMO["inicio"], PASSO, fim=RESUMO["fim"])
ts_assin = tempos(ASSINATURA["texto"], ASSINATURA["inicio"], PASSO, fim=ASSINATURA["fim"])
for texto, ts in ((RESUMO["texto"], ts_resumo), (ASSINATURA["texto"], ts_assin)):
    for ch, t in zip(texto, ts):
        eventos.append((t, -13.0, ch == " "))

TEXTO_HTML = f"""<template>
  <style>
    @font-face {{
      font-family: "Imperial Script";
      src: url("assets/fonts/imperial-script-latin-400-normal.woff2") format("woff2");
      font-weight: 400;
      font-style: normal;
    }}
    @font-face {{
      font-family: "Montserrat";
      src: url("assets/fonts/montserrat-latin-700-normal.woff2") format("woff2");
      font-weight: 700;
      font-style: normal;
    }}
    #root {{
      position: absolute;
      inset: 0;
      overflow: hidden;
    }}
    /* Título no estilo do modelo: etiqueta pequena, palavra cursiva grande e linha digitada.
       O conjunto fica no meio do quadro. */
    .titulo {{
      position: absolute;
      left: 0;
      top: 800px;
      width: 1080px;
      display: flex;
      justify-content: center;
      opacity: 0;
    }}
    .caixa {{
      position: relative;
      display: inline-block;
    }}
    .cursiva-janela {{
      display: block;
    }}
    .cursiva {{
      display: block;
      padding: 0 24px;
      font-family: "Imperial Script", cursive;
      font-size: 218px;
      line-height: 260px;
      white-space: nowrap;
      color: #fcfdf5;
      text-shadow: 0 0 22px rgba(255, 255, 255, 0.5), 0 3px 16px rgba(10, 20, 30, 0.45);
    }}
    .etiqueta {{
      position: absolute;
      right: 6px;
      top: 6px;
      font-family: "Montserrat", sans-serif;
      font-weight: 700;
      font-size: 40px;
      line-height: 48px;
      letter-spacing: 0.01em;
      white-space: nowrap;
      color: #f3dfa2;
      text-shadow: 0 2px 12px rgba(10, 20, 30, 0.55);
    }}
    .etiqueta.no-centro {{
      left: 0;
      right: 0;
      text-align: center;
    }}
    /* Linhas digitadas: a mesma Montserrat da etiqueta e da assinatura. */
    .digitado,
    .linha {{
      font-family: "Montserrat", sans-serif;
      font-weight: 700;
      font-style: normal;
      letter-spacing: 0.03em;
      white-space: nowrap;
      color: #fcfdf5;
      text-shadow: 0 2px 14px rgba(10, 20, 30, 0.6);
    }}
    .digitado {{
      position: absolute;
      left: -300px;
      right: -300px;
      top: 250px;
      text-align: center;
      font-size: 42px;
      line-height: 56px;
    }}
    /* Cada letra digitada ocupa seu lugar desde o início e só aparece quando a tecla bate. */
    .k {{
      display: inline-block;
      opacity: 0;
    }}
    #t-logo {{
      position: absolute;
      left: 330px;
      top: 660px;
      width: 420px;
      height: 378px;
    }}
    .linha {{
      position: absolute;
      left: 0;
      width: 1080px;
      text-align: center;
    }}
    #t-resumo {{
      top: 1076px;
      font-size: 50px;
      line-height: 66px;
    }}
    #t-assinatura {{
      top: 1160px;
      font-family: "Montserrat", sans-serif;
      font-weight: 700;
      font-size: 36px;
      line-height: 48px;
      letter-spacing: 0.04em;
      color: #f3dfa2;
    }}
  </style>
  <div id="root" data-composition-id="texto" data-width="1080" data-height="1920">{"".join(blocos)}

    <!-- Tela final: o logo, a data digitada e a assinatura da marca. -->
    <img id="t-logo" src="assets/logo-vertical-ceu.svg" alt="Madame Solara, moda praia e resort" />
    <div class="linha" id="t-resumo">{letras(RESUMO["texto"], ts_resumo)}</div>
    <div class="linha" id="t-assinatura">{letras(ASSINATURA["texto"], ts_assin)}</div>
  </div>
  <script>
    (function () {{
      const tl = gsap.timeline({{ paused: true }});
      const CURSOR = "3px 0 0 0 rgba(252, 253, 245, 1)";
      const SEM_CURSOR = "3px 0 0 0 rgba(252, 253, 245, 0)";

      // Digitação: cada letra aparece no seu instante e leva o cursor até a próxima chegar.
      function digitar(id) {{
        const ls = Array.from(document.querySelectorAll("#" + id + " .k"));
        ls.forEach(function (el, i) {{
          const t = Number(el.dataset.t);
          const proximo = i + 1 < ls.length ? Number(ls[i + 1].dataset.t) : t + 0.5;
          tl.set(el, {{ opacity: 1, boxShadow: CURSOR }}, t);
          tl.set(el, {{ boxShadow: SEM_CURSOR }}, proximo);
        }});
      }}
{"".join(animacoes)}

      // Tela final: o logo entra, depois a data e a assinatura são digitadas.
      tl.fromTo(
        "#t-logo",
        {{ opacity: 0, scale: 1.1, filter: "blur(14px)" }},
        {{ opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.9, ease: "expo.out" }},
        {T_LOGO},
      );
      digitar("t-resumo");
      digitar("t-assinatura");

      window.__timelines["texto"] = tl;
    }})();
  </script>
</template>
"""
(AQUI / "compositions").mkdir(exist_ok=True)
(AQUI / "compositions" / "texto.html").write_text(TEXTO_HTML, encoding="utf-8")

# ----- Faixa de digitação ---------------------------------------------------
PASTA = AQUI / "assets" / "sfx" / "teclas"


def carregar(nome, corte=None):
    y, r = sf.read(PASTA / nome)
    assert r == SR
    if y.ndim == 1:
        y = np.stack([y, y], axis=1)
    if corte:
        y = y[: int(corte * SR)].copy()
        n = int(0.06 * SR)
        y[-n:] *= np.linspace(1, 0, n)[:, None]
    janela = int(0.005 * SR)
    m = np.abs(y).mean(axis=1)
    rms = np.array([m[i * janela:(i + 1) * janela].mean() for i in range(len(m) // janela)])
    return y / np.abs(y).max(), int(np.argmax(rms) * janela)   # som normalizado e posição do pico


teclas = [carregar(f"tecla_{i}.wav") for i in range(1, 9)]
espacos = [carregar("espaco_1.wav", 0.34), carregar("espaco_3.wav", 0.34)]
faixa = np.zeros((int(DURACAO * SR), 2), np.float32)
ATRASO = 0.02      # o som bate um instante depois da letra

for t, db, eh_espaco in sorted(eventos):
    banco = espacos if eh_espaco else teclas
    som, pico = banco[rng.randrange(len(banco))]
    ganho = 10 ** ((db + rng.uniform(-2.0, 1.5)) / 20)
    i0 = int((t + ATRASO) * SR) - pico
    a, b = max(i0, 0), min(i0 + len(som), len(faixa))
    if b > a:
        faixa[a:b] += som[a - i0:b - i0] * ganho

pico = float(np.abs(faixa).max())
if pico > 0.9:
    faixa *= 0.9 / pico
sf.write(AQUI / "assets" / "sfx" / "digitacao.wav", faixa, SR, subtype="PCM_16")

# Aponta o index.html para a trilha desta variante.
indice = AQUI / "index.html"
texto_indice = indice.read_text(encoding="utf-8")
novo, n = re.subn(r'src="assets/audio/[^"]+\.mp3"', f'src="assets/audio/{NOME}.mp3"', texto_indice)
assert n == 1, n
indice.write_text(novo, encoding="utf-8")

print(json.dumps({"variante": NOME, "teclas": len(eventos), "resumo": [ts_resumo[0], ts_resumo[-1]], "assinatura": [ts_assin[0], ts_assin[-1]]}))
