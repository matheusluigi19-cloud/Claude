#!/usr/bin/env bash
# Põe o selo com o logo e a frase por cima de um vídeo da loja e grava em 1080x1920, 30 fps,
# mantendo o som original.  Uso: ./montar.sh entrada.mov saida.mp4
# As camadas vêm de exportar-camadas.js (assets/camada-logo.png e assets/camada-frase.png).
set -euo pipefail
ffmpeg -v error -y -i "$1" \
  -framerate 30 -loop 1 -i assets/camada-logo.png \
  -framerate 30 -loop 1 -i assets/camada-frase.png \
  -filter_complex "\
[0:v]scale=1080:1920:flags=lanczos,setsar=1,fps=30[v];\
[1:v]format=rgba[l];\
[2:v]format=rgba[f];\
[v][l]overlay=shortest=1[a];[a][f]overlay=shortest=1,format=yuv420p[out]" \
  -map "[out]" -map 0:a -c:v libx264 -preset slow -crf 18 -profile:v high \
  -color_primaries bt709 -color_trc bt709 -colorspace bt709 \
  -c:a aac -b:a 192k -movflags +faststart -shortest "$2"
