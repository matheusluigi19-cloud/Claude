"""Monta o vídeo de lançamento da Madame Solara.

O visual segue o vídeo modelo enviado pela cliente: um título compacto no centro, com uma
etiqueta pequena sem serifa, uma palavra grande em letra cursiva, uma linha em itálico
digitada letra a letra e uma fileira de brilhos.

Gera, a partir dos textos e tempos abaixo:
  - compositions/texto.html  (cada letra digitada é um <span> com o instante em que aparece)
  - assets/sfx/digitacao.wav (uma tecla por letra, no mesmo instante)

Para trocar a data ou uma frase, edite TELAS e rode de novo:
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

# ----- Textos e tempos (é aqui que se troca a data) -------------------------
# A música tem batidas fortes em 2,10 / 4,93 / 6,16 / 7,75 / 8,99 s: as telas trocam nelas.
TELAS = [
    {"id": "t1", "inicio": 0.0, "fim": 2.10,
     "etiqueta": "anota aí:", "cursiva": "Sábado", "digitado": "28 de novembro", "t_digitado": 0.62},
    {"id": "t2", "inicio": 2.10, "fim": 4.93,
     "etiqueta": "é dia de:", "cursiva": "Lançamento", "digitado": "oficial da marca", "t_digitado": 2.95},
]
T_LOGO = 4.93
RESUMO = {"texto": "sábado · 28.11", "inicio": 5.42, "fim": 6.16}          # a última letra cai na batida
ASSINATURA = {"texto": "você é o seu padrão!", "inicio": 7.75, "fim": 8.99}

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


ESTRELA = "M0,-10 C0.9,-3 3,-0.9 10,0 C3,0.9 0.9,3 0,10 C-0.9,3 -3,0.9 -10,0 C-3,-0.9 -0.9,-3 0,-10Z"


def brilhos(ident):
    """A fileira de pontos e estrelas que fecha o título, como no modelo."""
    partes, x = [], 8
    for tipo in [".", ":", ".", "*", ".", ":", ".", "*", "."]:
        if tipo == ".":
            partes.append(f'<circle class="b" cx="{x}" cy="14" r="2.6" />')
            x += 20
        elif tipo == ":":
            partes.append(f'<g class="b"><circle cx="{x}" cy="8" r="2.2" /><circle cx="{x}" cy="20" r="2.2" /></g>')
            x += 20
        else:
            partes.append(f'<path class="b" transform="translate({x + 6} 14)" d="{ESTRELA}" />')
            x += 34
    return f'<svg class="brilhos" id="{ident}" viewBox="0 0 {x} 28" width="{x}" height="28">{"".join(partes)}</svg>', x


eventos = []          # (instante, força em dB, é espaço) para a faixa de teclado
blocos, animacoes = [], []
for tela in TELAS:
    i = tela["id"]
    ts = tempos(tela["digitado"], tela["t_digitado"], 0.066)
    t_fim_digitado = ts[-1]
    for ch, t in zip(tela["digitado"], ts):
        eventos.append((t, -13.0, ch == " "))
    eventos.append((tela["inicio"] + 0.02, -12.0, False))                       # a etiqueta entra com uma tecla
    n = len(tela["cursiva"])
    for k in range(n):                                                           # a cursiva: teclas rápidas e baixas
        eventos.append((tela["inicio"] + 0.06 + k * 0.5 / n, -18.0, False))
    svg, _ = brilhos(i + "-brilhos")
    blocos.append(f"""
    <div class="titulo" id="{i}">
      <div class="caixa">
        <div class="etiqueta" id="{i}-etiqueta">{html.escape(tela["etiqueta"])}</div>
        <div class="cursiva-janela" id="{i}-janela"><span class="cursiva" id="{i}-cursiva">{html.escape(tela["cursiva"])}</span></div>
        <div class="digitado" id="{i}-digitado">{letras(tela["digitado"], ts)}</div>
        {svg}
      </div>
    </div>""")
    animacoes.append(f"""
      // Tela "{tela["cursiva"]}": entra em {tela["inicio"]} s e sai no corte de {tela["fim"]} s.
      tl.set("#{i}", {{ opacity: 1 }}, {tela["inicio"]});
      tl.fromTo("#{i}-etiqueta", {{ opacity: 0, scale: 0.7 }}, {{ opacity: 1, scale: 1, duration: 0.22, ease: "back.out(2)" }}, {tela["inicio"]});
      tl.fromTo("#{i}-janela", {{ clipPath: "inset(-30% 100% -30% -12%)" }}, {{ clipPath: "inset(-30% -12% -30% -12%)", duration: 0.55, ease: "power2.out" }}, {round(tela["inicio"] + 0.04, 3)});
      digitar("{i}-digitado");
      tl.fromTo("#{i}-brilhos .b", {{ opacity: 0, scale: 0, transformOrigin: "50% 50%" }}, {{ opacity: 1, scale: 1, duration: 0.2, ease: "back.out(2)", stagger: 0.035 }}, {round(t_fim_digitado + 0.1, 3)});
      tl.set("#{i}", {{ opacity: 0 }}, {tela["fim"]});""")

ts_resumo = tempos(RESUMO["texto"], RESUMO["inicio"], 0.06, fim=RESUMO["fim"])
ts_assin = tempos(ASSINATURA["texto"], ASSINATURA["inicio"], 0.06, fim=ASSINATURA["fim"])
for texto, ts in ((RESUMO["texto"], ts_resumo), (ASSINATURA["texto"], ts_assin)):
    for ch, t in zip(texto, ts):
        eventos.append((t, -13.0, ch == " "))
svg_fim, largura_fim = brilhos("t-fim-brilhos")

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
    /* Título no estilo do modelo: etiqueta pequena, palavra cursiva grande, linha digitada e brilhos. */
    .titulo {{
      position: absolute;
      left: 0;
      top: 540px;
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
    .digitado,
    .linha {{
      font-family: "Playfair Display", serif;
      font-weight: 500;
      font-style: italic;
      white-space: nowrap;
      color: #fcfdf5;
      text-shadow: 0 2px 14px rgba(10, 20, 30, 0.55);
    }}
    .digitado {{
      position: absolute;
      right: 14px;
      top: 232px;
      font-size: 52px;
      line-height: 64px;
    }}
    .brilhos {{
      position: absolute;
      left: calc(50% - {largura_fim // 2}px);
      top: 316px;
      overflow: visible;
      fill: #fcfdf5;
    }}
    /* Cada letra digitada ocupa seu lugar desde o início e só aparece quando a tecla bate. */
    .k {{
      display: inline-block;
      opacity: 0;
    }}
    #t-logo {{
      position: absolute;
      left: 310px;
      top: 420px;
      width: 460px;
      height: 414px;
    }}
    .linha {{
      position: absolute;
      left: 0;
      width: 1080px;
      text-align: center;
    }}
    #t-resumo {{
      top: 872px;
      font-size: 60px;
      line-height: 76px;
    }}
    #t-fim-brilhos {{
      left: {round((1080 - largura_fim) / 2)}px;
      top: 968px;
    }}
    #t-assinatura {{
      top: 1024px;
      font-family: "Montserrat", sans-serif;
      font-weight: 700;
      font-style: normal;
      font-size: 34px;
      line-height: 46px;
      letter-spacing: 0.04em;
      color: #f3dfa2;
    }}
  </style>
  <div id="root" data-composition-id="texto" data-width="1080" data-height="1920">{"".join(blocos)}

    <!-- Tela final: o logo, a data digitada e a assinatura da marca. -->
    <img id="t-logo" src="assets/logo-vertical-ceu.svg" alt="Madame Solara, moda praia e resort" />
    <div class="linha" id="t-resumo">{letras(RESUMO["texto"], ts_resumo)}</div>
    {svg_fim}
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

      // Tela final: o logo entra na batida, depois a data e a assinatura são digitadas.
      tl.fromTo(
        "#t-logo",
        {{ opacity: 0, scale: 1.16, filter: "blur(16px)" }},
        {{ opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.6, ease: "expo.out" }},
        {T_LOGO},
      );
      digitar("t-resumo");
      tl.fromTo("#t-fim-brilhos .b", {{ opacity: 0, scale: 0, transformOrigin: "50% 50%" }}, {{ opacity: 1, scale: 1, duration: 0.2, ease: "back.out(2)", stagger: 0.035 }}, {round(RESUMO["fim"] + 0.12, 3)});
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

print(json.dumps({"teclas": len(eventos), "resumo": [ts_resumo[0], ts_resumo[-1]], "assinatura": [ts_assin[0], ts_assin[-1]]}))
