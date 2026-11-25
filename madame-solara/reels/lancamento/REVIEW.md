# Revisão: vídeo de lançamento (Reels)

Arquivo final: `renders/madame-solara-lancamento.mp4` (1080x1920, 30 fps, 10,8 s, H.264 com áudio AAC).

## O que foi pedido e o que foi decidido

- Pedido: divulgar o lançamento da marca, com o logo, o fundo um pouco desfocado e uma edição no estilo CapCut de um vídeo modelo do TikTok, dinâmica, com fontes diferentes e som de teclado.
- Primeira versão: feita sem ver o modelo, porque o TikTok está fora da rede liberada. Era só texto digitado em fonte de máquina. Foi substituída.
- Segunda versão (a atual): a cliente enviou o arquivo do vídeo modelo. O estilo dele é um título compacto no centro, com uma etiqueta pequena sem serifa, uma palavra grande em letra cursiva com floreios, uma linha em itálico digitada letra a letra e uma fileira de brilhos. O vídeo foi refeito nesse formato. O arquivo do modelo não está no repositório.
- Data: o pedido original dizia "sábado, 29/11". Em 2026 o dia 29/11 cai em um domingo. A cliente confirmou sábado, 28/11.
- Fundo: o vídeo enviado pela cliente, com as peças embaladas e as etiquetas da marca, desacelerado para 78%, desfocado e escurecido. Ele muda de enquadramento nas trocas de tela, como cortes.
- Três telas, trocadas nas batidas fortes da música:
  1. "anota aí:" / "Sábado" / "28 de novembro"
  2. "é dia de:" / "Lançamento" / "oficial da marca"
  3. o logo, "sábado · 28.11" digitado e a assinatura "você é o seu padrão!"
- Fontes: Imperial Script na palavra cursiva, Montserrat nas etiquetas e na assinatura, Playfair Display itálico nas linhas digitadas. As cores são as da marca (creme e dourado claro); o modelo usa rosa.
- Nenhuma informação além da data foi inventada (sem horário, endereço ou promoção).
- Som: uma tecla por letra digitada, no instante em que ela aparece, mais teclas rápidas e baixas quando a palavra cursiva entra, sobre a trilha "Majestic", a mesma das outras peças.

## Como editar

Os textos e os tempos ficam no começo de `montar.py`. Ele gera `compositions/texto.html` e `assets/sfx/digitacao.wav` juntos, para a letra e a tecla nunca saírem de sincronia. Depois de rodar, é só renderizar.

## O que foi medido e o que só foi visto

- `hyperframes check --safe-zone reels`: 0 erros e 0 avisos. Todo o texto e o logo ficam dentro da área livre do Reels.
- Quadros do vídeo final foram conferidos visualmente e comparados com os do modelo.
- Sincronia (`earshot timeline`, marcações em `som/cues.json`): a primeira tecla cai a 17 ms da entrada da etiqueta, a última letra da data a 3 ms da batida de 6,16 s e a última letra da assinatura a 4 ms da batida de 8,99 s.
- O Earshot lê o teclado no arquivo final (AudioSet: teclado de computador, digitação, máquina de escrever), ao fundo da música.
- Crítica (`earshot critique`): "launch-grade", 23 de 23 métricas na faixa de filmes de lançamento profissionais; naturalidade 0,97. A régua é de filme de lançamento de produto e vale como parâmetro.
- Medido no arquivo final: -15,9 LUFS, pico real de -1,3 dBTP.
- Ninguém ouviu o resultado. A escuta final é de quem publica.

## Diferenças em relação ao modelo

- O modelo tem narração e não escurece o fundo; aqui não há voz e o fundo foi escurecido para o texto se ler sobre as embalagens claras.
- A fonte cursiva do modelo não foi identificada. A Imperial Script foi a mais parecida entre seis testadas que tinha boa leitura em tela pequena.
