#!/usr/bin/env bash
# Prepara o vídeo de fundo a partir do original da cliente (IMG_4938.mov, 1080x1920, 59,94 fps):
# desacelera para 49,8% (17 s; o vídeo usa 16,8 s), desfoca, escurece e fecha as bordas, e grava em 30 fps.
# O desfoque fica gravado no arquivo porque aplicado na hora deixava a renderização lenta demais.
# Uso: ./preparar-fundo.sh caminho/do/original.mov
set -euo pipefail
ffmpeg -v error -y -i "$1" -an \
  -vf "scale=1080:1920:flags=lanczos,setsar=1,setpts=PTS/0.4982,fps=30,gblur=sigma=8,eq=saturation=0.92,lutrgb=r='val*0.56':g='val*0.56':b='val*0.58',vignette=angle=PI/4.6" \
  -c:v libx264 -preset slow -crf 20 -pix_fmt yuv420p -movflags +faststart assets/video/pecas-fundo.mp4
