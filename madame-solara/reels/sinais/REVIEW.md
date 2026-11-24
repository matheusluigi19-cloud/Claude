# Revisão: "Não ignore os sinais" (foto e Reels)

Segunda rodada, depois do retorno da cliente: outra tipografia, só as iniciais no lugar do logo completo, com detalhes dourados, e o vídeo com tudo na tela desde o início e o biquíni se movendo como nuvem.

- Foto, três opções em 2160x2880 (3:4 do feed): `foto/opcao-1.jpg`, `foto/opcao-2.jpg` e `foto/opcao-3.jpg`. Comparativo em `foto/opcoes.jpg`. Fonte editável em `foto/foto.html` (`?op=2` mostra a opção 2).
- Vídeo: `renders/madame-solara-sinais.mp4` (1080x1920, 30 fps, 8 s, H.264 com áudio AAC).

## O que foi decidido

- A base é a imagem de referência enviada pela cliente. As nuvens foram recortadas do céu em quatro camadas transparentes, em `assets/nuvens/`, e o texto original saiu no recorte. O céu é um degradê refeito, um pouco menos saturado que o da referência.
- Opções da foto:
  1. Montserrat Bold em caixa alta, o desenho mais próximo da referência. Monograma creme com a estrela dourada.
  2. Playfair Display em caixa alta, serifa com peso. Monograma todo dourado.
  3. "Não ignore" pequeno em Montserrat e "os sinais" grande em Playfair itálico. Monograma creme com estrela e anel dourados.
- Vídeo: um quadro só, com frase, biquíni e monograma juntos do começo ao fim, na tipografia da opção 1 e com o monograma da opção 3. O biquíni é levado pelo vento e passa por dois campos de ruído que deslizam e deformam as bordas aos poucos, como nuvem; cada peça também respira e balança por conta própria. As nuvens do fundo e do rodapé andam em velocidades diferentes. Um reflexo corre pelo anel dourado aos 2,9 s e a estrela pisca aos 5,7 s.

## O que foi medido e o que só foi visto

- `hyperframes check --safe-zone reels`: 0 erros e 0 avisos. A frase fica dentro da área livre do Reels. O monograma vai até cerca de 1425 px, abaixo do limite de 1248 px que a Meta recomenda deixar livre, para manter a mesma ordem da foto; uma legenda longa aberta pode encostar nele.
- Quadros do vídeo e as três fotos foram conferidos visualmente.

## Som do vídeo

- Trilha "Majestic", de Diego Nava (Mixkit), a mesma do teaser anterior. O trecho começa 11,2 s dentro da faixa, já na parte com batida.
- Brisa bem baixa nos primeiros 5 s, gerada com o Earshot. Créditos em `assets/audio/CREDITOS.md`.
- Sincronia (`earshot timeline`): o reflexo do anel cai a 3 ms de uma batida forte (2,92 s) e o piscar da estrela a 1 ms de outra (5,74 s).
- Crítica (`earshot critique`): "launch-grade", 17 de 17 métricas na faixa; naturalidade 0,87. Medido no arquivo final: -15,0 LUFS, pico real de -1,0 dBTP.
- Ninguém ouviu o resultado. A escuta final é de quem publica.

## Pontos de atenção

- Direito de uso: as nuvens saem da imagem de referência. Se ela veio de outra marca ou de banco de imagens, confirmar que pode ser usada antes de publicar.
- Resolução: a referência tem 1024x1536 px, então nas fotos de 2160 px as nuvens ficam mais suaves que o texto e o monograma.
- O dourado sobre azul tem contraste baixo. Na opção 1 a estrela dourada é pequena e quase não se nota; o dourado aparece de verdade nas opções 2 e 3.
