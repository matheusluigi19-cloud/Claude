---
name: Madame Solara
description: Loja de moda praia e resort montada como a fachada da loja física.
colors:
  creme: "#FCFDF5"
  parede: "#F7F3E8"
  azul: "#64A6C9"
  azul-logo: "#5598B3"
  azul-fundo: "#2F5D74"
  marinho: "#17323F"
  marrom: "#5E3416"
  marrom-suave: "#7A5A44"
  ouro: "#A57D2C"
  ouro-claro: "#C9A132"
  ouro-escuro: "#7A4E1C"
typography:
  display:
    fontFamily: "Italiana, Didot, serif"
    fontSize: "clamp(2rem, 4.4vw, 3.4rem)"
    fontWeight: 400
    lineHeight: 1.05
    letterSpacing: "0.01em"
  titulo-pagina:
    fontFamily: "Italiana, Didot, serif"
    fontSize: "clamp(2.6rem, 6vw, 4.6rem)"
    fontWeight: 400
    lineHeight: 1.05
  body:
    fontFamily: "Work Sans, system-ui, sans-serif"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.6
  rotulo:
    fontFamily: "Work Sans, system-ui, sans-serif"
    fontSize: "0.8rem"
    fontWeight: 400
    letterSpacing: "0.16em"
rounded:
  sm: "4px"
  md: "6px"
  pilula: "999px"
spacing:
  pagina-lateral: "clamp(16px, 4vw, 48px)"
  secao: "clamp(56px, 7vw, 96px)"
  grade: "clamp(16px, 2.4vw, 32px)"
components:
  botao-principal:
    backgroundColor: "{colors.marrom}"
    textColor: "{colors.creme}"
    rounded: "{rounded.sm}"
    padding: "0 22px"
    height: "46px"
  botao-principal-hover:
    backgroundColor: "{colors.ouro-escuro}"
  botao-claro:
    backgroundColor: "transparent"
    textColor: "{colors.marrom}"
    rounded: "{rounded.sm}"
  tamanho:
    textColor: "{colors.azul-fundo}"
    size: "40px"
    rounded: "50%"
  tamanho-selecionado:
    backgroundColor: "{colors.azul-fundo}"
    textColor: "{colors.creme}"
  filtro:
    textColor: "{colors.azul-fundo}"
    rounded: "{rounded.pilula}"
    padding: "8px 16px"
  filtro-ativo:
    backgroundColor: "{colors.azul-fundo}"
    textColor: "{colors.creme}"
---

# Design System: Madame Solara

## Overview

A loja online é a fachada da loja física vista da calçada. O letreiro leva o logo original, um toldo azul de borda recortada abre a vitrine, e a vitrine é uma janela de moldura dourada onde as peças ficam em expositores e já podem ser compradas, com tamanho e botão ali mesmo. Abaixo, cada categoria é uma arara: um trilho dourado com cabides de onde pendem os cartões das peças. A identidade vem do manual de marca da cliente (logo, monograma MS, sol com ondas e pontinhos, paleta); o sistema só traduz esse material para tela.

As peças aparecem como croquis técnicos de moda (desenho plano, traço fino na cor da peça) até existirem fotos. São material provisório e devem ser trocados pelas fotos reais, mantendo o campo de cor clara atrás de cada peça.

## Colors

### Primary
- **Azul Solara** (`#64A6C9`): o azul de fundo do manual. Ocupa regiões inteiras: toldo, bloco "Visite a loja". Nunca leva texto branco; o texto sobre ele é Marinho.
- **Azul Logo** (`#5598B3`): bordas de seletores e acentos finos.

### Secondary
- **Azul Fundo** (`#2F5D74`) e **Marinho** (`#17323F`): estados selecionados, contador da sacola, aviso do topo, rodapé e texto sobre o Azul Solara.

### Tertiary
- **Ouro** (`#A57D2C`, degradê de `#C9A132` a `#7A4E1C`): moldura da vitrine, trilho das araras, ganchos e marcadores. Só em linhas e filetes, nunca em blocos de texto.

### Neutral
- **Creme** (`#FCFDF5`): fundo das páginas. **Parede** (`#F7F3E8`): o reboco da fachada, um tom mais quente atrás do letreiro e da vitrine.
- **Marrom** (`#5E3416`): todo o texto e o botão principal. **Marrom suave** (`#7A5A44`): texto secundário.

### Named Rules
- **Regra do texto sobre azul:** texto sobre Azul Solara ou Azul Logo é Marinho; texto claro só sobre Azul Fundo ou Marinho.
- **Ouro é filete:** o dourado desenha bordas, trilhos e pontos; não preenche botões nem fundos.

## Typography

Italiana nos títulos e nos nomes das peças, pela afinidade com as capitulares finas e de alto contraste do logo. Work Sans no texto, nos preços e nos rótulos. As duas são servidas pelos arquivos da própria loja (`site/fonts/`).

### Hierarchy
- Título de página: Italiana, `clamp(2.6rem, 6vw, 4.6rem)`.
- Título de seção (nome da arara): Italiana, `clamp(2rem, 4.4vw, 3.4rem)`.
- Nome da peça: Italiana, 1.35rem nos cartões, maior na vitrine.
- Rótulos, navegação e botões: Work Sans em caixa alta, 0.8rem, espaçamento 0.12em a 0.16em.
- Preço: Work Sans com algarismos tabulares.

## Layout

Largura útil `min(1240px, 100% - 2 × clamp(16px, 4vw, 48px))`. A home segue a ordem física da loja: letreiro, placa com o logo, toldo, vitrine (três expositores em colunas iguais), calçada com duas notas, araras por categoria (lista horizontal com rolagem e encaixe), bloco "Visite a loja" dividido entre texto e foto da fachada, rodapé. Abaixo de 860px a vitrine vira um carrossel com encaixe no centro, as araras mostram dois terços de cartão para indicar rolagem e o menu vai para o botão de três linhas.

## Elevation & Depth

Profundidade só em dois lugares: a sombra projetada sob as peças na vitrine (`drop-shadow` marrom suave) e a sombra azulada do cartão ao passar o mouse (`0 18px 40px -22px rgba(47,93,116,.45)`). A sacola abre por cima com um véu azul translúcido.

## Shapes

Cantos de 4px em botões e campos, 6px em blocos grandes. O toldo tem a borda inferior recortada em meias-luas. Tamanhos P, M e G são círculos de 40px. Filtros de categoria são pílulas.

## Components

### Buttons
Principal marrom com texto creme em caixa alta; ao passar o mouse vira o dourado escuro. Variante clara com contorno marrom. Nunca quebram linha.

### Chips
Tamanho: círculo com letra em Italiana, contorno Azul Logo; selecionado preenche em Azul Fundo. Filtro: pílula com contorno; ativo preenche em Azul Fundo.

### Cards / Containers
Cartão de peça: campo de cor clara na proporção 4:5 com o croqui ao centro, nome em Italiana e preço na mesma linha, bolinhas das cores abaixo. Na home cada cartão pende de um gancho dourado sobre o trilho da arara e balança de leve ao passar o mouse.

### Inputs / Fields
Campos brancos com borda dourada translúcida, 46px de altura, foco com contorno Azul Logo.

### Navigation
Letreiro fixo no topo, translúcido sobre o creme: categorias à esquerda, logo horizontal ao centro, "A loja" e a sacola à direita. Na home o logo do letreiro só aparece depois que a placa da fachada sai da tela.

### Vitrine
Janela com moldura dourada de 2px e filete interno, vidro em degradê claro, o sol do logo nascendo atrás das peças e um reflexo de luz que atravessa o vidro uma única vez ao abrir a página.

## Do's and Don'ts

### Do:
- Usar o logo, o monograma e o sol a partir dos SVGs extraídos do manual.
- Manter o campo de cor clara atrás de cada peça quando as fotos chegarem.
- Exigir a escolha do tamanho antes de adicionar, com o aviso ao lado do botão.

### Don't:
- Colocar texto branco sobre o Azul Solara.
- Inventar preços, parcelamento, prazos ou avaliações: até existirem dados reais, ficam marcados como exemplo ou "a preencher".
- Usar rótulo pequeno acima dos títulos.
