# Revisão: teaser de suspense (Reels)

Arquivos finais (1080x1920, 30 fps, 20 s, H.264 com áudio AAC):

- `renders/madame-solara-em-breve.mp4`: trilha "Majestic", de Diego Nava. É a versão do projeto.
- `renders/madame-solara-em-breve-trilha-b.mp4`: mesma imagem com a trilha "One More Dance", de Arulo.

## O que foi decidido

- O vídeo é um suspense do lançamento, então o nome e o logo completo da Madame Solara (com "Moda praia & resort") não aparecem. Da marca nova só entram o sol do logo, na cena 1, e o monograma MS, no fecho.
- Roteiro enviado pela cliente, usado na íntegra:
  - Cena 1, aurora (0 a 4,9 s): "Uma nova fase. Um novo sol." O sol nasce por trás das ondas e a luz toma a tela.
  - Cena 2, capítulo (4,45 a 10,3 s): "A Madame Dress está crescendo e nossa história ganha um novo capítulo.", sobre a seda creme do manual.
  - Cena 3, mergulho (9,2 a 20 s): a maré azul sobe; "Agora, além da moda feminina, vamos mergulhar em um universo de sol, mar, liberdade e estilo.", com as quatro palavras entrando uma por vez; depois "Aguardem!" e o monograma.
- Tipografia: Italiana em todo o texto. Conteúdo centralizado no quadro, um pouco acima do meio exato. A moldura dourada da cena 2 foi retirada a pedido.

## O que foi medido e o que só foi visto

- `hyperframes check --safe-zone reels`: 0 erros. Os 4 avisos de contraste e de texto encoberto são do instante 10 s, quando a maré está cobrindo o texto da cena 2 de propósito.
- Linhas que passam do limite de 1248 px que a Meta recomenda deixar livre, aceitas de propósito por causa da centralização: "um novo capítulo." (até 1236 px, dentro), "liberdade" e "e estilo." (até 1366 px). Uma legenda longa aberta no Reels pode encostar nelas.
- Quadros extraídos do MP4 final foram conferidos visualmente.

## Som

- Trilhas do Mixkit, sob a Mixkit Stock Music Free License (uso comercial, redes sociais e anúncios online permitidos). Efeitos da biblioteca da skill media-use, sob a Pixabay Content License. Detalhes em `assets/audio/CREDITOS.md`.
- Ninguém ouviu o resultado: as faixas foram escolhidas pelo gênero e pelo clima informados no Mixkit e por medição (andamento, timbre e curva de energia). Vale a escuta de quem publica.
- "Majestic" (lounge, 113 bpm): o trecho começa 1,4 s dentro da faixa. A introdução acompanha o sol, uma camada nova entra perto da virada para a seda creme, e o grave entra aos 9,9 s, com a maré já cobrindo a tela. As linhas e as quatro palavras da cena 3 entram na grade da batida (0,529 s).
- "One More Dance" (pop suave, 110 bpm): começa 0,1 s depois do início e o grave entra aos 9,7 s. Só o deslocamento foi ajustado; as entradas de texto seguem a grade da outra faixa.
- Dois efeitos: um sopro longo com o pico aos 4,3 s, na luz que toma a tela, e um curto aos 9,65 s, na subida da maré.
- Medido no arquivo final: versão principal em -16,4 LUFS com pico de -1,0 dBFS; alternativa em -15,9 LUFS com pico de -1,0 dBFS.
- Para trocar a trilha do projeto, mude o `src` do `<audio id="musica">` em `index.html` para `assets/audio/one-more-dance.mp3`, com `data-start="0.1"` e `data-duration="19.9"`.

## Ponto mais fraco

- As três linhas de abertura da cena 3 ficam em 62 px para caber na largura; são legíveis no celular, mas são o texto mais miúdo do vídeo.
- As texturas de seda vêm das fotos do manual (no máximo 1112 x 1390 px) e foram ampliadas.

## Pendências

- Escolher entre as duas trilhas ouvindo, ou indicar outro clima para buscar outra faixa.
- Confirmar se o monograma MS pode aparecer no fecho ou se o suspense pede tirar também.
