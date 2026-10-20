# Aplicar a loja Madame Solara na Nuvemshop

O protótipo em `site/` (e o link publicado) mostra como a loja deve ficar. O que dá para levar para a Nuvemshop depende do plano.

## O que muda conforme o plano

- **Planos de entrada:** a loja usa um tema pronto da Nuvemshop. A personalização é pelo editor de layout (cores, fontes, banners, ordem das seções) e pelo campo "Edição avançada de CSS", que só muda o estilo de elementos que o tema já tem. Toldo, vitrine com moldura e araras com cabides não existem nos temas prontos; dá para chegar perto com banners e cores.
- **A partir do plano Escala:** acesso ao código do tema por FTP. Aí dá para reproduzir o protótipo inteiro. Ao ativar o FTP não é mais possível trocar de tema sem desativá-lo antes.

Fontes: [personalização avançada](https://atendimento.nuvemshop.com.br/personalizacao-avancada-do-layout/como-editar-o-codigo-do-layout-da-minha-loja), [o que dá para alterar por CSS](https://atendimento.nuvemshop.com.br/codigo-css/o-que-da-para-ser-alterado-por-css-nos-layouts-da-nuvemshop), [recursos de layout](https://www.nuvemshop.com.br/recursos/layout-loja-virtual). Conferir a página de planos atual, porque as regras podem mudar.

## Configurações do editor (qualquer plano)

| Onde | Valor |
|---|---|
| Fundo da loja | `#FCFDF5` (creme) |
| Texto | `#5E3416` (marrom) |
| Botões | fundo `#5E3416`, texto `#FCFDF5` |
| Destaques, faixa de aviso, rodapé | `#2F5D74` (azul escuro, aceita texto branco) |
| Cor da marca em blocos grandes | `#64A6C9` (azul claro; texto sobre ele em `#17323F`, nunca branco) |
| Fonte de títulos | Italiana (se o tema oferecer) |
| Fonte de texto | Work Sans (se o tema oferecer) |
| Logo | `identidade-visual/logos-e-elementos/logo-horizontal-colorido.png` |
| Ícone do navegador | `identidade-visual/logos-e-elementos/monograma-dourado.png` |

Se Italiana ou Work Sans não estiverem na lista de fontes do tema, a escolha da substituta depende do tema escolhido.

## Próximo passo

Escolher o plano e o tema. Com o tema definido, dá para escrever o CSS avançado para ele (as classes mudam de tema para tema) e preparar os banners nos tamanhos que o tema pede.
