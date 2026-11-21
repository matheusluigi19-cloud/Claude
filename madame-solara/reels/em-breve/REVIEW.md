# Revisão: teaser de suspense (Reels)

Arquivo final: `renders/madame-solara-em-breve.mp4` (1080x1920, 30 fps, 20 s, H.264 com áudio AAC).

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

Refeito com o Earshot, que descreve e mede áudio para quem não pode ouvir. As leituras abaixo são dele; gosto ele não mede.

- Trilha: "Majestic", de Diego Nava (Mixkit). Foram comparadas 63 faixas do Mixkit pelo som. No trecho de 20 s usado no vídeo, "Majestic" teve leitura forte para "lounge de praia calmo e sofisticado" (z +4,3) e para "música calma com batida lenta e teclas suaves" (z +4,2), e fraca para "música cinematográfica de teaser de moda de luxo" (z +2,3). A alternativa anterior, "One More Dance", ficou em 41º de 63 e foi retirada.
- O trecho começa 1,64 s dentro da faixa: o grave entra aos 9,65 s, quando a maré cruza o meio da tela, e a música abaixa pela metade por 0,4 s logo antes.
- Efeitos gerados com o Earshot: mar na abertura, com a onda maior quebrando aos 4,4 s, quando a luz toma a tela; outra onda com o pico na maré; uma batida grave na entrada do monograma. O Earshot leu os dois recortes de mar como onda de praia com leitura forte (z +5,0 e +4,1) e como som de gravação real (p_real 0,78 e 0,90).
- Sincronia (`earshot timeline`, marcações em `som/cues.json`): 82% das 11 entradas caem a até um quadro de um ataque do som, contra 27% que o acaso daria. Nenhuma ficou sem som; a da luz é um crescimento de nível, sem ataque.
- Crítica (`earshot critique`): "launch-grade", 21 de 22 métricas dentro da faixa de 7 filmes de lançamento profissionais. A única fora é a naturalidade do som (p_real 0,69, mínimo de 0,77), mais baixa na abertura e no fecho. A referência é de filmes de lançamento de produto, então vale como parâmetro e não como nota.
- Medido no arquivo final: -15,8 LUFS, pico real de -1,3 dBTP, faixa dinâmica de 4,9 LU. A abertura fica em -18 LUFS e o trecho depois da maré em -14 LUFS.
- A folha `som/folha-de-som.png` mostra quadros, eventos, espectrograma, volume e sincronia.
- Ninguém ouviu o resultado. A escuta final é de quem publica.

## Ponto mais fraco

- As três linhas de abertura da cena 3 ficam em 62 px para caber na largura; são legíveis no celular, mas são o texto mais miúdo do vídeo.
- As texturas de seda vêm das fotos do manual (no máximo 1112 x 1390 px) e foram ampliadas.

## Pendências

- Ouvir e aprovar a trilha, ou indicar outro clima para buscar outra faixa.
- Confirmar se o monograma MS pode aparecer no fecho ou se o suspense pede tirar também.
