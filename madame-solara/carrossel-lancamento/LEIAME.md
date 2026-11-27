# Carrossel de lançamento

Sete imagens 4:5, em PNG de 2160x2700, para o Instagram, em `final/`, na ordem de postagem.

- Slide 1: biquíni amarelo e azul com o selo azul "peças a partir de R$ 53,00", todo em Montserrat.
- Slides 2 a 7: as demais fotos com o logo colorido num selo creme no canto de baixo à esquerda.

As fotos originais estão em `fotos/`, já giradas. As fotos 3:4 perderam cerca de 6% em cima e embaixo para caber em 4:5. A foto 6 (maiôs empilhados) é bem mais comprida que 4:5. Para não cortar o maiô marrom, ela aparece quase inteira (de 170 a 2300 px na altura) e sobram faixas de 80 px nos lados, preenchidas com a cor da mesa por `fundo-6.py`.

Para refazer um slide:

    node exportar.js "foto=fotos/foto-1.jpg&y=50&modo=preco" saida.png
    node exportar.js "foto=fotos/foto-6.jpg&modo=logo&faixa=170,2300&fundo=fotos/fundo-6.png" saida.png

`y` move o recorte na vertical (0 = topo, 100 = base).
