/* Catálogo de exemplo da Madame Solara.
   Nomes, preços e descrições são provisórios: substituir pelos dados reais ao cadastrar na Nuvemshop. */

const CORES = {
  azul:  { nome: "Azul Solara", fundo: "#64A6C9", traco: "#2F5D74", campo: "#E3EEF3" },
  areia: { nome: "Areia",       fundo: "#E6D6B8", traco: "#7A5A34", campo: "#F4EEE2" },
  terra: { nome: "Terra",       fundo: "#9C6440", traco: "#4E2C14", campo: "#EFE3D8" },
  sol:   { nome: "Estampa Sóis", fundo: "#64A6C9", traco: "#2F5D74", campo: "#E3EEF3", estampa: true },
  creme: { nome: "Off Solara",  fundo: "#FBF7EC", traco: "#7A5A34", campo: "#EEF3F1" },
};

const CATEGORIAS = {
  biquinis: "Biquínis",
  maios: "Maiôs",
  resort: "Resort",
};

const PRODUTOS = [
  { id: "aurora",     nome: "Biquíni Aurora",      categoria: "biquinis", forma: "cortininha", cores: ["azul", "areia"], preco: 219,
    texto: "Cortininha de amarração com bojo removível. Calcinha de lateral ajustável." },
  { id: "mare",       nome: "Biquíni Maré",        categoria: "biquinis", forma: "faixa",      cores: ["sol", "azul"],   preco: 229,
    texto: "Top faixa com nó central e alça removível. Calcinha de cós médio." },
  { id: "duna",       nome: "Biquíni Duna",        categoria: "biquinis", forma: "cortininha", cores: ["terra", "areia"], preco: 219,
    texto: "Cortininha de amarração em tecido de toque acetinado." },
  { id: "solara",     nome: "Maiô Solara",         categoria: "maios",    forma: "maio",       cores: ["terra", "azul"], preco: 289,
    texto: "Maiô de decote arredondado e costas baixas, com forro duplo." },
  { id: "brisa",      nome: "Maiô Brisa",          categoria: "maios",    forma: "maio",       cores: ["azul", "creme"], preco: 289,
    texto: "Maiô de alças finas reguláveis e cava alta." },
  { id: "horizonte",  nome: "Kaftan Horizonte",    categoria: "resort",   forma: "kaftan",     cores: ["areia", "creme"], preco: 349,
    texto: "Saída longa de mangas amplas, para usar aberta ou com faixa na cintura." },
  { id: "entardecer", nome: "Vestido Entardecer",  categoria: "resort",   forma: "vestido",    cores: ["terra", "azul"], preco: 389,
    texto: "Vestido midi de alças, com fenda lateral e caimento fluido." },
  { id: "concha",     nome: "Saída Concha",        categoria: "resort",   forma: "kaftan",     cores: ["sol", "areia"],  preco: 329,
    texto: "Saída curta em estampa exclusiva de sóis." },
];

const NA_VITRINE = ["aurora", "solara", "horizonte"];
const TAMANHOS = ["P", "M", "G"];

function formatarPreco(valor) {
  return valor.toLocaleString("pt-BR", { style: "currency", currency: "BRL" });
}

function produtoPorId(id) {
  return PRODUTOS.find((p) => p.id === id);
}

/* Croquis técnicos (desenho plano de moda) que ficam no lugar das fotos até elas existirem. */
const FORMAS = {
  cortininha: `
    <path d="M70 52 C66 70 58 86 50 100 C64 108 84 106 96 96 C88 80 80 66 70 52 Z"/>
    <path d="M130 52 C134 70 142 86 150 100 C136 108 116 106 104 96 C112 80 120 66 130 52 Z"/>
    <path class="fio" d="M70 52 C74 40 80 32 88 24 M130 52 C126 40 120 32 112 24 M50 100 C40 101 30 99 20 95 M150 100 C160 101 170 99 180 95"/>
    <path class="fio" d="M96 96 Q100 99 104 96"/>
    <path d="M56 150 Q100 162 144 150 L140 160 Q120 192 104 204 Q100 207 96 204 Q80 192 60 160 Z"/>
    <path class="fio" d="M56 150 C48 148 40 152 36 160 M144 150 C152 148 160 152 164 160"/>`,
  faixa: `
    <path d="M44 66 Q100 54 156 66 L154 98 Q100 110 46 98 Z"/>
    <path class="fio" d="M92 62 Q100 82 108 62 M94 104 Q100 84 106 104"/>
    <path d="M52 146 Q100 156 148 146 L150 168 Q132 192 106 202 Q100 204 94 202 Q68 192 50 168 Z"/>
    <path class="fio" d="M54 158 Q100 168 146 158"/>`,
  maio: `
    <path d="M72 20 L78 20 C80 52 90 66 100 66 C110 66 120 52 122 20 L128 20
             C134 52 142 70 140 96 C138 120 128 134 130 158 C132 176 146 196 152 210
             Q126 204 108 222 Q100 228 92 222 Q74 204 48 210
             C54 196 68 176 70 158 C72 134 62 120 60 96 C58 70 66 52 72 20 Z"/>
    <path class="fio" d="M74 120 Q100 128 126 120"/>`,
  kaftan: `
    <path d="M84 20 Q100 36 116 20 L140 26 L196 96 L176 116 L148 86 L156 226 L44 226 L52 86 L24 116 L4 96 L60 26 Z"/>
    <path class="fio" d="M84 20 Q100 52 116 20 M100 44 V226 M56 120 Q100 130 144 120"/>`,
  vestido: `
    <path d="M78 18 L82 18 L86 54 Q100 64 114 54 L118 18 L122 18 L128 60 Q140 90 136 112
             L160 226 L40 226 L64 112 Q60 90 72 60 Z"/>
    <path class="fio" d="M66 108 Q100 118 134 108 M130 150 L138 226"/>`,
};

function croqui(produto, corChave) {
  const cor = CORES[corChave || produto.cores[0]];
  const uid = `${produto.id}-${corChave || produto.cores[0]}`;
  const preench = cor.estampa ? `url(#estampa-${uid})` : cor.fundo;
  const estampa = cor.estampa
    ? `<pattern id="estampa-${uid}" width="22" height="16" patternUnits="userSpaceOnUse">
         <rect width="22" height="16" fill="${cor.fundo}"/>
         <path d="M5 11 A6 6 0 0 1 17 11" fill="none" stroke="#FCFDF5" stroke-width="1.2"/>
         <path d="M11 3 V1.5 M5.5 5.5 L4.4 4.4 M16.5 5.5 L17.6 4.4" stroke="#FCFDF5" stroke-width="1" stroke-linecap="round"/>
       </pattern>`
    : "";
  return `<svg class="croqui" viewBox="0 0 200 240" role="img" aria-label="Desenho da peça ${produto.nome} na cor ${cor.nome}">
    <defs>${estampa}</defs>
    <g fill="${preench}" stroke="${cor.traco}" stroke-width="1.6" stroke-linejoin="round" stroke-linecap="round">
      ${FORMAS[produto.forma].replaceAll('class="fio"', 'class="fio" fill="none"')}
    </g>
  </svg>`;
}
