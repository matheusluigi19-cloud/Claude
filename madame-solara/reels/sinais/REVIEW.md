# Revisão: "Não ignore os sinais" (foto e Reels)

Quinta rodada. A cliente pediu a fonte da primeira foto (Italiana), o logo com o sol dourado e o nome em branco, e depois apontou que o dourado estava com baixa qualidade e que a frase e o logo estavam grandes demais para uma marca minimalista.

- Foto: `foto/nao-ignore-os-sinais.jpg` (2160x2880, proporção 3:4 do feed). Fonte editável em `foto/foto.html`.
- Vídeo: `renders/madame-solara-sinais.mp4` (1080x1920, 30 fps, 8 s, H.264 com áudio AAC). Não mudou nesta rodada: segue com Montserrat e o monograma MS com anel dourado.

## O que foi decidido

- A base é a imagem de referência enviada pela cliente. As nuvens foram recortadas do céu em quatro camadas transparentes, em `assets/nuvens/`, e o texto original saiu no recorte. O céu é um degradê refeito, um pouco menos saturado que o da referência.
- Foto: céu inteiro e o biquíni como protagonista. A frase vai em uma linha só, pequena e bem espaçada (Italiana, 46 px em 1080), e o logo vertical fica pequeno embaixo (210 px de largura). As nuvens do rodapé se abrem no centro para o logo ficar sobre o azul.
- Logo da foto (`assets/logo-vertical-ceu.svg`): os traços do logo vertical branco do manual, com o nome e a assinatura em branco e o sol preenchido por um degradê dourado claro. É vetor puro, sem recorte nem sombra.
- Qualidade do dourado: a versão anterior saía em JPEG com subamostragem de cor 4:2:0, que borra linhas finas e saturadas, e usava o sol do logo colorido, que é um degradê recortado. Agora o sol é traço vetorial e a foto é exportada em JPEG 4:4:4 com qualidade 96.
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
