# Revisão: "Não ignore os sinais" (foto e Reels)

Terceira rodada. A cliente recusou as três opções de tipografia da rodada anterior e pediu a fonte da primeira foto (Italiana) com o logo colorido completo: sol dourado, nome em azul e assinatura em marrom.

- Foto: `foto/nao-ignore-os-sinais.jpg` (2160x2880, proporção 3:4 do feed). Fonte editável em `foto/foto.html`.
- Vídeo: `renders/madame-solara-sinais.mp4` (1080x1920, 30 fps, 8 s, H.264 com áudio AAC). Não mudou nesta rodada: segue com Montserrat e o monograma MS com anel dourado.

## O que foi decidido

- A base é a imagem de referência enviada pela cliente. As nuvens foram recortadas do céu em quatro camadas transparentes, em `assets/nuvens/`, e o texto original saiu no recorte. O céu é um degradê refeito, um pouco menos saturado que o da referência.
- Foto: frase em Italiana no alto e biquíni no centro. O logo colorido tem letras azuis, que somem sobre o céu, então o quadro termina em creme: perto do rodapé o azul vira névoa e depois o creme da marca, com os topos das nuvens se desfazendo na passagem, e o logo vertical colorido fica sobre o creme.
- As nuvens do rodapé estão sem saturação na foto, porque sobre o creme a sombra azulada delas puxava para o rosa.
- Vídeo: um quadro só, com frase, biquíni e monograma juntos do começo ao fim. O biquíni é levado pelo vento e passa por dois campos de ruído que deslizam e deformam as bordas aos poucos, como nuvem; cada peça também respira e balança por conta própria. As nuvens do fundo e do rodapé andam em velocidades diferentes. Um reflexo corre pelo anel dourado aos 2,9 s e a estrela pisca aos 5,7 s.

## O que foi medido e o que só foi visto

- `hyperframes check --safe-zone reels`: 0 erros e 0 avisos. A frase fica dentro da área livre do Reels. O monograma vai até cerca de 1425 px, abaixo do limite de 1248 px que a Meta recomenda deixar livre, para manter a mesma ordem da foto; uma legenda longa aberta pode encostar nele.
- Quadros do vídeo e a foto final foram conferidos visualmente.

## Som do vídeo

- Trilha "Majestic", de Diego Nava (Mixkit), a mesma do teaser anterior. O trecho começa 11,2 s dentro da faixa, já na parte com batida.
- Brisa bem baixa nos primeiros 5 s, gerada com o Earshot. Créditos em `assets/audio/CREDITOS.md`.
- Sincronia (`earshot timeline`): o reflexo do anel cai a 3 ms de uma batida forte (2,92 s) e o piscar da estrela a 1 ms de outra (5,74 s).
- Crítica (`earshot critique`): "launch-grade", 17 de 17 métricas na faixa; naturalidade 0,87. Medido no arquivo final: -15,0 LUFS, pico real de -1,0 dBTP.
- Ninguém ouviu o resultado. A escuta final é de quem publica.

## Pontos de atenção

- Direito de uso: as nuvens saem da imagem de referência. Se ela veio de outra marca ou de banco de imagens, confirmar que pode ser usada antes de publicar.
- Resolução: a referência tem 1024x1536 px, então na foto de 2160 px as nuvens ficam mais suaves que o texto e o logo.
- Foto e vídeo estão com tipografia e marca diferentes. Levar o logo colorido para o vídeo pede uma base clara dentro da área livre do Reels, o que muda a composição.
