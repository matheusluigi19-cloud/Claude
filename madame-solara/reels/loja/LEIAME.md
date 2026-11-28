# Vídeos da loja

Três vídeos gravados na loja (IMG_5108, IMG_5109 e um segundo IMG_5108), com o logo solto
(nome branco e sol dourado, com sombra) embaixo e centralizado, e a frase "venha conferir as
nossas peças na Madame Dress" em branco, sem fundo, no alto do quadro. A primeira versão tinha
selo creme e quadro creme, e a cliente achou que tampava as peças. Saem em `renders/` em
1080x1920, 30 fps, com o som original. Os originais não estão no repositório.

O logo entra aos 0,2 s e a frase aos 0,9 s, e os dois ficam até o fim. O logo fica entre y 1360 e
1585, abaixo da área segura oficial do Reels (até y 1248), porque a cliente pediu embaixo; pode
ficar perto da legenda quando ela for longa.

Para refazer: `node exportar-camadas.js` (se mudar o texto em `sobreposicao.html`) e depois
`./montar.sh original.mov renders/saida.mp4`.
