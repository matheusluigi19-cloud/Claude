# Vídeos da loja

Três vídeos gravados na loja (IMG_5108, IMG_5109 e um segundo IMG_5108), com o selo do logo no alto
e a frase "venha conferir as nossas peças na Madame Dress" num quadro creme. Saem em
`renders/` em 1080x1920, 30 fps, com o som original. Os originais não estão no repositório.

O logo entra aos 0,2 s e a frase aos 0,9 s, e os dois ficam até o fim. A frase termina antes de
y 1248, para não ficar embaixo da legenda do Reels.

Para refazer: `node exportar-camadas.js` (se mudar o texto em `sobreposicao.html`) e depois
`./montar.sh original.mov renders/saida.mp4`.
