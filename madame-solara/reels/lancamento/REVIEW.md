# Revisão: vídeo de lançamento (Reels)

Arquivo final: `renders/madame-solara-lancamento.mp4` (1080x1920, 30 fps, 10,8 s, H.264 com áudio AAC).

## O que foi pedido e o que foi decidido

- Pedido: divulgar o lançamento da marca, com o logo, o fundo um pouco desfocado e uma edição no estilo CapCut como a de um vídeo modelo do TikTok, dinâmica, com fontes diferentes e som de teclado.
- O vídeo modelo não pôde ser aberto: o TikTok está fora da rede liberada nesta sessão. A edição segue a descrição do pedido, e não o modelo.
- Data: o pedido dizia "sábado, 29/11". Em 2026 o dia 29/11 cai em um domingo. A cliente confirmou sábado, 28/11, e é isso que está no vídeo.
- Fundo: o vídeo enviado pela cliente, com as peças embaladas e as etiquetas da marca, desacelerado para 78%, desfocado e escurecido para o texto se ler.
- Texto digitado letra a letra, com cursor, em três fontes: IBM Plex Mono nas linhas de apoio, Playfair Display itálico em "sábado," e na assinatura, e a Italiana da marca na data.
- Roteiro: "guarda essa data" / "sábado," / "28.11" / "lançamento oficial"; o texto é apagado; entra o logo; "sábado · 28.11" / "Você é o seu padrão!". Nenhuma informação além da data foi inventada (sem horário, endereço ou promoção).
- Som: uma tecla por letra, no instante em que ela aparece, sobre a trilha "Majestic", a mesma das outras peças. A data entra junto com o grave da música (2,10 s) e o logo em outra batida forte (6,16 s), com um pequeno salto do fundo nas duas.

## Como editar

Os textos e os tempos ficam no começo de `montar.py`. Ele gera `compositions/texto.html` e `assets/sfx/digitacao.wav` juntos, para a letra e a tecla nunca saírem de sincronia. Depois de rodar, é só renderizar.

## O que foi medido e o que só foi visto

- `hyperframes check --safe-zone reels`: 0 erros e 0 avisos. Todo o texto e o logo ficam dentro da área livre do Reels.
- Quadros do vídeo foram conferidos visualmente.
- O Earshot leu a faixa de digitação como teclado mecânico, com leitura forte (z +4,1; AudioSet "Typing" 0,61).
- Sincronia (`earshot timeline`, marcações em `som/cues.json`): a primeira tecla cai a 4 ms da primeira letra, a data a 17 ms do grave da música, o logo a 17 ms da batida e a última letra a 23 ms da batida final.
- Volume do teclado: na primeira medição as teclas ficaram 10 a 12 dB acima da música e a crítica apontou médios ásperos. O teclado foi reduzido em cerca de 4 dB para ficar ao fundo, e o aviso sumiu.
- Crítica (`earshot critique`): "launch-grade", 22 de 22 métricas na faixa de filmes de lançamento profissionais; naturalidade 0,95. A régua é de filme de lançamento de produto e vale como parâmetro.
- Medido no arquivo final: -15,7 LUFS, pico real de -1,0 dBTP.
- Ninguém ouviu o resultado. A escuta final é de quem publica.
