/* Provador de olhar: troca a foto, o resumo, as miniaturas e a mensagem do WhatsApp a cada escolha. */
(function () {
  "use strict";

  function montarMensagem(escolhas) {
    var partes = escolhas.map(function (o) { return o.mensagem; }).filter(Boolean);
    return "Oi, Laryssa! Montei meu olhar no site: " + partes.join(", ") + ". Quero agendar!";
  }

  function linkWhatsapp(numero, texto) {
    return "https://wa.me/" + numero + "?text=" + encodeURIComponent(texto);
  }

  if (typeof module !== "undefined" && module.exports) {
    module.exports = { montarMensagem: montarMensagem, linkWhatsapp: linkWhatsapp };
    return;
  }

  var secao = document.getElementById("inicio");
  var fonte = document.getElementById("provador-dados");
  if (!secao || !fonte) { return; }

  var dados = JSON.parse(fonte.textContent);
  var escolha = {};
  dados.grupos.forEach(function (g) { escolha[g.grupo] = g.inicial; });

  var figura = secao.querySelector(".provador-foto");
  var foto = secao.querySelector("[data-provador-foto]");
  var resumo = secao.querySelector("[data-provador-resumo]");
  var miniaturas = secao.querySelector("[data-provador-miniaturas]");
  var zap = secao.querySelector("[data-provador-whatsapp]");
  var fotosCarregadas = false;

  function opcao(grupo, id) {
    var g = dados.grupos.filter(function (x) { return x.grupo === grupo; })[0];
    return g.opcoes.filter(function (o) { return o.id === id; })[0];
  }

  function escolhidas() {
    return dados.grupos.map(function (g) { return opcao(g.grupo, escolha[g.grupo]); });
  }

  function preCarregar() {
    if (fotosCarregadas) { return; }
    fotosCarregadas = true;
    dados.grupos.forEach(function (g) {
      g.opcoes.forEach(function (o) {
        if (o.foto) {
          var img = new Image();
          img.srcset = o.foto.srcset;
          img.sizes = "(min-width: 720px) 45vw, 100vw";
          img.src = o.foto.src;
        }
      });
    });
  }

  function trocarFoto(o) {
    if (!o.foto) { return; }
    if (!foto) {
      foto = document.createElement("img");
      foto.setAttribute("data-provador-foto", "");
      foto.decoding = "async";
      foto.sizes = "(min-width: 720px) 45vw, 100vw";
      figura.insertBefore(foto, figura.firstChild);
      figura.classList.remove("sem-foto");
    }
    foto.classList.add("trocando");
    window.setTimeout(function () {
      foto.srcset = o.foto.srcset;
      foto.src = o.foto.src;
      foto.width = o.foto.w;
      foto.height = o.foto.h;
      foto.alt = o.alt;
      foto.classList.remove("trocando");
    }, 150);
  }

  function atualizar() {
    var lista = escolhidas();
    resumo.textContent = lista.map(function (o) { return o.rotulo; }).join(" · ");
    zap.href = linkWhatsapp(dados.whatsapp, montarMensagem(lista));
    miniaturas.innerHTML = "";
    lista.forEach(function (o) {
      if (!o.foto) { return; }
      var mini = document.createElement("img");
      mini.src = o.foto.mini;
      mini.alt = "";
      mini.width = 44;
      mini.height = 44;
      miniaturas.appendChild(mini);
    });
  }

  secao.addEventListener("click", function (evento) {
    var botao = evento.target.closest(".provador-opcao");
    if (!botao) { return; }
    preCarregar();
    var grupo = botao.getAttribute("data-grupo");
    if (escolha[grupo] === botao.getAttribute("data-opcao")) { return; }
    escolha[grupo] = botao.getAttribute("data-opcao");
    secao.querySelectorAll('.provador-opcao[data-grupo="' + grupo + '"]').forEach(function (b) {
      b.setAttribute("aria-pressed", b === botao ? "true" : "false");
    });
    trocarFoto(opcao(grupo, escolha[grupo]));
    atualizar();
  });

  if ("IntersectionObserver" in window) {
    new IntersectionObserver(function (entradas) {
      document.body.classList.toggle("provador-visivel", entradas[0].isIntersecting);
    }, { threshold: 0 }).observe(secao);
  }
})();
