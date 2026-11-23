"""Gera a dublagem (voz Piper pt-BR + efeitos) e junta com o vídeo.

Uso: python3 dublar.py <modelo_piper.onnx>
Gera audio/narracao_N.wav, audio/trilha.wav e os vídeos *-dublado.mp4.
"""
import json, os, subprocess, sys, wave
import numpy as np
import linha_do_tempo as L

SR = 48000
DUR = L.DUR
AQUI = os.path.dirname(os.path.abspath(__file__))
AUD = os.path.join(AQUI, "audio")
os.makedirs(AUD, exist_ok=True)

# texto falado (números por extenso para a voz ler certo) e instante de início (s)
FALAS = [
    (L.N1, "Planta petroquímica operando normalmente. Agora, vamos ver o que acontece quando surge um curto no alimentador do reator."),
    (L.N2, "Sem seletividade, a proteção da entrada atua junto, e derruba tudo. Até as cargas que não tinham relação com a falha."),
    (L.N3, "Agora, só o cinquenta e dois A abre, em milissegundos. O resto da planta continua funcionando, e as cargas críticas não sentem o afundamento de tensão."),
    (L.N4, "Mesma falha, consequências totalmente diferentes. É isso que um bom projeto de proteção faz."),
]
LENGTH_SCALE = "1.08"

def ler_wav(caminho):
    tmp = caminho + ".48k.wav"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", caminho, "-ar", str(SR), "-ac", "1",
                    "-af", "loudnorm=I=-16:TP=-1.5:LRA=7", "-ar", str(SR), tmp], check=True)
    with wave.open(tmp) as w:
        x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    os.remove(tmp)
    return x

def env(n, ataque, queda):
    t = np.arange(n) / SR
    return np.minimum(1, t / max(ataque, 1e-4)) * np.exp(-t / queda)

rng = np.random.default_rng(7)

def ruido_filtrado(n, corte):
    x = rng.standard_normal(n).astype(np.float32)
    a = np.exp(-2 * np.pi * corte / SR)
    y = np.empty_like(x)
    acc = 0.0
    for i in range(n):  # passa-baixa de 1ª ordem
        acc = (1 - a) * x[i] + a * acc
        y[i] = acc
    return y / (np.abs(y).max() + 1e-9)

def arco(dur):
    """Zumbido de arco elétrico: 120 Hz rasgado + estalos."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    zumb = np.sign(np.sin(2 * np.pi * 120 * t)) * 0.5 + np.sin(2 * np.pi * 240 * t) * 0.3
    estalo = rng.standard_normal(n) * (rng.random(n) < 0.004) * 3
    chiado = rng.standard_normal(n) * 0.25
    x = (zumb + chiado) * (0.75 + 0.25 * np.sin(2 * np.pi * 7 * t)) + estalo
    e = np.minimum(1, t / 0.02) * np.minimum(1, (dur - t) / 0.08)
    return (x * e).astype(np.float32)

def estouro():
    n = int(0.5 * SR)
    t = np.arange(n) / SR
    x = rng.standard_normal(n) * env(n, 0.002, 0.07) + np.sin(2 * np.pi * 70 * t) * env(n, 0.002, 0.12)
    return x.astype(np.float32)

def disjuntor():
    n = int(0.45 * SR)
    t = np.arange(n) / SR
    clique = rng.standard_normal(n) * env(n, 0.0005, 0.012)
    baque = np.sin(2 * np.pi * 85 * t) * env(n, 0.002, 0.09)
    eco = rng.standard_normal(n) * env(n, 0.03, 0.05) * 0.15
    return (clique * 0.9 + baque * 1.0 + eco).astype(np.float32)

def desliga(dur=1.6):
    """Zumbido de transformador caindo de frequência até sumir."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = 120 * (1 - 0.65 * t / dur)
    fase = 2 * np.pi * np.cumsum(f) / SR
    x = np.sin(fase) + 0.4 * np.sin(2 * fase)
    return (x * (1 - t / dur) ** 2).astype(np.float32)

def zumbido(dur):
    n = int(dur * SR)
    t = np.arange(n) / SR
    x = np.sin(2 * np.pi * 120 * t) + 0.5 * np.sin(2 * np.pi * 240 * t) + 0.2 * np.sin(2 * np.pi * 360 * t)
    return x.astype(np.float32)

def tom_transicao():
    n = int(2.2 * SR)
    t = np.arange(n) / SR
    x = (np.sin(2 * np.pi * 196 * t) + 0.6 * np.sin(2 * np.pi * 294 * t) + 0.3 * np.sin(2 * np.pi * 392 * t))
    return (x * np.minimum(1, t / 0.3) * np.exp(-t / 0.9)).astype(np.float32)

def por(trilha, sinal, t0, ganho):
    i = int(t0 * SR)
    j = min(len(trilha), i + len(sinal))
    trilha[i:j] += sinal[: j - i] * ganho

def faixa_zumbido(a, b, ganho):
    z = zumbido(b - a)
    n = len(z)
    rampa = int(0.6 * SR)
    e = np.ones(n, dtype=np.float32)
    e[:rampa] = np.linspace(0, 1, rampa)
    e[-int(0.05 * SR):] = np.linspace(1, 0, int(0.05 * SR))
    return z * e, ganho

def main(modelo):
    voz = np.zeros(int(DUR * SR), dtype=np.float32)
    sfx = np.zeros_like(voz)
    tempos = []
    for k, (t0, fala) in enumerate(FALAS, 1):
        cru = os.path.join(AUD, f"narracao_{k}_cru.wav")
        subprocess.run(["piper", "-m", modelo, "-f", cru, "--length-scale", LENGTH_SCALE,
                        "--sentence-silence", "0.35"], input=fala.encode(), check=True,
                       stderr=subprocess.DEVNULL)
        x = ler_wav(cru)
        os.replace(cru, os.path.join(AUD, f"narracao_{k}.wav"))
        por(voz, x, t0, 1.0)
        tempos.append((t0, round(t0 + len(x) / SR, 2)))

    # zumbido de fundo enquanto a planta está energizada
    for a, b in [(2.3, L.TRIP_A + 0.05), (L.DEPOIS, L.FIM_D)]:
        z, g = faixa_zumbido(a, b, 0.018)
        por(sfx, z, a, g)
    # ANTES: curto, corrente de falta até o 52-1 abrir
    por(sfx, estouro(), L.FALHA_A, 0.55)
    por(sfx, arco(L.TRIP_A - L.FALHA_A), L.FALHA_A, 0.10)
    por(sfx, disjuntor(), L.TRIP_A, 0.7)
    por(sfx, desliga(), L.TRIP_A + 0.05, 0.12)
    # transição
    por(sfx, tom_transicao(), L.TRANS + 0.4, 0.10)
    # DEPOIS: mesmo curto, 52-A abre logo
    por(sfx, estouro(), L.FALHA_D, 0.55)
    por(sfx, arco(L.TRIP_D - L.FALHA_D), L.FALHA_D, 0.10)
    por(sfx, disjuntor(), L.TRIP_D, 0.7)

    # abaixa os efeitos de fundo quando a voz fala (ducking simples)
    janela = int(0.15 * SR)
    nivel = np.convolve(np.abs(voz), np.ones(janela) / janela, mode="same")
    duck = 1 - 0.5 * np.clip(nivel / 0.05, 0, 1)
    mix = voz * 0.9 + sfx * duck
    mix = mix / max(1.0, np.abs(mix).max() / 0.95)
    estereo = np.stack([mix, mix], axis=1)
    trilha = os.path.join(AUD, "trilha.wav")
    with wave.open(trilha, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((estereo * 32767).astype(np.int16).tobytes())

    with open(os.path.join(AUD, "tempos.json"), "w") as f:
        json.dump(tempos, f)
    print("tempos das falas:", tempos)
    return trilha

def juntar(trilha):
    for v in ["com-legenda", "sem-legenda"]:
        src = os.path.join(AQUI, f"antes-e-depois-da-protecao-{v}.mp4")
        dst = os.path.join(AQUI, f"antes-e-depois-da-protecao-{v}-dublado.mp4")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-i", trilha,
                        "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                        "-shortest", "-movflags", "+faststart", dst], check=True)
        print("ok", dst)

if __name__ == "__main__":
    if sys.argv[1] == "juntar":
        juntar(os.path.join(AUD, "trilha.wav"))
    else:
        main(sys.argv[1])
