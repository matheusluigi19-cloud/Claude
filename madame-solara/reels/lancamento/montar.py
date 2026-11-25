"""Monta o vídeo de lançamento da Madame Solara.

Gera, a partir dos textos e tempos abaixo:
  - compositions/texto.html  (cada letra é um <span> com o instante em que aparece)
  - assets/sfx/digitacao.wav (uma tecla por letra, no mesmo instante)

Para trocar a data ou uma frase, edite TEXTOS e rode de novo:
  python montar.py
Precisa de numpy e soundfile.
"""
import html
import json
import random
from pathlib import Path

import numpy as np
import soundfile as sf

AQUI = Path(__file__).parent
DURACAO = 10.8          # segundos
SR = 48000

# ----- Textos (é aqui que se troca a data) ---------------------------------
TEXTOS = {
    "chamada": "guarda essa data",
    "dia": "sábado,",
    "data": "28.11",
    "apoio": "lançamento oficial",
    "resumo": "sábado · 28.11",
    "assinatura": "Você é o seu padrão!",
}

# ----- Tempos, em segundos. A música tem batidas fortes em 2,10 / 6,16 / 7,75 / 8,99.
T_CHAMADA = 0.0
T_DIA = 1.2
T_DATA = [2.10, 2.24, 2.38, 2.52, 2.66]     # um toque por caractere da data, a partir da batida
T_SUBLINHA = 2.86
T_APOIO = 3.3
T_APAGA = 5.35                               # começa a apagar a primeira tela
T_LOGO = 6.16
T_RESUMO = 7.0
T_ASSINATURA = 8.1
T_ASSINATURA_FIM = 8.99                      # a última letra cai na batida

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


linhas = {
    "chamada": tempos(TEXTOS["chamada"], T_CHAMADA, 0.066),
    "dia": tempos(TEXTOS["dia"], T_DIA, 0.088),
    "apoio": tempos(TEXTOS["apoio"], T_APOIO, 0.060),
    "resumo": tempos(TEXTOS["resumo"], T_RESUMO, 0.058),
    "assinatura": tempos(TEXTOS["assinatura"], T_ASSINATURA, 0.046, fim=T_ASSINATURA_FIM),
}
assert len(TEXTOS["data"]) == len(T_DATA), "a data precisa ter um tempo por caractere"

# apagar: a linha de apoio some letra a letra, de trás para a frente; depois as outras, uma tecla cada
n_apoio = len(TEXTOS["apoio"])
apaga_apoio = [round(T_APAGA + i * 0.02, 3) for i in range(n_apoio)]        # i = 0 é a última letra
t_some = {"data": round(apaga_apoio[-1] + 0.07, 3)}
t_some["dia"] = round(t_some["data"] + 0.07, 3)
t_some["chamada"] = round(t_some["dia"] + 0.07, 3)


def spans(nome, com_cursor=True):
    partes = []
    ts = linhas[nome]
    for i, ch in enumerate(TEXTOS[nome]):
        attrs = f'class="k" data-t="{ts[i]}"'
        if nome == "apoio":
            attrs += f' data-fim="{apaga_apoio[n_apoio - 1 - i]}"'
        partes.append(f"<span {attrs}>{'&nbsp;' if ch == ' ' else html.escape(ch)}</span>")
    return "".join(partes)


digitos = "".join(
    f'<span class="d" data-t="{t}">{html.escape(ch)}</span>' for ch, t in zip(TEXTOS["data"], T_DATA)
)

TEXTO_HTML = f"""<template>
  <style>
    @font-face {{
      font-family: "Italiana";
      src: url("assets/fonts/Italiana-Regular.ttf") format("truetype");
      font-weight: 400;
      font-style: normal;
    }}
    @font-face {{
      font-family: "IBM Plex Mono";
      src: url("assets/fonts/ibm-plex-mono-latin-400-normal.woff2") format("woff2");
      font-weight: 400;
      font-style: normal;
    }}
    @font-face {{
      font-family: "Playfair Display";
      src: url("assets/fonts/playfair-display-latin-500-italic.woff2") format("woff2");
      font-weight: 500;
      font-style: italic;
    }}
    #root {{
      position: absolute;
      inset: 0;
      overflow: hidden;
    }}
    .linha {{
      position: absolute;
      left: 0;
      width: 1080px;
      text-align: center;
      white-space: nowrap;
      color: #fcfdf5;
      text-shadow: 0 2px 20px rgba(10, 20, 30, 0.45);
    }}
    /* Cada letra ocupa seu lugar desde o início e só aparece quando a tecla bate. */
    .k,
    .d {{
      display: inline-block;
      opacity: 0;
    }}
    .maquina {{
      font-family: "IBM Plex Mono", monospace;
      font-weight: 400;
      letter-spacing: 0.02em;
    }}
    .italico {{
      font-family: "Playfair Display", serif;
      font-weight: 500;
      font-style: italic;
    }}
    #t-chamada {{
      top: 438px;
      font-size: 44px;
      line-height: 60px;
    }}
    #t-dia {{
      top: 506px;
      font-size: 128px;
      line-height: 150px;
    }}
    #t-data {{
      top: 640px;
      font-family: "Italiana", serif;
      font-size: 300px;
      line-height: 310px;
      letter-spacing: -0.045em;
    }}
    #t-sublinha {{
      position: absolute;
      left: 400px;
      top: 968px;
      width: 280px;
      height: 3px;
      background: linear-gradient(90deg, #eccb6a, #f8e6ab 50%, #dcb24a);
    }}
    #t-apoio {{
      top: 1006px;
      font-size: 42px;
      line-height: 58px;
    }}
    #t-logo {{
      position: absolute;
      left: 280px;
      top: 392px;
      width: 520px;
      height: 468px;
    }}
    #t-resumo {{
      top: 930px;
      font-size: 46px;
      line-height: 62px;
    }}
    #t-assinatura {{
      top: 1010px;
      font-size: 60px;
      line-height: 78px;
    }}
  </style>
  <div id="root" data-composition-id="texto" data-width="1080" data-height="1920">
    <!-- Primeira tela: a data, digitada. Três fontes de propósito: máquina, itálico e a Italiana da marca. -->
    <div class="linha maquina" id="t-chamada">{spans("chamada")}</div>
    <div class="linha italico" id="t-dia">{spans("dia")}</div>
    <div class="linha" id="t-data">{digitos}</div>
    <div id="t-sublinha"></div>
    <div class="linha maquina" id="t-apoio">{spans("apoio")}</div>

    <!-- Segunda tela: o logo, o resumo da data e a assinatura da marca. -->
    <img id="t-logo" src="assets/logo-vertical-ceu.svg" alt="Madame Solara, moda praia e resort" />
    <div class="linha maquina" id="t-resumo">{spans("resumo")}</div>
    <div class="linha italico" id="t-assinatura">{spans("assinatura")}</div>
  </div>
  <script>
    (function () {{
      const tl = gsap.timeline({{ paused: true }});
      const CURSOR = "3px 0 0 0 rgba(252, 253, 245, 1)";
      const SEM_CURSOR = "3px 0 0 0 rgba(252, 253, 245, 0)";

      // Digitação: cada letra aparece no seu instante e leva o cursor até a próxima chegar.
      function digitar(id) {{
        const letras = Array.from(document.querySelectorAll("#" + id + " .k"));
        letras.forEach(function (el, i) {{
          const t = Number(el.dataset.t);
          const proximo = i + 1 < letras.length ? Number(letras[i + 1].dataset.t) : t + 0.5;
          tl.set(el, {{ opacity: 1, boxShadow: CURSOR }}, t);
          tl.set(el, {{ boxShadow: SEM_CURSOR }}, proximo);
        }});
      }}
      ["t-chamada", "t-dia", "t-apoio", "t-resumo", "t-assinatura"].forEach(digitar);

      // A data entra um caractere por toque, com um pequeno salto.
      document.querySelectorAll("#t-data .d").forEach(function (el) {{
        tl.fromTo(
          el,
          {{ opacity: 0, scale: 1.3, transformOrigin: "50% 60%" }},
          {{ opacity: 1, scale: 1, duration: 0.2, ease: "back.out(1.8)" }},
          Number(el.dataset.t),
        );
      }});
      tl.fromTo("#t-sublinha", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.4, ease: "power3.out" }}, {T_SUBLINHA});

      // Apagar: a linha de apoio some letra a letra, depois as outras, uma por tecla.
      document.querySelectorAll("#t-apoio .k").forEach(function (el) {{
        tl.set(el, {{ opacity: 0 }}, Number(el.dataset.fim));
      }});
      tl.set("#t-sublinha", {{ opacity: 0 }}, {t_some["data"]});
      tl.set("#t-data", {{ opacity: 0 }}, {t_some["data"]});
      tl.set("#t-dia", {{ opacity: 0 }}, {t_some["dia"]});
      tl.set("#t-chamada", {{ opacity: 0 }}, {t_some["chamada"]});

      // O logo entra na batida.
      tl.fromTo(
        "#t-logo",
        {{ opacity: 0, scale: 1.14, filter: "blur(16px)" }},
        {{ opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.7, ease: "expo.out" }},
        {T_LOGO},
      );

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


def bater(t, db, banco):
    som, pico = banco[rng.randrange(len(banco))]
    ganho = 10 ** ((db + rng.uniform(-2.0, 1.5)) / 20)
    i0 = int((t + ATRASO) * SR) - pico
    a, b = max(i0, 0), min(i0 + len(som), len(faixa))
    if b > a:
        faixa[a:b] += som[a - i0:b - i0] * ganho


for nome, ts in linhas.items():
    for ch, t in zip(TEXTOS[nome], ts):
        bater(t, -13.0, espacos if ch == " " else teclas)
for t in T_DATA:
    bater(t, -9.5, teclas)                    # a data bate mais forte
for t in apaga_apoio:
    bater(t, -19.0, teclas)                   # apagar é rápido e mais baixo
for t in t_some.values():
    bater(t, -14.0, teclas)

pico = float(np.abs(faixa).max())
if pico > 0.9:
    faixa *= 0.9 / pico
sf.write(AQUI / "assets" / "sfx" / "digitacao.wav", faixa, SR, subtype="PCM_16")

print(json.dumps({"linhas": {k: [v[0], v[-1]] for k, v in linhas.items()}, "apaga": [apaga_apoio[0], t_some]}, ensure_ascii=False))
