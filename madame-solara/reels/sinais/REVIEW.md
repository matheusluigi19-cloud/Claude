# Revisão: "Não ignore os sinais" (foto e Reels)

Duas peças com os mesmos elementos, para escolher a que funciona melhor:

- Foto: `foto/nao-ignore-os-sinais.jpg` (2160x2880, proporção 3:4 do feed). Fonte editável em `foto/foto.html`.
- Vídeo: `renders/madame-solara-sinais.mp4` (1080x1920, 30 fps, 10 s, H.264 com áudio AAC).

## O que foi decidido

- A base é a imagem de referência enviada pela cliente (céu azul com um biquíni de nuvens e a frase). As nuvens foram recortadas do céu em quatro camadas transparentes (parte de cima do biquíni, parte de baixo, nuvens finas e nuvens do rodapé), em `assets/nuvens/`. O texto original da imagem saiu no recorte.
- O céu é um degradê refeito a partir das cores medidas na imagem, um pouco menos saturado para chegar perto do azul da marca.
- A frase foi recomposta em Italiana, a fonte dos títulos da marca, e o logo horizontal branco assina as duas peças.
- Foto: frase no alto, biquíni no centro, logo embaixo. As nuvens do rodapé se abrem no centro para o logo ficar sobre o azul.
- Vídeo, um plano só: a frase já está na tela no quadro 0 (0 a 2,5 s); as nuvens se juntam e viram o biquíni (2,75 a 4 s); o biquíni sobe e encolhe e o logo entra (5,7 a 7 s). As camadas de nuvem andam com o vento em velocidades diferentes do início ao fim.

## O que foi medido e o que só foi visto

- `hyperframes check --safe-zone reels`: 0 erros e 0 avisos. Frase e logo ficam dentro da área livre do Reels.
- Quadros do vídeo e a foto final foram conferidos visualmente.

## Som do vídeo

- Trilha "Majestic", de Diego Nava (Mixkit), a mesma do teaser anterior, para as peças da campanha soarem iguais. O trecho começa 7,89 s dentro da faixa.
- Efeitos gerados com o Earshot: brisa nos primeiros 5 s, um sopro na formação do biquíni e uma batida grave no logo. Créditos em `assets/audio/CREDITOS.md`.
- Sincronia (`earshot timeline`): o grave da música cai a 6 ms da formação do biquíni (3,4 s) e a batida a 2 ms da entrada do logo (6,23 s).
- Crítica (`earshot critique`): "launch-grade", 22 de 22 métricas na faixa de filmes de lançamento profissionais; naturalidade do som 0,92. A régua é de filme de lançamento de produto, vale como parâmetro.
- Medido no arquivo final: -16,0 LUFS, pico real de -1,0 dBTP.
- Na primeira versão o Earshot leu a brisa como "carro passando". O volume dela foi reduzido a cerca de um terço e a leitura sumiu da descrição principal, mas "carro" ainda aparece como leitura secundária. Se o vento soar estranho, é o primeiro efeito a tirar.
- Ninguém ouviu o resultado. A escuta final é de quem publica.

## Pontos de atenção

- Direito de uso: as nuvens saem da imagem de referência. Se ela veio de outra marca ou de banco de imagens, confirmar que pode ser usada antes de publicar.
- Resolução: a imagem de referência tem 1024x1536 px. No vídeo as nuvens são ampliadas em até 25%, o que não aparece no celular; na foto de 2160 px elas ficam mais suaves que o texto e o logo.
