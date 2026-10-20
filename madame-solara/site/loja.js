/* Comportamento compartilhado da loja: letreiro, rodapé, sacola e páginas. */

const ICONES = {
  sacola: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 8h14l-1 12H6L5 8Z"/><path d="M9 8V6a3 3 0 0 1 6 0v2"/></svg>',
  fechar: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>',
  menu: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" aria-hidden="true"><path d="M4 8h16M4 16h16"/></svg>',
  gancho: '<svg class="cabide__gancho" viewBox="0 0 64 44" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M32 22 V16 C32 11 38 10 38 5 C38 1 33 -1 29 2"/><path d="M32 22 L6 40 Q4 42 7 42 H57 Q60 42 58 40 Z"/></svg>',
};

let PAGINA = document.body.dataset.pagina;

/* Na versão de arquivo único (link do Claude) as telas trocam sem recarregar a página. */
const SPA = window.MS_SPA || null;
function parametros() { return SPA ? SPA.params : new URLSearchParams(location.search); }

/* ---------- sacola (guardada no navegador; na Nuvemshop o carrinho é da plataforma) ---------- */
const CHAVE = "madame-solara-sacola";
let sacola = [];
try { sacola = JSON.parse(localStorage.getItem(CHAVE)) || []; } catch (e) { sacola = []; }

function salvar() {
  try { localStorage.setItem(CHAVE, JSON.stringify(sacola)); } catch (e) { /* navegação privada: segue só nesta página */ }
  atualizarContador();
  desenharSacola();
}

function adicionar(id, tamanho, cor) {
  const existente = sacola.find((i) => i.id === id && i.tamanho === tamanho && i.cor === cor);
  if (existente) existente.qtd += 1;
  else sacola.push({ id, tamanho, cor, qtd: 1 });
  salvar();
  const contador = document.querySelector(".contador");
  contador.classList.add("pulsa");
  setTimeout(() => contador.classList.remove("pulsa"), 400);
  abrirSacola();
}

function totalItens() { return sacola.reduce((s, i) => s + i.qtd, 0); }
function subtotal() { return sacola.reduce((s, i) => s + produtoPorId(i.id).preco * i.qtd, 0); }

function atualizarContador() {
  const c = document.querySelector(".contador");
  if (c) c.textContent = totalItens();
}

function abrirSacola() {
  document.body.classList.add("sacola-aberta");
  document.querySelector(".sacola").setAttribute("aria-hidden", "false");
  document.querySelector(".sacola .fechar").focus();
}
function fecharSacola() {
  document.body.classList.remove("sacola-aberta");
  document.querySelector(".sacola").setAttribute("aria-hidden", "true");
  document.querySelector(".botao-sacola").focus();
}

function desenharSacola() {
  const lista = document.querySelector(".sacola__itens");
  const rodape = document.querySelector(".sacola__rodape");
  if (!lista) return;
  if (!sacola.length) {
    lista.innerHTML = `<li class="sacola__vazia">
        <img src="assets/sol.svg" alt="">
        <p>Sua sacola está vazia.</p>
        <a class="botao botao--claro" href="colecao.html">Ver a coleção</a>
      </li>`;
    rodape.hidden = true;
    return;
  }
  rodape.hidden = false;
  lista.innerHTML = sacola.map((item, n) => {
    const p = produtoPorId(item.id);
    return `<li class="item">
      <a class="item__campo" href="produto.html?id=${p.id}" style="background:${CORES[item.cor].campo}">${croqui(p, item.cor)}</a>
      <div>
        <h3>${p.nome}</h3>
        <p>${CORES[item.cor].nome} · Tamanho ${item.tamanho}</p>
        <div class="qtd" role="group" aria-label="Quantidade de ${p.nome}">
          <button type="button" data-qtd="-1" data-n="${n}" aria-label="Diminuir">–</button>
          <output>${item.qtd}</output>
          <button type="button" data-qtd="1" data-n="${n}" aria-label="Aumentar">+</button>
        </div>
      </div>
      <div style="display:grid; justify-items:end; gap:6px">
        <span class="preco">${formatarPreco(p.preco * item.qtd)}</span>
        <button type="button" class="remover" data-remover="${n}">Remover</button>
      </div>
    </li>`;
  }).join("");
  document.querySelector(".sacola .subtotal").textContent = formatarPreco(subtotal());
}

/* ---------- letreiro, sacola e rodapé ---------- */
function montarMoldura() {
  const atual = (nome) => (PAGINA === nome ? ' aria-current="page"' : "");
  document.body.insertAdjacentHTML("afterbegin", `
    <a class="oculto" href="#conteudo">Pular para o conteúdo</a>
    <p class="aviso">Protótipo · peças e preços de exemplo</p>
    <header class="letreiro">
      <div class="letreiro__faixa">
        <button class="menu-celular" type="button" aria-label="Abrir menu" aria-expanded="false">${ICONES.menu}</button>
        <nav aria-label="Principal">
          <a href="colecao.html"${atual("colecao")}>Coleção</a>
          <a href="colecao.html?c=biquinis">Biquínis</a>
          <a href="colecao.html?c=maios">Maiôs</a>
          <a href="colecao.html?c=resort">Resort</a>
        </nav>
        <a class="letreiro__logo" href="index.html" aria-label="Madame Solara, página inicial">
          <img src="assets/logo-horizontal-colorido.svg" alt="Madame Solara">
        </a>
        <div class="letreiro__acoes">
          <a class="so-desktop" href="index.html#visite">A loja</a>
          <button class="botao-sacola" type="button" aria-haspopup="dialog">
            ${ICONES.sacola}<span class="rotulo">Sacola</span><span class="contador" aria-label="itens na sacola">0</span>
          </button>
        </div>
      </div>
    </header>`);

  document.body.insertAdjacentHTML("beforeend", `
    <footer class="rodape">
      <div class="rodape__miolo">
        <div class="rodape__marca">
          <img src="assets/monograma-branco.svg" alt="">
          <p>Você é o seu padrão!</p>
        </div>
        <div><h3>Comprar</h3><ul>
          <li><a href="colecao.html?c=biquinis">Biquínis</a></li>
          <li><a href="colecao.html?c=maios">Maiôs</a></li>
          <li><a href="colecao.html?c=resort">Resort</a></li></ul></div>
        <div><h3>Atendimento</h3><ul>
          <li><a href="#">Trocas e devoluções</a></li>
          <li><a href="#">Pagamentos</a></li>
          <li><a href="#">Envios</a></li>
          <li><a href="#">Cuidados com a peça</a></li></ul></div>
        <div><h3>Siga</h3><ul>
          <li><a href="#">Instagram</a></li>
          <li><a href="#">WhatsApp</a></li>
          <li><a href="index.html#visite">Loja física</a></li></ul></div>
      </div>
      <p class="rodape__fim">Madame Solara · Moda praia &amp; resort</p>
    </footer>
    <div class="sacola-fundo"></div>
    <aside class="sacola" role="dialog" aria-modal="true" aria-label="Sacola" aria-hidden="true">
      <div class="sacola__topo"><h2>Sacola</h2><button class="fechar" type="button" aria-label="Fechar sacola">${ICONES.fechar}</button></div>
      <ul class="sacola__itens"></ul>
      <div class="sacola__rodape">
        <div class="linha-total"><span>Subtotal</span><strong class="subtotal">R$ 0,00</strong></div>
        <small>Frete e prazo calculados no fechamento do pedido.</small>
        <a class="botao" href="checkout.html">Finalizar compra</a>
      </div>
    </aside>`);

  document.querySelector(".botao-sacola").addEventListener("click", abrirSacola);
  document.querySelector(".sacola .fechar").addEventListener("click", fecharSacola);
  document.querySelector(".sacola-fundo").addEventListener("click", fecharSacola);
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && document.body.classList.contains("sacola-aberta")) fecharSacola();
  });
  document.querySelector(".sacola__itens").addEventListener("click", (e) => {
    const b = e.target.closest("button");
    if (!b) return;
    if (b.dataset.remover !== undefined) sacola.splice(+b.dataset.remover, 1);
    if (b.dataset.qtd) {
      const item = sacola[+b.dataset.n];
      item.qtd += +b.dataset.qtd;
      if (item.qtd < 1) sacola.splice(+b.dataset.n, 1);
    }
    salvar();
  });
  const menu = document.querySelector(".menu-celular");
  menu.addEventListener("click", () => {
    const aberto = document.querySelector(".letreiro").classList.toggle("menu-aberto");
    menu.setAttribute("aria-expanded", aberto);
    menu.setAttribute("aria-label", aberto ? "Fechar menu" : "Abrir menu");
  });
  atualizarContador();
  desenharSacola();
}

/* ---------- peças ---------- */
function seletorTamanho(id) {
  return `<fieldset class="tamanhos">
    <legend>Tamanho</legend>
    ${TAMANHOS.map((t) => `<label><input type="radio" name="tam-${id}" value="${t}"><span>${t}</span></label>`).join("")}
  </fieldset>`;
}

/* Botão que exige tamanho antes de adicionar; o aviso aparece ao lado, sem janela. */
function ligarCompra(raiz, id, corAtual) {
  raiz.querySelector("[data-comprar]").addEventListener("click", () => {
    const marcado = raiz.querySelector(`input[name="tam-${id}"]:checked`);
    const aviso = raiz.querySelector(".aviso-campo");
    if (!marcado) { aviso.textContent = "Escolha um tamanho."; raiz.querySelector(`input[name="tam-${id}"]`).focus(); return; }
    aviso.textContent = "";
    adicionar(id, marcado.value, corAtual());
  });
}

function amostra(c) {
  return CORES[c].estampa
    ? `radial-gradient(circle, #FCFDF5 1.4px, transparent 1.8px) 0 0 / 7px 7px, ${CORES[c].fundo}`
    : CORES[c].fundo;
}

function cartao(p) {
  return `<li class="cabide">
    ${PAGINA === "inicio" ? ICONES.gancho : ""}
    <a class="cartao" href="produto.html?id=${p.id}">
      <div class="cartao__campo" style="background:${CORES[p.cores[0]].campo}">${croqui(p)}</div>
      <div class="cartao__info"><h3>${p.nome}</h3><span class="preco">${formatarPreco(p.preco)}</span></div>
      <div class="cartao__cores" aria-label="Cores disponíveis">${p.cores.map((c) => `<i style="background:${amostra(c)}" title="${CORES[c].nome}"></i>`).join("")}</div>
    </a>
  </li>`;
}

function paginaInicio() {
  // o logo do letreiro só aparece depois que a placa da fachada sai da tela
  const placa = document.querySelector(".fachada__placa");
  if ("IntersectionObserver" in window) {
    new IntersectionObserver(([e]) => document.body.classList.toggle("no-topo", e.isIntersecting)).observe(placa);
  }
  const pecas = document.querySelector(".vitrine__pecas");
  pecas.innerHTML = NA_VITRINE.map((id) => {
    const p = produtoPorId(id);
    return `<article class="expositor" data-id="${p.id}">
      <a class="expositor__peca" href="produto.html?id=${p.id}">${croqui(p)}<span class="expositor__base"></span></a>
      <h3>${p.nome}</h3>
      <span class="preco">${formatarPreco(p.preco)}</span>
      ${seletorTamanho(p.id)}
      <button class="botao" type="button" data-comprar>Adicionar à sacola</button>
      <p class="aviso-campo" role="status"></p>
    </article>`;
  }).join("");
  pecas.querySelectorAll(".expositor").forEach((el) => {
    const p = produtoPorId(el.dataset.id);
    ligarCompra(el, p.id, () => p.cores[0]);
  });
  document.querySelectorAll("[data-arara]").forEach((lista) => {
    lista.innerHTML = PRODUTOS.filter((p) => p.categoria === lista.dataset.arara).map(cartao).join("");
  });
}

function paginaColecao() {
  let filtro = parametros().get("c") || "todos";
  const grade = document.querySelector(".grade");
  const titulo = document.querySelector(".pagina__titulo h1");
  const botoes = document.querySelectorAll(".filtros button");
  function desenhar() {
    const lista = filtro === "todos" ? PRODUTOS : PRODUTOS.filter((p) => p.categoria === filtro);
    grade.innerHTML = lista.map(cartao).join("");
    titulo.textContent = filtro === "todos" ? "Coleção" : CATEGORIAS[filtro];
    botoes.forEach((b) => b.setAttribute("aria-pressed", b.dataset.filtro === filtro));
    document.title = `${titulo.textContent} · Madame Solara`;
  }
  botoes.forEach((b) => b.addEventListener("click", () => {
    filtro = b.dataset.filtro;
    if (!SPA) history.replaceState(null, "", filtro === "todos" ? "colecao.html" : `colecao.html?c=${filtro}`);
    desenhar();
  }));
  desenhar();
}

function paginaProduto() {
  const p = produtoPorId(parametros().get("id")) || PRODUTOS[0];
  let cor = p.cores[0];
  document.title = `${p.nome} · Madame Solara`;
  const raiz = document.querySelector(".produto");
  raiz.innerHTML = `
    <div class="produto__campo" style="background:${CORES[cor].campo}">
      ${croqui(p, cor)}<span class="produto__selo">Foto da peça em breve</span>
    </div>
    <div class="produto__info">
      <p class="trilha"><a href="colecao.html">Coleção</a> / <a href="colecao.html?c=${p.categoria}">${CATEGORIAS[p.categoria]}</a></p>
      <h1>${p.nome}</h1>
      <span class="preco">${formatarPreco(p.preco)} <small>preço de exemplo</small></span>
      <p>${p.texto}</p>
      <div class="campo-escolha"><span>Cor: <b class="nome-cor">${CORES[cor].nome}</b></span>
        <div class="cores">${p.cores.map((c) => `<button type="button" data-cor="${c}" aria-label="${CORES[c].nome}" aria-pressed="${c === cor}" style="background:${amostra(c)}"></button>`).join("")}</div>
      </div>
      <div class="campo-escolha"><span>Tamanho</span>${seletorTamanho(p.id)}</div>
      <button class="botao" type="button" data-comprar>Adicionar à sacola</button>
      <p class="aviso-campo" role="status"></p>
      <div>
        <details><summary>Guia de medidas</summary>
          <table><thead><tr><th>Tamanho</th><th>Busto</th><th>Quadril</th></tr></thead>
          <tbody><tr><td>P</td><td>— cm</td><td>— cm</td></tr><tr><td>M</td><td>— cm</td><td>— cm</td></tr><tr><td>G</td><td>— cm</td><td>— cm</td></tr></tbody></table>
          <p>Medidas a preencher pela Madame Solara.</p></details>
        <details><summary>Cuidados</summary>
          <p>Lave à mão com sabão neutro e água fria, antes do primeiro uso. Não torça, seque à sombra e não use prendedor, alvejante, ferro ou máquina. Não deixe de molho nem guarde úmido em saco plástico. Peças neon pedem cuidado redobrado.</p></details>
        <details><summary>Envios e trocas</summary>
          <p>Prazo, frete e política de trocas a definir.</p></details>
      </div>
    </div>`;
  ligarCompra(raiz, p.id, () => cor);
  raiz.querySelectorAll("[data-cor]").forEach((b) => b.addEventListener("click", () => {
    cor = b.dataset.cor;
    raiz.querySelector(".produto__campo").style.background = CORES[cor].campo;
    raiz.querySelector(".produto__campo .croqui").outerHTML = croqui(p, cor);
    raiz.querySelector(".nome-cor").textContent = CORES[cor].nome;
    raiz.querySelectorAll("[data-cor]").forEach((x) => x.setAttribute("aria-pressed", x === b));
  }));
  document.querySelector("[data-arara]").innerHTML =
    PRODUTOS.filter((x) => x.categoria === p.categoria && x.id !== p.id).concat(PRODUTOS.filter((x) => x.categoria !== p.categoria)).slice(0, 4).map(cartao).join("");
}

function paginaCheckout() {
  const resumo = document.querySelector(".resumo__itens");
  const form = document.querySelector(".checkout form");
  if (!sacola.length) {
    document.querySelector(".checkout").innerHTML = `<div class="confirmacao" style="grid-column:1/-1">
      <img src="assets/sol.svg" alt=""><h1>Sua sacola está vazia</h1><a class="botao" href="colecao.html">Ver a coleção</a></div>`;
    return;
  }
  resumo.innerHTML = sacola.map((i) => {
    const p = produtoPorId(i.id);
    return `<div class="linha-total"><span>${i.qtd}× ${p.nome} · ${i.tamanho}</span><span class="preco">${formatarPreco(p.preco * i.qtd)}</span></div>`;
  }).join("");
  document.querySelector(".resumo .subtotal").textContent = formatarPreco(subtotal());
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    if (!form.reportValidity()) return;
    sacola = []; salvar();
    document.querySelector(".checkout").innerHTML = `<div class="confirmacao" style="grid-column:1/-1">
      <img src="assets/monograma-dourado.svg" alt=""><h1>Pedido de demonstração recebido</h1>
      <p>Na loja de verdade, este passo é o checkout da Nuvemshop, com Pix, cartão e cálculo de frete.</p>
      <a class="botao botao--claro" href="index.html">Voltar à vitrine</a></div>`;
    window.scrollTo({ top: 0 });
  });
}

const PAGINAS = { inicio: paginaInicio, colecao: paginaColecao, produto: paginaProduto, checkout: paginaCheckout };

function navegar(href) {
  const [caminho, ancora] = href.split("#");
  const [arquivo, busca] = caminho.split("?");
  const nome = { "index.html": "inicio", "colecao.html": "colecao", "produto.html": "produto", "checkout.html": "checkout" }[arquivo || "index.html"];
  SPA.params = new URLSearchParams(busca || "");
  PAGINA = nome;
  document.body.dataset.pagina = nome;
  document.body.classList.remove("no-topo", "sacola-aberta");
  document.querySelector(".letreiro").classList.remove("menu-aberto");
  const main = document.getElementById("conteudo");
  main.className = SPA.classes[nome];
  main.innerHTML = document.getElementById(`tela-${nome}`).innerHTML;
  document.title = SPA.titulos[nome];
  document.querySelectorAll(".letreiro nav a").forEach((a) => a.toggleAttribute("aria-current", nome === "colecao" && a.getAttribute("href") === "colecao.html"));
  PAGINAS[nome]();
  const alvo = ancora && document.getElementById(ancora);
  if (alvo) alvo.scrollIntoView(); else window.scrollTo({ top: 0 });
}

montarMoldura();
if (SPA) {
  document.addEventListener("click", (e) => {
    const a = e.target.closest("a[href]");
    if (!a) return;
    const href = a.getAttribute("href");
    if (/^(index|colecao|produto|checkout)\.html/.test(href)) { e.preventDefault(); navegar(href); }
    else if (href === "#") e.preventDefault();
  });
  navegar("index.html");
} else {
  PAGINAS[PAGINA]?.();
}
