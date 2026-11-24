# Revisão: "Não ignore os sinais" (foto e Reels)

Sexta rodada. A cliente voltou ao layout da primeira foto (frase grande em duas linhas e biquíni grande) e pediu só a troca do logo de baixo e a imagem em alta qualidade.

- Foto: `foto/nao-ignore-os-sinais.png` (2160x2880, PNG sem perda, proporção 3:4 do feed), com o logo vertical. Variante com o logo horizontal no mesmo tamanho da primeira versão: `foto/nao-ignore-os-sinais-logo-horizontal.png`. Fonte editável em `foto/foto.html` (`?logo=horizontal` troca o logo).
- Vídeo: `renders/madame-solara-sinais.mp4` (1080x1920, 30 fps, 8 s, H.264 com áudio AAC). Não mudou nesta rodada: segue com Montserrat e o monograma MS com anel dourado.

## O que foi decidido

- A base é a imagem de referência enviada pela cliente. As nuvens foram recortadas do céu em quatro camadas transparentes, em `assets/nuvens/`, e o texto original saiu no recorte. O céu é um degradê refeito, um pouco menos saturado que o da referência.
- Foto: o layout da primeira versão, sem mudanças. Frase em Italiana em duas linhas no alto, biquíni grande no centro e o logo embaixo, com as nuvens do rodapé abertas no centro.
- Logo: os traços do logo branco do manual, com o nome e a assinatura em branco e o sol preenchido por um degradê dourado claro (`assets/logo-vertical-ceu.svg` e `assets/logo-horizontal-ceu.svg`). É vetor puro, sem recorte nem sombra. O pedido não dizia qual arranjo, então a versão principal usa o vertical, que foi o modelo enviado pela cliente, e a variante usa o horizontal.
- Alta qualidade: a imagem de referência (1024x1536 px) foi ampliada 4 vezes com o modelo de super-resolução Real-ESRGAN e as camadas de nuvem foram recortadas de novo a partir dela, em 2160 px de largura. Na foto elas entram ponto a ponto, sem ampliação. A exportação é PNG, sem compressão com perda.
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
- Super-resolução: o modelo reconstrói detalhe que não existia na imagem de 1024 px. As nuvens ficaram nítidas, mas o contorno delas é em parte invenção do modelo, o que em nuvem não incomoda.
- O vídeo ainda não foi renderizado de novo com as camadas em alta e continua com a fonte e o monograma antigos.
