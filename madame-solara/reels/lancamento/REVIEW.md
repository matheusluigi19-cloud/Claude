# Revisão: vídeo de lançamento (Reels)

Arquivos: `renders/madame-solara-lancamento-musica-1-every-24th-of-august.mp4` e `renders/madame-solara-lancamento-musica-2-oh-barcelona.mp4` (1080x1920, 30 fps, 16,8 s, H.264 com áudio AAC). São o mesmo vídeo com duas trilhas, para a cliente escolher.

## O que foi pedido e o que foi decidido

- Pedido: divulgar o lançamento da marca, com o logo, o fundo um pouco desfocado e uma edição no estilo CapCut de um vídeo modelo do TikTok, dinâmica, com fontes diferentes e som de teclado.
- Primeira versão: feita sem ver o modelo, porque o TikTok está fora da rede liberada. Era só texto digitado em fonte de máquina. Foi substituída.
- Segunda versão: a cliente enviou o arquivo do vídeo modelo e o vídeo foi refeito como título compacto (etiqueta pequena, palavra cursiva grande e linha digitada). Tinha 10,8 s. O arquivo do modelo não está no repositório.
- Terceira versão (a atual), a partir dos comentários da cliente sobre a segunda:
  - Estava curto e rápido demais para ler. Passou de 10,8 s para 18,6 s e depois foi fechado em 16,8 s, porque a cliente pediu no máximo 17 s.
  - O texto estava alto no quadro. O conjunto agora fica no meio da tela.
  - As linhas digitadas ("28 de novembro", "oficial da marca", "sábado · 28.11") saíram do itálico fino. Uma tentativa em Playfair Display 800 maiúscula foi recusada; a cliente pediu a mesma fonte de "anota aí" e da assinatura, então elas estão em Montserrat 700, em minúsculas, e a data da primeira tela ficou menor (42 px).
  - A fileira de estrelinhas foi removida.
  - A trilha estava batida demais. Entrou um instrumental de violão com percussão leve ("Ocean of Love").
- Data: o pedido original dizia "sábado, 29/11". Em 2026 o dia 29/11 cai em um domingo. A cliente confirmou sábado, 28/11.
- Fundo: o vídeo enviado pela cliente, com as peças embaladas e as etiquetas da marca, desacelerado para cerca de 50% da velocidade, desfocado e escurecido.
- Três telas. A cliente pediu a frase "na loja da Madame Dress"; uma tela "com promoções imperdíveis" foi testada e ela não gostou, então saiu.
  1. "anota aí:" / "Sábado" / "28 de novembro"
  2. "é dia de:" / "Lançamento" / "oficial da marca" / "na loja da Madame Dress"
  3. o logo, "sábado · 28.11" digitado e a assinatura "você é o seu padrão!"
- Fontes: Imperial Script na palavra cursiva, Montserrat 700 nas etiquetas, nas linhas digitadas e na assinatura. As cores são as da marca (creme e dourado claro); o modelo usa rosa.
- Data e local vêm da cliente. Nada além disso foi inventado (sem horário, endereço ou valores).
- Som: uma tecla por letra digitada, no instante em que ela aparece, mais teclas rápidas e baixas quando a palavra cursiva entra, sobre a trilha.

## Como a trilha foi escolhida

A cliente achou a primeira trilha ("Majestic") batida demais e a segunda ("Ocean of Love") sem graça e lenta. Cerca de 125 faixas do Mixkit foram ranqueadas pelo Earshot contra descrições de samba, bossa animada e violão latino de praia, e contra descrições do que ela não quer (lento, eletrônico pesado, música de fundo corporativa). Quatro foram enviadas como opção. Ela pediu então dois vídeos:

1. "Every 24th of August" (112 bpm), a primeira das quatro opções, agora com as trocas de tela nas batidas.
2. "Oh Barcelona" (123 bpm), uma faixa nova, de violão com percussão, mais rápida.

Nas duas, as trocas de tela e o início de cada linha digitada caem em batidas medidas no trecho usado. São faixas de banco de música, e não gravações de MPB de artista conhecido.

## Como editar

Os textos e os tempos ficam no começo de `montar.py`. Ele gera `compositions/texto.html` e `assets/sfx/digitacao.wav` juntos, para a letra e a tecla nunca saírem de sincronia. Rode com o nome da variante (`python montar.py oh-barcelona`), porque os tempos de cada uma seguem a sua música; ele também aponta o `index.html` para a trilha certa. Se a duração mudar, `preparar-fundo.sh` refaz o fundo no tamanho novo. Depois é só renderizar.

## O que foi medido e o que só foi visto

- `hyperframes check --safe-zone reels`: 0 erros e 0 avisos. Todo o texto e o logo ficam dentro da área livre do Reels.
- Quadros foram conferidos visualmente nas três telas.
- Medido nos arquivos finais: -17,6 LUFS e pico real de -1,4 dBTP na música 1; -17,5 LUFS e -1,7 dBTP na música 2.
- Teclado: picos em torno de -13 dBFS sobre uma música com média perto de -19 dBFS, ou seja, dá para notar, mas fica ao fundo.
- Ninguém ouviu o resultado. A escuta final é de quem publica.

## Diferenças em relação ao modelo

- O modelo tem narração e não escurece o fundo; aqui não há voz e o fundo foi escurecido para o texto se ler sobre as embalagens claras.
- A fonte cursiva do modelo não foi identificada. A Imperial Script foi a mais parecida entre seis testadas que tinha boa leitura em tela pequena.
