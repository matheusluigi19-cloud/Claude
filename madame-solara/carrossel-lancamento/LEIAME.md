# Carrossel de lançamento

Sete imagens 4:5 (exportadas a 2160x2700) para o Instagram, em `final/`, na ordem de postagem.

- Slide 1: biquíni amarelo e azul com o selo azul "peças a partir de R$ 53,00".
- Slides 2 a 7: as demais fotos com o logo colorido num selo creme no canto de baixo à esquerda.

As fotos originais estão em `fotos/`, já giradas. As fotos 3:4 perderam cerca de 6% em cima e embaixo para caber em 4:5. A foto 6 (maiôs empilhados) era 9:16 e foi recortada mais: sai o topo do maiô marrom e a etiqueta dele.

Para refazer um slide:

    node exportar.js "foto=fotos/foto-1.jpg&y=50&modo=preco" saida.png
    node exportar.js "foto=fotos/foto-6.jpg&y=58&modo=logo" saida.png

`y` move o recorte na vertical (0 = topo, 100 = base).
