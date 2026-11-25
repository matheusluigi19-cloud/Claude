# Revisão: vídeo de lançamento (Reels)

Arquivo final: `renders/madame-solara-lancamento.mp4` (1080x1920, 30 fps, 17 s, H.264 com áudio AAC).

## O que foi pedido e o que foi decidido

- Pedido: divulgar o lançamento da marca, com o logo, o fundo um pouco desfocado e uma edição no estilo CapCut de um vídeo modelo do TikTok, dinâmica, com fontes diferentes e som de teclado.
- Primeira versão: feita sem ver o modelo, porque o TikTok está fora da rede liberada. Era só texto digitado em fonte de máquina. Foi substituída.
- Segunda versão: a cliente enviou o arquivo do vídeo modelo e o vídeo foi refeito como título compacto (etiqueta pequena, palavra cursiva grande e linha digitada). Tinha 10,8 s. O arquivo do modelo não está no repositório.
- Terceira versão (a atual), a partir dos comentários da cliente sobre a segunda:
  - Estava curto e rápido demais para ler. Passou de 10,8 s para 18,6 s e depois foi fechado em 17 s, o máximo que a cliente pediu.
  - O texto estava alto no quadro. O conjunto agora fica no meio da tela.
  - As linhas digitadas ("28 de novembro", "oficial da marca", "sábado · 28.11") saíram do itálico fino. Uma tentativa em Playfair Display 800 maiúscula foi recusada; a cliente pediu a mesma fonte de "anota aí" e da assinatura, então elas estão em Montserrat 700, em minúsculas, e a data da primeira tela ficou menor (42 px).
  - A fileira de estrelinhas foi removida.
  - A trilha estava batida demais. Entrou um instrumental de violão com percussão leve ("Ocean of Love").
- Data: o pedido original dizia "sábado, 29/11". Em 2026 o dia 29/11 cai em um domingo. A cliente confirmou sábado, 28/11.
- Fundo: o vídeo enviado pela cliente, com as peças embaladas e as etiquetas da marca, desacelerado para cerca de 50% da velocidade, desfocado e escurecido.
- Quatro telas (a cliente pediu para testar as frases "lançamento oficial da marca na loja da Madame Dress" e "com promoções imperdíveis"):
  1. "anota aí:" / "Sábado" / "28 de novembro"
  2. "é dia de:" / "Lançamento" / "oficial da marca" / "na loja da Madame Dress"
  3. "com" / "Promoções" / "imperdíveis"
  4. o logo, "sábado · 28.11" digitado e a assinatura "você é o seu padrão!"
- Fontes: Imperial Script na palavra cursiva, Montserrat 700 nas etiquetas, nas linhas digitadas e na assinatura. As cores são as da marca (creme e dourado claro); o modelo usa rosa.
- Data, local e promoções vêm da cliente. Nada além disso foi inventado (sem horário, endereço ou valores).
- Som: uma tecla por letra digitada, no instante em que ela aparece, mais teclas rápidas e baixas quando a palavra cursiva entra, sobre a trilha.

## Como a trilha foi escolhida

Candidatas instrumentais do Mixkit foram baixadas e ordenadas pelo Earshot, que compara o áudio com descrições em texto. "Ocean of Love" ficou na frente para bossa nova, violão, samba e dedilhado, e não bateu com a descrição de batida pesada. É uma faixa de banco de música com cara de bossa e praia, e não uma gravação de MPB de artista conhecido.

A cliente não gostou dessa trilha. Quatro opções mais animadas foram enviadas para ela escolher ("Every 24th of August", "Spanish Heart", "Cherry on Top" e "Wherever You Are", todas de Michael Ramir C., no Mixkit). Até a escolha, o arquivo final continua com "Ocean of Love".

## Como editar

Os textos e os tempos ficam no começo de `montar.py`. Ele gera `compositions/texto.html` e `assets/sfx/digitacao.wav` juntos, para a letra e a tecla nunca saírem de sincronia. Se a duração mudar, `preparar-fundo.sh` refaz o fundo no tamanho novo. Depois é só renderizar.

## O que foi medido e o que só foi visto

- `hyperframes check --safe-zone reels`: 0 erros e 0 avisos. Todo o texto e o logo ficam dentro da área livre do Reels.
- Quadros foram conferidos visualmente nas quatro telas.
- Medido no arquivo final: -16,8 LUFS, pico real de -1,0 dBTP.
- Teclado: picos em torno de -13 dBFS sobre uma música com média perto de -19 dBFS, ou seja, dá para notar, mas fica ao fundo.
- Ninguém ouviu o resultado. A escuta final é de quem publica.

## Diferenças em relação ao modelo

- O modelo tem narração e não escurece o fundo; aqui não há voz e o fundo foi escurecido para o texto se ler sobre as embalagens claras.
- A fonte cursiva do modelo não foi identificada. A Imperial Script foi a mais parecida entre seis testadas que tinha boa leitura em tela pequena.
