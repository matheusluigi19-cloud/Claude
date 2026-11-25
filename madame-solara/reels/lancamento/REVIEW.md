# Revisão: vídeo de lançamento (Reels)

Arquivos (1080x1920, 30 fps, 15,6 s, H.264 com áudio AAC): `renders/madame-solara-lancamento-com-musica.mp4`, com a trilha "You're like Caviar", e `renders/madame-solara-lancamento-so-teclado.mp4`, o mesmo vídeo só com o som do teclado, para a cliente pôr a música dentro do Instagram.

## O que foi pedido e o que foi decidido

- Pedido: divulgar o lançamento da marca, com o logo, o fundo um pouco desfocado e uma edição no estilo CapCut de um vídeo modelo do TikTok, dinâmica, com fontes diferentes e som de teclado.
- Primeira versão: feita sem ver o modelo, porque o TikTok está fora da rede liberada. Era só texto digitado em fonte de máquina. Foi substituída.
- Segunda versão: a cliente enviou o arquivo do vídeo modelo e o vídeo foi refeito como título compacto (etiqueta pequena, palavra cursiva grande e linha digitada). Tinha 10,8 s. O arquivo do modelo não está no repositório.
- Terceira versão (a atual), a partir dos comentários da cliente sobre a segunda:
  - Estava curto e rápido demais para ler. Passou de 10,8 s para 18,6 s e depois foi fechado abaixo de 17 s, o máximo que a cliente pediu. Hoje tem 15,6 s.
  - O texto estava alto no quadro. O conjunto agora fica no meio da tela.
  - As linhas digitadas ("28 de novembro", "oficial da marca", "sábado · 28.11") saíram do itálico fino. Uma tentativa em Playfair Display 800 maiúscula foi recusada; a cliente pediu a mesma fonte de "anota aí" e da assinatura, então elas estão em Montserrat 700, em minúsculas, e a data da primeira tela ficou menor (42 px).
  - A fileira de estrelinhas foi removida.
  - A trilha estava batida demais. Entrou um instrumental de violão com percussão leve ("Ocean of Love").
- Data: o pedido original dizia "sábado, 29/11". Em 2026 o dia 29/11 cai em um domingo. A cliente confirmou sábado, 28/11.
- Fundo: o vídeo enviado pela cliente, com as peças embaladas e as etiquetas da marca, desacelerado para cerca de 50% da velocidade, desfocado e escurecido.
- Três telas. Uma linha "na loja da Madame Dress" e uma tela "com promoções imperdíveis" foram testadas a pedido da cliente e depois retiradas por ela.
  1. "anota aí:" / "Sábado" / "28 de novembro"
  2. "é dia de:" (centralizado, a pedido) / "Lançamento" / "oficial da marca"
  3. o logo, "sábado · 28.11" digitado e a assinatura "você é o seu padrão!", que foi aumentada para 42 px
- Fontes: Imperial Script na palavra cursiva, Montserrat 700 nas etiquetas, nas linhas digitadas e na assinatura. As cores são as da marca (creme e dourado claro); o modelo usa rosa.
- Nenhuma informação além da data foi inventada (sem horário, endereço ou promoção).
- Som: uma tecla por letra digitada, no instante em que ela aparece, mais teclas rápidas e baixas quando a palavra cursiva entra, sobre a trilha.

## Como a trilha foi escolhida

A trilha é o ponto que ainda não fechou. A cliente recusou, nesta ordem: "Majestic" (batida demais), "Ocean of Love" (sem graça e lenta), e "Every 24th of August" e "Oh Barcelona" (violão latino animado, que para ela não combinou com o vídeo nem com a marca). As escolhas são feitas por ranqueamento do Earshot contra descrições em texto e por medição de andamento, sem ninguém ouvir, o que explica os erros.

A tentativa atual muda de direção: "You're like Caviar", um lounge com cara de resort, com batida mais leve que a de "Majestic". As trocas de tela e o início de cada linha digitada caem em batidas medidas no trecho usado.

Depois disso a cliente pediu uma pesquisa de instrumentais de praia usadas nas redes. As indicadas ("Summer Samba", "Wave", "Sunset Lover") são gravações comerciais, que não podem ser embutidas no arquivo; só entram pelo Instagram. Para ela ouvir algo na mesma linha, foram enviados três testes com faixas licenciadas: "Poquito" (bossa de praia), "Pop 07" (bossa lo-fi) e "Pop 11" (eletrônica suave). Os vídeos de teste não estão no repositório, só as trilhas e as variantes em `montar.py`.

Como alternativa, a versão só com teclado serve para a cliente escolher a música na biblioteca do Instagram, ouvindo, o que também é o único caminho para usar uma gravação de MPB de verdade.

## Como editar

Os textos e os tempos ficam no começo de `montar.py`. Ele gera `compositions/texto.html` e `assets/sfx/digitacao.wav` juntos, para a letra e a tecla nunca saírem de sincronia. Rode com o nome da variante (`python montar.py youre-like-caviar`), porque os tempos de cada uma seguem a sua música; ele também aponta o `index.html` para a trilha certa. Se a duração mudar, `preparar-fundo.sh` refaz o fundo no tamanho novo. Depois é só renderizar.

## O que foi medido e o que só foi visto

- `hyperframes check --safe-zone reels`: 0 erros e 0 avisos. Todo o texto e o logo ficam dentro da área livre do Reels.
- Quadros foram conferidos visualmente nas três telas.
- Medido nos arquivos finais: -17,4 LUFS e pico real de -1,8 dBTP na versão com música; -20,5 LUFS e -6,4 dBTP na versão só com teclado.
- Teclado: picos em torno de -13 dBFS sobre uma música com média perto de -19 dBFS, ou seja, dá para notar, mas fica ao fundo.
- Ninguém ouviu o resultado. A escuta final é de quem publica.

## Diferenças em relação ao modelo

- O modelo tem narração e não escurece o fundo; aqui não há voz e o fundo foi escurecido para o texto se ler sobre as embalagens claras.
- A fonte cursiva do modelo não foi identificada. A Imperial Script foi a mais parecida entre seis testadas que tinha boa leitura em tela pequena.
