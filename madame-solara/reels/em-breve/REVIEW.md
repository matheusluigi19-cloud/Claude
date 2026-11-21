# Revisão: teaser de suspense (Reels)

Arquivo final: `renders/madame-solara-em-breve.mp4` (1080x1920, 30 fps, 20 s, H.264, sem áudio).

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
- O arquivo não tem trilha. Nada de som foi avaliado. A ferramenta avisa que um vídeo de 20 s pede música.

## Ponto mais fraco

- As três linhas de abertura da cena 3 ficam em 62 px para caber na largura; são legíveis no celular, mas são o texto mais miúdo do vídeo.
- As texturas de seda vêm das fotos do manual (no máximo 1112 x 1390 px) e foram ampliadas.

## Pendências

- Trilha sonora: escolher a música no Instagram ao publicar, ou enviar um arquivo de áudio para entrar na composição.
- Confirmar se o monograma MS pode aparecer no fecho ou se o suspense pede tirar também.
