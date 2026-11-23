"""Instantes (s) de cada evento do vídeo. Usado por gerar_video.py e dublar.py."""
DUR = 38.8

N1 = 0.8          # fala 1: planta operando
ANTES = 8.1       # entra a parte "Antes"
FALHA_A = 8.3     # curto (antes)
N2 = 8.7          # fala 2
TRIP_A = 10.6     # 52-1 abre (proteção da entrada, lenta)
FAIXA_A = 11.3    # "Planta inteira parada"
TRANS = 16.5      # tela "Com o esquema proposto"
DEPOIS = 18.3     # volta o diagrama, parte "Depois"
FALHA_D = 19.3    # mesmo curto
TRIP_D = 19.6     # 52-A abre
N3 = 19.8         # fala 3
FAIXA_D = 21.2    # "Só o reator isolado"
FIM_D = 30.2      # fim da parte "Depois"
N4 = 30.9         # fala 4 (fechamento)

FALAS_INICIO = [N1, N2, N3, N4]
