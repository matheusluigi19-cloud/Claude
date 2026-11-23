"""Gera o vídeo "Antes e depois da proteção" (subestação de planta petroquímica).

Uso: python3 gerar_video.py            -> gera as duas versões (com e sem legenda)
Os rótulos das cargas e disjuntores ficam em CARGAS / DISJ para ajustar ao slide 2.
"""
import math, subprocess, sys
import cairo

W, H, FPS = 1920, 1080, 30
DUR = 75.0

# ---------------------------------------------------------------- textos
CARGAS = {
    "A": ("Reator VG-principal", "linha com a falta"),
    "B": ("Outras cargas", "sem relação com a falta"),
    "C": ("Cargas críticas", "não podem parar"),
}
CRITICAS = {"C"}
DISJ = {"in": "52-1", "A": "52-A", "B": "52-B", "C": "52-C"}
# funções de proteção do esquema proposto (slide 2): só aparecem na parte "Depois"
FUNC = {"in": "entrada · 51 com atraso de 0,3 s", "A": "50/51, 50N/51N, 79", "B": "", "C": "27 + UPS"}
FUNC_BARRA = "proteção 87B"
DISCENTES = "Stephanie Angele · Murilo Lima · Rian David"

NARRACAO = [
    (1.0, 9.6, "Planta petroquímica operando normalmente. Agora vamos ver o que acontece quando surge um curto no alimentador do reator."),
    (17.6, 29.4, "Sem seletividade, a proteção da entrada atua junto e derruba tudo, até as cargas que não tinham relação com a falha."),
    (39.2, 52.0, "Agora só o 52-A abre, em milissegundos. O resto da planta continua funcionando e as cargas críticas não sentem o afundamento de tensão."),
    (62.0, 72.5, "Mesma falha, consequências totalmente diferentes. É isso que um bom projeto de proteção faz."),
]

# ---------------------------------------------------------------- cores
def hx(s, a=1.0):
    s = s.lstrip("#")
    return (int(s[0:2], 16) / 255, int(s[2:4], 16) / 255, int(s[4:6], 16) / 255, a)

BG = hx("0D131A")
GRID = hx("17212B")
VIVO = hx("F2B33D")        # condutor energizado
MORTO = hx("33404C")       # condutor desenergizado
FALHA = hx("FF4A3D")
FECHADO = hx("E5484D")     # convenção ANSI: vermelho = fechado
ABERTO = hx("2FB36E")      # verde = aberto
TXT = hx("E8EDF2")
TXT2 = hx("8C9AA8")
CARD = hx("16202A")
CARD_OFF = hx("12191F")
UPS = hx("4DA3FF")

def mix(a, b, k):
    k = max(0.0, min(1.0, k))
    return tuple(a[i] + (b[i] - a[i]) * k for i in range(4))

def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))

def ramp(t, t0, t1):
    if t1 == t0:
        return 1.0 if t >= t0 else 0.0
    return clamp((t - t0) / (t1 - t0))

def ease(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)

def ease_out(x):
    x = clamp(x)
    return 1 - (1 - x) ** 3

def fade(t, a, b, c, d):
    """0 antes de a, sobe até b, fica 1 até c, desce até d."""
    return ease(ramp(t, a, b)) * (1 - ease(ramp(t, c, d)))

# ---------------------------------------------------------------- texto
def font(ctx, size, bold=False, weight=None):
    ctx.select_font_face("Inter", cairo.FONT_SLANT_NORMAL,
                         cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(size)

def text(ctx, s, x, y, size, color, bold=False, align="center", alpha=1.0):
    font(ctx, size, bold)
    ext = ctx.text_extents(s)
    if align == "center":
        x0 = x - ext.width / 2 - ext.x_bearing
    elif align == "right":
        x0 = x - ext.width - ext.x_bearing
    else:
        x0 = x
    ctx.set_source_rgba(color[0], color[1], color[2], color[3] * alpha)
    ctx.move_to(x0, y)
    ctx.show_text(s)
    return ext.width

def wrap(ctx, s, size, maxw, bold=False):
    font(ctx, size, bold)
    linhas, atual = [], ""
    for p in s.split():
        teste = (atual + " " + p).strip()
        if ctx.text_extents(teste).x_advance > maxw and atual:
            linhas.append(atual)
            atual = p
        else:
            atual = teste
    if atual:
        linhas.append(atual)
    return linhas

def rrect(ctx, x, y, w, h, r):
    ctx.new_sub_path()
    ctx.arc(x + w - r, y + r, r, -math.pi / 2, 0)
    ctx.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    ctx.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
    ctx.arc(x + r, y + r, r, math.pi, 3 * math.pi / 2)
    ctx.close_path()

# ---------------------------------------------------------------- diagrama
# coordenadas no "espaço do diagrama" (1920x1080)
SRC = (960, 122)
B1 = (960, 222)
BUS_Y = 318
BUS_X = (470, 1450)
FX = {"A": 560, "B": 960, "C": 1360}
BR_Y = 408
FAULT_Y = 480
LOAD_Y = 540
LOAD_W, LOAD_H = 330, 182

def estado_normal():
    return {
        "brk": {"in": 0.0, "A": 0.0, "B": 0.0, "C": 0.0},     # 0 fechado, 1 aberto
        "brk_flash": {"in": 0.0, "A": 0.0, "B": 0.0, "C": 0.0},
        "seg": {"in": 1.0, "main": 1.0, "A": 1.0, "Abot": 1.0, "B": 1.0, "C": 1.0},
        "load": {"A": 1.0, "B": 1.0, "C": 1.0},
        "fault": 0.0,          # intensidade do raio
        "fault_flow": 0.0,     # corrente de curto passando
        "dip": 0.0,            # afundamento de tensão no barramento
        "ups": 0.0,
        "reveal": 1.0,
        "t": 0.0,
        "func": 0.0,
    }

def seg_color(v, dip=0.0):
    c = mix(MORTO, VIVO, v)
    if dip > 0:
        c = mix(c, hx("8A5A1E"), dip * v)
    return c

def line(ctx, pts, color, w):
    ctx.set_source_rgba(*color)
    ctx.set_line_width(w)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.move_to(*pts[0])
    for p in pts[1:]:
        ctx.line_to(*p)
    ctx.stroke()

def glow_line(ctx, pts, color, w, v):
    if v > 0.02:
        g = (color[0], color[1], color[2], 0.18 * v)
        line(ctx, pts, g, w + 14)
    line(ctx, pts, color, w)

def breaker(ctx, x, y, aberto, flash, nome, alpha=1.0, func="", func_a=0.0):
    s = 62
    # flash de atuação
    if flash > 0:
        r = 40 + 90 * (1 - flash)
        ctx.set_source_rgba(1, 1, 1, 0.55 * flash * alpha)
        ctx.set_line_width(4)
        ctx.new_path()
        ctx.arc(x, y, r, 0, 2 * math.pi)
        ctx.stroke()
    cor = mix(FECHADO, ABERTO, aberto)
    ctx.set_source_rgba(BG[0], BG[1], BG[2], alpha)
    rrect(ctx, x - s / 2, y - s / 2, s, s, 8)
    ctx.fill()
    rrect(ctx, x - s / 2, y - s / 2, s, s, 8)
    ctx.set_source_rgba(cor[0], cor[1], cor[2], (0.95 - 0.75 * aberto) * alpha)
    ctx.fill_preserve()
    ctx.set_source_rgba(cor[0], cor[1], cor[2], alpha)
    ctx.set_line_width(4)
    ctx.stroke()
    # contato: barra vertical (fechado) que gira até ficar inclinada (aberto)
    ang = aberto * math.radians(38)
    ctx.save()
    ctx.translate(x, y + 18)
    ctx.rotate(-ang)
    ctx.set_source_rgba(1, 1, 1, 0.95 * alpha)
    ctx.set_line_width(5)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.move_to(0, 0)
    ctx.line_to(0, -36)
    ctx.stroke()
    ctx.restore()
    text(ctx, nome, x + s / 2 + 16, y + 9, 26, TXT, bold=True, align="left", alpha=alpha)
    if func and func_a > 0.01:
        text(ctx, func, x + s / 2 + 16, y + 38, 20, VIVO, align="left", alpha=alpha * func_a)

def lamp(ctx, x, y, on, alpha=1.0):
    if on > 0.02:
        g = cairo.RadialGradient(x, y, 4, x, y, 70)
        g.add_color_stop_rgba(0, VIVO[0], VIVO[1], VIVO[2], 0.55 * on * alpha)
        g.add_color_stop_rgba(1, VIVO[0], VIVO[1], VIVO[2], 0)
        ctx.set_source(g)
        ctx.arc(x, y, 70, 0, 2 * math.pi)
        ctx.fill()
    c = mix(hx("2A343E"), hx("FFD27A"), on)
    ctx.set_source_rgba(c[0], c[1], c[2], alpha)
    ctx.arc(x, y, 17, 0, 2 * math.pi)
    ctx.fill()
    ctx.set_source_rgba(c[0], c[1], c[2], alpha)
    ctx.set_line_width(3)
    ctx.arc(x, y, 24, 0, 2 * math.pi)
    ctx.stroke()

def load_box(ctx, k, on, ups, alpha=1.0, reator_falha=0.0):
    x = FX[k] - LOAD_W / 2
    y = LOAD_Y
    borda = mix(MORTO, VIVO, on)
    if reator_falha > 0:
        borda = mix(borda, FALHA, reator_falha)
    ctx.set_source_rgba(*mix(CARD_OFF, CARD, on)[:3], alpha)
    rrect(ctx, x, y, LOAD_W, LOAD_H, 16)
    ctx.fill()
    rrect(ctx, x, y, LOAD_W, LOAD_H, 16)
    ctx.set_source_rgba(borda[0], borda[1], borda[2], (0.45 + 0.55 * on) * alpha)
    ctx.set_line_width(3)
    ctx.stroke()
    lamp(ctx, x + 58, y + 64, on, alpha)
    nome, sub = CARGAS[k]
    linhas = wrap(ctx, nome, 30, LOAD_W - 120, bold=True)
    yy = y + 52
    for ln in linhas:
        text(ctx, ln, x + 104, yy, 30, mix(TXT2, TXT, on), bold=True, align="left", alpha=alpha)
        yy += 36
    for ln in wrap(ctx, sub, 22, LOAD_W - 120):
        text(ctx, ln, x + 104, yy, 22, TXT2, align="left", alpha=alpha)
        yy += 27
    estado = "operando" if on > 0.5 else "desligada"
    cor_est = mix(hx("6B7681"), VIVO, on)
    text(ctx, estado.upper(), x + 104, y + LOAD_H - 22, 20, cor_est, bold=True, align="left", alpha=alpha)
    # selo UPS
    if ups > 0.01 and k in CRITICAS:
        sc = 0.6 + 0.4 * ease_out(ups)
        bx, by = x + LOAD_W - 18, y - 4
        ctx.save()
        ctx.translate(bx, by)
        ctx.scale(sc, sc)
        rrect(ctx, -96, -26, 112, 52, 26)
        ctx.set_source_rgba(UPS[0], UPS[1], UPS[2], ups * alpha)
        ctx.fill()
        # ícone de bateria
        ctx.set_source_rgba(1, 1, 1, ups * alpha)
        ctx.set_line_width(3)
        rrect(ctx, -82, -11, 26, 22, 3)
        ctx.stroke()
        ctx.rectangle(-56, -5, 4, 10)
        ctx.fill()
        ctx.rectangle(-78, -7, 12, 14)
        ctx.fill()
        text(ctx, "UPS", -20, 10, 26, hx("FFFFFF"), bold=True, alpha=ups * alpha)
        ctx.restore()

def bolt(ctx, x, y, k, t):
    if k <= 0.01:
        return
    # brilho
    pulse = 0.75 + 0.25 * math.sin(t * 38)
    g = cairo.RadialGradient(x, y, 5, x, y, 150)
    g.add_color_stop_rgba(0, FALHA[0], FALHA[1], FALHA[2], 0.6 * k * pulse)
    g.add_color_stop_rgba(1, FALHA[0], FALHA[1], FALHA[2], 0)
    ctx.set_source(g)
    ctx.arc(x, y, 150, 0, 2 * math.pi)
    ctx.fill()
    s = 1.0 + 0.08 * math.sin(t * 30)
    ctx.save()
    ctx.translate(x - 64, y)
    ctx.scale(s * k ** 0.3, s * k ** 0.3)
    pts = [(14, -58), (-16, 4), (4, 4), (-12, 58), (24, -10), (4, -10), (22, -58)]
    ctx.move_to(*pts[0])
    for p in pts[1:]:
        ctx.line_to(*p)
    ctx.close_path()
    ctx.set_source_rgba(FALHA[0], FALHA[1], FALHA[2], k)
    ctx.fill_preserve()
    ctx.set_source_rgba(1, 0.85, 0.8, k)
    ctx.set_line_width(2.5)
    ctx.stroke()
    ctx.restore()
    # marca do curto no condutor
    ctx.set_source_rgba(1, 1, 1, k * pulse)
    ctx.arc(x, y, 9, 0, 2 * math.pi)
    ctx.fill()

def fluxo(ctx, pts, k, t):
    """Corrente de curto: traços vermelhos correndo pelo caminho."""
    if k <= 0.01:
        return
    ctx.save()
    ctx.set_source_rgba(FALHA[0], FALHA[1], FALHA[2], 0.85 * k)
    ctx.set_line_width(7)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_dash([18, 26], -t * 260)
    ctx.move_to(*pts[0])
    for p in pts[1:]:
        ctx.line_to(*p)
    ctx.stroke()
    ctx.restore()

def fonte(ctx, alpha, v):
    x, y = SRC
    c = mix(MORTO, VIVO, v)
    ctx.set_source_rgba(BG[0], BG[1], BG[2], alpha)
    ctx.arc(x, y, 38, 0, 2 * math.pi)
    ctx.fill()
    ctx.set_source_rgba(c[0], c[1], c[2], alpha)
    ctx.set_line_width(4)
    ctx.arc(x, y, 38, 0, 2 * math.pi)
    ctx.stroke()
    # senoide
    ctx.set_line_width(4)
    for i in range(41):
        xx = x - 20 + i
        yy = y - 11 * math.sin((i / 40) * 2 * math.pi)
        if i == 0:
            ctx.move_to(xx, yy)
        else:
            ctx.line_to(xx, yy)
    ctx.stroke()
    text(ctx, "Rede da concessionária", x + 62, y - 4, 26, TXT, bold=True, align="left", alpha=alpha)
    text(ctx, "via transformador", x + 62, y + 26, 22, TXT2, align="left", alpha=alpha)

def diagrama(ctx, st):
    t = st["t"]
    rv = st["reveal"]
    a_src = ease(ramp(rv, 0.0, 0.25))
    a_bus = ease(ramp(rv, 0.15, 0.45))
    a_feed = {k: ease(ramp(rv, 0.35 + 0.1 * i, 0.65 + 0.1 * i)) for i, k in enumerate("ABC")}

    seg = st["seg"]
    dip = st["dip"]

    # condutores
    def cl(v, a, d=0.0):
        c = seg_color(v, d)
        return (c[0], c[1], c[2], c[3] * a)

    glow_line(ctx, [(SRC[0], SRC[1] + 38), (B1[0], B1[1] - 31)], cl(seg["in"], a_src), 7, seg["in"] * a_src)
    glow_line(ctx, [(B1[0], B1[1] + 31), (B1[0], BUS_Y)], cl(seg["main"], a_bus, dip), 7, seg["main"] * a_bus)
    # barramento
    glow_line(ctx, [(BUS_X[0], BUS_Y), (BUS_X[1], BUS_Y)], cl(seg["main"], a_bus, dip), 12, seg["main"] * a_bus)
    if a_bus > 0.05:
        text(ctx, "Barra de média tensão", BUS_X[1] + 22, BUS_Y + 9, 22, TXT2, align="left", alpha=a_bus)
        if st["func"] > 0.01:
            text(ctx, FUNC_BARRA, BUS_X[1] + 22, BUS_Y + 38, 20, VIVO, align="left", alpha=a_bus * st["func"])

    for k in "ABC":
        x = FX[k]
        a = a_feed[k]
        vtop = seg["main"] if k != "A" else seg["main"]
        glow_line(ctx, [(x, BUS_Y), (x, BR_Y - 31)], cl(vtop, a, dip), 7, vtop * a)
        vbot = seg["Abot"] if k == "A" else seg[k]
        glow_line(ctx, [(x, BR_Y + 31), (x, LOAD_Y)], cl(vbot, a, dip), 7, vbot * a)

    # corrente de curto (por cima dos condutores)
    if st["fault_flow"] > 0:
        caminho = [(SRC[0], SRC[1] + 38), (B1[0], BUS_Y), (FX["A"], BUS_Y), (FX["A"], FAULT_Y)]
        if st.get("flow_from_bus"):
            caminho = [(FX["A"], BUS_Y), (FX["A"], FAULT_Y)]
        fluxo(ctx, caminho, st["fault_flow"], t)

    # disjuntores
    breaker(ctx, B1[0], B1[1], st["brk"]["in"], st["brk_flash"]["in"], DISJ["in"], a_bus, FUNC["in"], st["func"])
    for k in "ABC":
        breaker(ctx, FX[k], BR_Y, st["brk"][k], st["brk_flash"][k], DISJ[k], a_feed[k], FUNC[k], st["func"])

    fonte(ctx, a_src, seg["in"])

    for k in "ABC":
        load_box(ctx, k, st["load"][k], st["ups"], a_feed[k],
                 reator_falha=(st["fault"] if k == "A" else 0.0))

    bolt(ctx, FX["A"], FAULT_Y, st["fault"], t)

def legenda_disj(ctx, alpha):
    if alpha <= 0.01:
        return
    x, y = 1500, 120
    for i, (cor, nome) in enumerate([(FECHADO, "fechado"), (ABERTO, "aberto")]):
        yy = y + i * 36
        rrect(ctx, x, yy - 18, 22, 22, 4)
        ctx.set_source_rgba(cor[0], cor[1], cor[2], alpha * (0.95 if i == 0 else 0.35))
        ctx.fill_preserve()
        ctx.set_source_rgba(cor[0], cor[1], cor[2], alpha)
        ctx.set_line_width(2.5)
        ctx.stroke()
        text(ctx, "disjuntor " + nome, x + 34, yy, 21, TXT2, align="left", alpha=alpha)

# ---------------------------------------------------------------- cenas
def cena_abertura(t):
    st = estado_normal()
    st["t"] = t
    st["reveal"] = ease(ramp(t, 0.6, 4.2))
    acende = {k: ease(ramp(t, 3.6 + 0.35 * i, 4.3 + 0.35 * i)) for i, k in enumerate("ABC")}
    eng = ease(ramp(t, 3.2, 4.0))
    st["seg"] = {k: eng for k in st["seg"]}
    st["load"] = acende
    return st

def cena_antes(t):
    """t global, 10..30"""
    st = estado_normal()
    st["t"] = t
    tf = 12.6          # curto
    tt = 16.4          # 52-1 abre (proteção lenta, sem seletividade)
    st["fault"] = ease(ramp(t, tf, tf + 0.25)) * (1 - ease(ramp(t, tt + 0.6, tt + 1.6)))
    st["fault_flow"] = ease(ramp(t, tf + 0.2, tf + 0.8)) * (1 - ease(ramp(t, tt, tt + 0.25)))
    # afundamento geral enquanto o curto persiste
    st["dip"] = 0.75 * ease(ramp(t, tf, tf + 0.3)) * (1 - ease(ramp(t, tt, tt + 0.2)))
    ab = ease_out(ramp(t, tt, tt + 0.35))
    st["brk"]["in"] = ab
    st["brk_flash"]["in"] = (1 - ramp(t, tt, tt + 0.7)) if t >= tt else 0.0
    off = 1 - ease(ramp(t, tt + 0.05, tt + 0.6))
    st["seg"] = {"in": 1.0, "main": off, "A": off, "Abot": off, "B": off, "C": off}
    for i, k in enumerate("ABC"):
        base = 1 - ease(ramp(t, tt + 0.15 + 0.25 * i, tt + 0.55 + 0.25 * i))
        # cargas piscam durante o afundamento
        if tf < t < tt:
            base *= 0.72 + 0.22 * math.sin(t * 17 + i)
        st["load"][k] = base
    return st

def cena_depois(t):
    """t global, 35..60"""
    st = estado_normal()
    st["t"] = t
    tf = 38.0
    tt = 38.3          # 52-A abre em milissegundos (acelerado no vídeo para ser visível)
    st["fault"] = ease(ramp(t, tf, tf + 0.2)) * (1 - ease(ramp(t, tt + 0.6, tt + 1.6)))
    st["fault_flow"] = ease(ramp(t, tf, tf + 0.12)) * (1 - ease(ramp(t, tt, tt + 0.12)))
    st["flow_from_bus"] = False
    st["dip"] = 0.75 * ease(ramp(t, tf, tf + 0.08)) * (1 - ease(ramp(t, tt, tt + 0.35)))
    ab = ease_out(ramp(t, tt, tt + 0.25))
    st["brk"]["A"] = ab
    st["brk_flash"]["A"] = (1 - ramp(t, tt, tt + 0.7)) if t >= tt else 0.0
    st["seg"]["Abot"] = 1 - ease(ramp(t, tt + 0.02, tt + 0.4))
    st["load"]["A"] = 1 - ease(ramp(t, tt + 0.1, tt + 0.6))
    # carga não crítica sente o afundamento por um instante; a crítica não
    if tf < t < tt + 0.35:
        st["load"]["B"] = 0.65 + 0.2 * math.sin(t * 40)
    st["ups"] = ease_out(ramp(t, tf + 0.05, tf + 0.5))
    st["func"] = ease(ramp(t, 35.6, 36.6))
    return st

# ---------------------------------------------------------------- overlays
def tag(ctx, texto, cor, alpha, sub=None):
    if alpha <= 0.01:
        return
    font(ctx, 26, True)
    w = ctx.text_extents(texto).x_advance
    x, y = 70, 58
    rrect(ctx, x, y, w + 58, 50, 25)
    ctx.set_source_rgba(cor[0], cor[1], cor[2], 0.18 * alpha)
    ctx.fill_preserve()
    ctx.set_source_rgba(cor[0], cor[1], cor[2], alpha)
    ctx.set_line_width(2)
    ctx.stroke()
    ctx.set_source_rgba(cor[0], cor[1], cor[2], alpha)
    ctx.arc(x + 25, y + 25, 6, 0, 2 * math.pi)
    ctx.fill()
    text(ctx, texto, x + 42, y + 34, 26, TXT, bold=True, align="left", alpha=alpha)
    if sub:
        text(ctx, sub, x + 4, y + 88, 24, TXT2, align="left", alpha=alpha)

def faixa(ctx, titulo, sub, cor, alpha, y=800):
    if alpha <= 0.01:
        return
    sc = 0.94 + 0.06 * ease_out(alpha)
    ctx.save()
    ctx.translate(W / 2, y)
    ctx.scale(sc, sc)
    font(ctx, 46, True)
    w = ctx.text_extents(titulo).x_advance
    if sub:
        font(ctx, 26)
        w = max(w, ctx.text_extents(sub).x_advance)
    w = max(w, 300) + 120
    rrect(ctx, -w / 2, -44, w, 88 if not sub else 120, 18)
    ctx.set_source_rgba(cor[0] * 0.25, cor[1] * 0.25, cor[2] * 0.25, 0.94 * alpha)
    ctx.fill_preserve()
    ctx.set_source_rgba(cor[0], cor[1], cor[2], alpha)
    ctx.set_line_width(3)
    ctx.stroke()
    text(ctx, titulo, 0, 16, 46, hx("FFFFFF"), bold=True, alpha=alpha)
    if sub:
        text(ctx, sub, 0, 58, 26, TXT, alpha=alpha * 0.9)
    ctx.restore()

def callout(ctx, x, y, texto, cor, alpha, lado="left"):
    if alpha <= 0.01:
        return
    font(ctx, 24, True)
    w = ctx.text_extents(texto).x_advance + 36
    bx = x - w - 40 if lado == "left" else x + 40
    ctx.set_source_rgba(cor[0], cor[1], cor[2], alpha)
    ctx.set_line_width(2.5)
    ctx.move_to(x + (-36 if lado == "left" else 36), y)
    ctx.line_to(bx + (w if lado == "left" else 0), y)
    ctx.stroke()
    rrect(ctx, bx, y - 24, w, 48, 10)
    ctx.set_source_rgba(cor[0] * 0.2, cor[1] * 0.2, cor[2] * 0.2, 0.95 * alpha)
    ctx.fill_preserve()
    ctx.set_source_rgba(cor[0], cor[1], cor[2], alpha)
    ctx.stroke()
    text(ctx, texto, bx + w / 2, y + 9, 24, hx("FFFFFF"), bold=True, alpha=alpha)

def legenda(ctx, t):
    for a, b, s in NARRACAO:
        al = fade(t, a, a + 0.4, b - 0.4, b)
        if al <= 0.01:
            continue
        linhas = wrap(ctx, s, 34, 1480)
        lh = 46
        hbox = len(linhas) * lh + 34
        y0 = H - 40 - hbox
        rrect(ctx, W / 2 - 800, y0, 1600, hbox, 14)
        ctx.set_source_rgba(0, 0, 0, 0.72 * al)
        ctx.fill()
        for i, ln in enumerate(linhas):
            text(ctx, ln, W / 2, y0 + 17 + 34 + i * lh - 4, 34, hx("FFFFFF"), alpha=al)

def fundo(ctx):
    ctx.set_source_rgba(*BG)
    ctx.paint()
    ctx.set_source_rgba(*GRID)
    ctx.set_line_width(1)
    for x in range(0, W, 48):
        ctx.move_to(x + 0.5, 0)
        ctx.line_to(x + 0.5, H)
    for y in range(0, H, 48):
        ctx.move_to(0, y + 0.5)
        ctx.line_to(W, y + 0.5)
    ctx.stroke()

def vinheta(ctx):
    g = cairo.RadialGradient(W / 2, H / 2, H * 0.35, W / 2, H / 2, H * 1.05)
    g.add_color_stop_rgba(0, 0, 0, 0, 0)
    g.add_color_stop_rgba(1, 0, 0, 0, 0.55)
    ctx.set_source(g)
    ctx.paint()

def preto(ctx, a):
    if a > 0.001:
        ctx.set_source_rgba(0, 0, 0, clamp(a))
        ctx.paint()

def painel(ctx, st, x, y, s, titulo, sub, cor, alpha):
    pw, ph = 1920 * s, 700 * s
    rrect(ctx, x - 20, y - 20, pw + 40, ph + 150, 22)
    ctx.set_source_rgba(CARD[0], CARD[1], CARD[2], 0.9 * alpha)
    ctx.fill_preserve()
    ctx.set_source_rgba(cor[0], cor[1], cor[2], alpha)
    ctx.set_line_width(3)
    ctx.stroke()
    ctx.save()
    ctx.rectangle(x - 18, y - 18, pw + 36, ph + 10)
    ctx.clip()
    ctx.push_group()
    ctx.translate(x, y - 50 * s)
    ctx.scale(s, s)
    diagrama(ctx, st)
    ctx.pop_group_to_source()
    ctx.paint_with_alpha(alpha)
    ctx.restore()
    text(ctx, titulo, x + pw / 2, y + ph + 50, 44, cor, bold=True, alpha=alpha)
    text(ctx, sub, x + pw / 2, y + ph + 98, 32, TXT, bold=True, alpha=alpha)

# ---------------------------------------------------------------- quadro
def quadro(ctx, t, com_legenda):
    fundo(ctx)

    if t < 10.0:
        st = cena_abertura(t)
        diagrama(ctx, st)
        legenda_disj(ctx, ease(ramp(t, 4.5, 5.5)))
        tag(ctx, "Planta petroquímica · operação normal", VIVO, ease(ramp(t, 1.2, 2.2)))
        # título de abertura
        a = fade(t, 0.2, 1.0, 3.6, 4.4)
        if a > 0.01:
            ctx.set_source_rgba(BG[0], BG[1], BG[2], 0.85 * a)
            ctx.paint()
            text(ctx, "Antes e depois da proteção", W / 2, H / 2 - 10, 78, TXT, bold=True, alpha=a)
            text(ctx, "a mesma falha, duas vezes", W / 2, H / 2 + 56, 34, TXT2, alpha=a)
            ctx.set_source_rgba(VIVO[0], VIVO[1], VIVO[2], a)
            ctx.rectangle(W / 2 - 60, H / 2 + 104, 120, 3)
            ctx.fill()
            text(ctx, DISCENTES, W / 2, H / 2 + 160, 30, TXT, alpha=a)
        callout(ctx, FX["A"] - 90, FAULT_Y, "linha do reator VG-principal", FALHA, fade(t, 6.2, 6.8, 9.3, 9.9), lado="left")

    elif t < 30.0:
        st = cena_antes(t)
        diagrama(ctx, st)
        legenda_disj(ctx, 1.0)
        tag(ctx, "ANTES · proteção sem seletividade", FALHA, ease(ramp(t, 10.0, 10.8)))
        callout(ctx, FX["A"] - 90, FAULT_Y, "FALTA (curto recorrente)", FALHA, fade(t, 12.8, 13.3, 16.6, 17.2), lado="left")
        callout(ctx, B1[0] - 70, B1[1], "52-1 abre: entrada desligada", FALHA, fade(t, 16.7, 17.2, 29.0, 29.6), lado="left")
        faixa(ctx, "Planta inteira parada", "as três cargas desligadas por uma falha em um só alimentador", FALHA,
              ease_out(ramp(t, 18.4, 19.2)) * (1 - ease(ramp(t, 29.2, 29.8))), y=800)
        preto(ctx, ease(ramp(t, 29.4, 30.0)))

    elif t < 35.0:
        preto(ctx, 1.0)
        a = fade(t, 30.6, 31.4, 33.8, 34.5)
        text(ctx, "Com o esquema proposto", W / 2, H / 2 + 14, 72, TXT, bold=True, alpha=a)
        ctx.set_source_rgba(ABERTO[0], ABERTO[1], ABERTO[2], a)
        w = 220 * ease_out(ramp(t, 31.0, 32.0))
        ctx.rectangle(W / 2 - w / 2, H / 2 + 52, w, 5)
        ctx.fill()

    elif t < 60.0:
        st = cena_depois(t)
        diagrama(ctx, st)
        legenda_disj(ctx, 1.0)
        tag(ctx, "DEPOIS · proteção seletiva", ABERTO, ease(ramp(t, 35.2, 36.0)))
        callout(ctx, FX["A"] - 90, FAULT_Y, "mesma falta", FALHA, fade(t, 37.0, 37.5, 38.6, 39.0), lado="left")
        callout(ctx, FX["A"], BR_Y, "52-A abre em milissegundos", ABERTO, fade(t, 38.8, 39.3, 59.0, 59.6), lado="left")
        faixa(ctx, "Só o reator isolado", "o resto da planta continua operando", ABERTO,
              ease_out(ramp(t, 41.0, 41.8)) * (1 - ease(ramp(t, 59.2, 59.8))), y=800)
        preto(ctx, 1 - ease(ramp(t, 35.0, 35.7)))
        preto(ctx, ease(ramp(t, 59.5, 60.0)))

    else:
        a = ease(ramp(t, 60.2, 61.2))
        s = 0.42
        sa = cena_antes(29.0)
        sd = cena_depois(59.0)
        x0 = (W - (2 * (1920 * s + 40) + 60)) / 2 + 20
        painel(ctx, sa, x0, 250, s, "Antes", "planta parada", FALHA, ease(ramp(t, 60.2, 61.0)))
        painel(ctx, sd, x0 + 1920 * s + 100, 250, s, "Depois", "só o reator isolado", ABERTO, ease(ramp(t, 60.8, 61.6)))
        text(ctx, "Mesma falha, consequências diferentes", W / 2, 160, 48, TXT, bold=True, alpha=a)
        text(ctx, "Discentes: " + DISCENTES, W / 2, 780, 30, TXT2, alpha=ease(ramp(t, 62.0, 63.0)))
        preto(ctx, ease(ramp(t, 73.6, 75.0)))

    vinheta(ctx)
    if com_legenda:
        legenda(ctx, t)

def render(saida, com_legenda):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    ctx = cairo.Context(surf)
    proc = subprocess.Popen([
        "ffmpeg", "-y", "-loglevel", "error",
        "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
        "-f", "lavfi", "-t", str(DUR), "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-shortest", "-movflags", "+faststart", saida,
    ], stdin=subprocess.PIPE)
    n = int(DUR * FPS)
    for i in range(n):
        t = i / FPS
        ctx.save()
        quadro(ctx, t, com_legenda)
        ctx.restore()
        surf.flush()
        proc.stdin.write(bytes(surf.get_data()))
        if i % 300 == 0:
            print(f"{saida}: {i}/{n}", flush=True)
    proc.stdin.close()
    proc.wait()

def still(t, saida, com_legenda=True):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    ctx = cairo.Context(surf)
    quadro(ctx, t, com_legenda)
    surf.write_to_png(saida)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stills":
        for t in [float(x) for x in sys.argv[3:]]:
            still(t, f"{sys.argv[2]}/frame_{t:05.1f}.png")
    else:
        render("antes-e-depois-da-protecao-com-legenda.mp4", True)
        render("antes-e-depois-da-protecao-sem-legenda.mp4", False)
