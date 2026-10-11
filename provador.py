"""Topo da página do studio: o provador de olhar (cílios, sobrancelha e lábios com fotos reais)."""
import json
from urllib.parse import quote

from components import caminhos_imagem, esc, imagem
from data import NEGOCIO, PROVADOR, PROVADOR_MENSAGEM_PADRAO


def link_whatsapp(numero_e164, texto):
    return f"https://wa.me/{numero_e164.lstrip('+')}?text={quote(texto)}"


def _chaves_de_foto(opcao):
    """Nomes de foto da opção, do mais específico (arquivo provador-*) ao compartilhado."""
    return [c for c in (opcao.get("foto"), opcao.get("foto_padrao")) if c]


def _foto_escolhida(opcao, fotos):
    return next((c for c in _chaves_de_foto(opcao) if c in fotos), None)


def opcoes_visiveis(grupo, fotos):
    return [o for o in grupo["opcoes"] if not (o.get("exige_foto") and _foto_escolhida(o, fotos) is None)]


def _foto(nome, fotos):
    if not nome or nome not in fotos:
        return None
    info = fotos[nome]
    src, srcset, _ = caminhos_imagem(nome, info)
    return {"nome": nome, "src": src, "srcset": srcset,
            "mini": f"/img/{nome}-{info['larguras'][0]}.webp",
            "w": info["w"], "h": info["h"]}


def dados_provador(fotos, numero_e164):
    grupos = []
    for grupo in PROVADOR:
        visiveis = opcoes_visiveis(grupo, fotos)
        if not visiveis:
            raise SystemExit(f"provador: o grupo '{grupo['grupo']}' ficou sem nenhuma opção visível")
        opcoes = [{"id": o["id"], "rotulo": o["rotulo"], "mensagem": o["mensagem"], "alt": o["alt"],
                   "foto": _foto(_foto_escolhida(o, fotos), fotos)}
                  for o in visiveis]
        inicial = grupo["inicial"] if any(o["id"] == grupo["inicial"] for o in opcoes) else opcoes[0]["id"]
        grupos.append({"grupo": grupo["grupo"], "rotulo": grupo["rotulo"],
                       "inicial": inicial, "opcoes": opcoes})
    return {"whatsapp": numero_e164.lstrip("+"), "grupos": grupos}


def _inicial(grupo):
    for o in grupo["opcoes"]:
        if o["id"] == grupo["inicial"]:
            return o
    raise SystemExit(f"provador: a opção inicial '{grupo['inicial']}' do grupo '{grupo['grupo']}' não está visível")


def _grupo_html(grupo):
    botoes = "".join(
        f'<button type="button" class="provador-opcao" data-grupo="{esc(grupo["grupo"])}" '
        f'data-opcao="{esc(o["id"])}" aria-pressed="{"true" if o["id"] == grupo["inicial"] else "false"}">'
        f'{esc(o["rotulo"])}</button>'
        for o in grupo["opcoes"])
    return (f'<div class="provador-grupo" role="group" aria-label="{esc(grupo["rotulo"])}">'
            f'<p class="provador-rotulo">{esc(grupo["rotulo"])}</p>'
            f'<div class="provador-opcoes">{botoes}</div></div>')


def _miniaturas_html(escolhidas):
    itens = "".join(
        f'<img src="{esc(o["foto"]["mini"])}" alt="" width="44" height="44" loading="lazy" decoding="async">'
        for o in escolhidas if o["foto"])
    return f'<div class="provador-miniaturas" data-provador-miniaturas>{itens}</div>'


def render_provador(fotos, numero_e164, agenda_url):
    n = NEGOCIO
    dados = dados_provador(fotos, numero_e164)
    escolhidas = [_inicial(g) for g in dados["grupos"]]
    resumo = " · ".join(o["rotulo"] for o in escolhidas)
    principal = escolhidas[0]
    foto_html = ""
    if principal["foto"]:
        nome = principal["foto"]["nome"]
        foto_html = imagem(nome, fotos[nome], principal["alt"], sizes="(min-width: 720px) 45vw, 100vw",
                           carregar="eager", prioridade=True, extra="data-provador-foto")
    classe_foto = "provador-foto" if foto_html else "provador-foto sem-foto"
    grupos = "".join(_grupo_html(g) for g in dados["grupos"])
    json_txt = json.dumps(dados, ensure_ascii=False).replace("</", "<\\/")
    zap = link_whatsapp(numero_e164, PROVADOR_MENSAGEM_PADRAO)
    return f'''<section id="inicio" class="provador">
  <div class="provador-texto">
    <img class="hero-logo" src="/static/logo-lockup.png" alt="{esc(n['nome'])} Studio e Academy" width="398" height="178">
    <p class="eyebrow">Studio de cílios e sobrancelhas no {esc(n['bairro'])}</p>
    <h1>Um olhar pra cada mulher. <em>Escolha o seu.</em></h1>
  </div>
  <figure class="{classe_foto}">{foto_html}
    <figcaption class="provador-selo"><small>O seu olhar</small><b data-provador-resumo aria-live="polite">{esc(resumo)}</b></figcaption>
  </figure>
  <div class="provador-controles">
    {grupos}
    <div class="provador-escolhas">{_miniaturas_html(escolhidas)}<p>A Laryssa confirma o combo certo no WhatsApp</p></div>
    <a class="btn btn-whatsapp" href="{esc(zap)}" target="_blank" rel="noopener" data-cta="provador-whatsapp" data-provador-whatsapp>Quero esse olhar · WhatsApp</a>
    <p class="provador-agenda"><a href="{esc(agenda_url)}" target="_blank" rel="noopener" data-cta="provador-agenda">Prefiro escolher o horário na agenda</a></p>
    <p class="selo">{esc(n['nota_google'])} no Google · {n['avaliacoes_google']} avaliações</p>
  </div>
  <script type="application/json" id="provador-dados">{json_txt}</script>
</section>'''
