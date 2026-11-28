# Vídeos da loja

Três vídeos gravados na loja (IMG_5108, IMG_5109 e um segundo IMG_5108), só com o logo solto
(nome branco e sol dourado, com sombra), pequeno, embaixo e centralizado, desde o primeiro
quadro até o fim. Saem em `renders/` em 1080x1920, 30 fps, com o som original. Os originais não
estão no repositório.

Testes que saíram: selo e quadro creme (tampavam as peças) e a frase "venha conferir nossas peças
na Madame Dress!" em Montserrat branca (a cliente não gostou da fonte). A frase continua em
`sobreposicao.html` (`?camada=frase`), mas `montar.sh` não a usa.

O logo fica entre y 1360 e 1585, abaixo da área segura oficial do Reels (até y 1248), porque a
cliente pediu embaixo; pode ficar perto da legenda quando ela for longa.

Para refazer: `node exportar-camadas.js` (se mudar o texto em `sobreposicao.html`) e depois
`./montar.sh original.mov renders/saida.mp4`.

## Triconjunto (IMG_5114)

O mesmo logo, mais a frase "Triconjunto disponível no marrom e off white": "Triconjunto" em
Imperial Script e a linha de baixo em Italiana (com contorno da mesma cor, para engrossar o
traço), logo acima do logo. Três versões de cor da frase, para a cliente escolher:
`renders/madame-solara-triconjunto-azul.mp4`, `-dourado.mp4` e `-branco.mp4`.

Para refazer: `node exportar-triconjunto.js <cor> assets/camada-triconjunto-<cor>.png` e
`./montar.sh original.mov renders/saida.mp4 assets/camada-triconjunto-<cor>.png`.
