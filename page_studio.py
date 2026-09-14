"""Página principal: o studio. Nove seções, na ordem revisada em 14/09/2026."""
from components import esc, cta, imagem, ornamento
from data import (NEGOCIO, HORARIO, HORARIO_FECHADO, SERVICOS, FOTO_SERVICO, PRIMEIRO_OLHAR, COMBOS, PACOTES,
                  AVALIACOES_STUDIO, FAQ, ALT_FOTOS)
from head import render_head
from schema import beauty_salon, jsonld_script

TITULO = "Extensão de cílios e sobrancelhas no Rio Comprido | Rainha do Olhar"
DESCRICAO = (f"Studio de cílios, sobrancelhas e lábios no Rio Comprido. Nota {NEGOCIO['nota_google']} no Google "
             f"com {NEGOCIO['avaliacoes_google']} avaliações. Agende pelo Maapp.")
MAAPP = NEGOCIO["maapp_url"]


def _inicio(fotos):
    n = NEGOCIO
    tem_foto = bool(fotos and fotos.get("hero"))
    foto_html = ""
    if tem_foto:
        img = imagem("hero", fotos["hero"], ALT_FOTOS["hero"], sizes="(min-width: 720px) 45vw, 100vw",
                     carregar="eager", prioridade=True)
        foto_html = f'<figure class="hero-foto">{img}</figure>'
    classe = "hero tem-foto" if tem_foto else "hero"
    return f'''<section id="inicio" class="{classe}">
  <div class="hero-conteudo">
    <img class="hero-logo" src="/static/logo-lockup.png" alt="{esc(n['nome'])} Studio e Academy" width="398" height="178">
    <p class="eyebrow">Studio de cílios e sobrancelhas no {esc(n['bairro'])}</p>
    <h1>Um olhar pra cada mulher. <em>Escolha o seu.</em></h1>
    <p class="lead">Extensão de cílios, design de sobrancelhas e lábios, com quem também forma profissionais.</p>
    {cta(MAAPP, "Agendar horário", "hero")}
    <p class="selo">{esc(n['nota_google'])} no Google · {n['avaliacoes_google']} avaliações</p>
  </div>
  {foto_html}
</section>'''


def _antes_depois_micropigmentacao(fotos):
    if not fotos or "micropigmentacao-antes" not in fotos or "micropigmentacao-depois" not in fotos:
        return ""
    antes = imagem("micropigmentacao-antes", fotos["micropigmentacao-antes"],
                   ALT_FOTOS["micropigmentacao-antes"], sizes="(min-width: 720px) 40vw, 50vw")
    depois = imagem("micropigmentacao-depois", fotos["micropigmentacao-depois"],
                    ALT_FOTOS["micropigmentacao-depois"], sizes="(min-width: 720px) 40vw, 50vw")
    return f'''<div class="bloco-antes-depois">
  <h3 class="subtitulo">Antes e depois da micropigmentação</h3>
  <div class="antes-depois">
    <figure>{antes}<figcaption>Antes</figcaption></figure>
    <figure>{depois}<figcaption>Depois</figcaption></figure>
  </div>
</div>'''


def _cartao_servico(item, foto_nome, foto_info):
    img = imagem(foto_nome, foto_info, ALT_FOTOS[foto_nome], sizes="(min-width: 720px) 25vw, 50vw")
    return (f'<article class="cartao-servico"><div class="foto-servico">{img}</div>'
            f'<div class="corpo-cartao"><h4>{esc(item["nome"])}</h4>'
            f'<p class="detalhe">{esc(item["duracao"])} · {esc(item["texto"])}</p>'
            f'{cta(MAAPP, "Agendar", f"servico-{foto_nome}", "secundario")}</div></article>')


def _categoria_servicos(cat, fotos):
    cartoes, lista = [], []
    for item in cat["itens"]:
        foto_nome = FOTO_SERVICO.get(item["nome"])
        if foto_nome and fotos.get(foto_nome):
            cartoes.append(_cartao_servico(item, foto_nome, fotos[foto_nome]))
        else:
            lista.append(f'<li><div class="servico"><span class="nome">{esc(item["nome"])}</span></div>'
                         f'<p class="detalhe">{esc(item["duracao"])} · {esc(item["texto"])}</p></li>')
    cartoes_html = f'<div class="cartoes-servicos">{"".join(cartoes)}</div>' if cartoes else ""
    lista_html = f'<ul class="lista-servicos">{"".join(lista)}</ul>' if lista else ""
    return f'<div class="categoria"><h3>{esc(cat["categoria"])}</h3>{cartoes_html}{lista_html}</div>'


def _servicos(fotos):
    blocos = []
    for cat in SERVICOS:
        blocos.append(_categoria_servicos(cat, fotos))
        if cat["categoria"] == "Sobrancelhas":
            blocos.append(_antes_depois_micropigmentacao(fotos))
    return f'''<section id="servicos">
  {ornamento()}
  <h2>Serviços</h2>
  <div class="categorias">{"".join(b for b in blocos if b)}</div>
  <div class="centro">
    {cta(MAAPP, "Agendar horário", "servicos")}
    <p class="mais-instagram"><a href="{esc(NEGOCIO['instagram_url'])}" target="_blank" rel="noopener">Ver mais no Instagram @{esc(NEGOCIO['instagram_usuario'])}</a></p>
  </div>
</section>'''


def _primeiro_olhar():
    po = PRIMEIRO_OLHAR
    return f'''<section id="primeiro-olhar" class="destaque">
  <p class="eyebrow">Para quem vem pela primeira vez</p>
  <h2>{esc(po['nome'])}</h2>
  <p>{esc(po['texto'])}</p>
  <p>{esc(po['argumento'])}</p>
  <p class="detalhe">Duração: {esc(po['duracao'])}</p>
  {cta(MAAPP, "Quero o Primeiro Olhar", "primeiro-olhar")}
</section>'''


def _cartao(oferta, rastreio, texto_botao):
    return (f'<article class="cartao"><h3>{esc(oferta["nome"])}</h3><p>{esc(oferta["inclui"])}</p>'
            f'{cta(MAAPP, texto_botao, rastreio, "secundario")}</article>')


def _pacotes_bloco():
    itens = "".join(
        f'<li><span class="nome-pacote">{esc(p["nome"])}</span> · {esc(p["inclui"])} '
        f'{cta(MAAPP, "Agendar", "pacote", "texto")}</li>'
        for p in PACOTES)
    return f'''<div class="bloco-pacotes">
  <p class="secao-intro">Pacotes: você agenda a primeira sessão e fecha o pacote com a Laryssa no dia.</p>
  <ul class="lista-pacotes">{itens}</ul>
</div>'''


def _combos_pacotes():
    combos = "".join(_cartao(c, "combo", "Agendar combo") for c in COMBOS)
    return f'''<section id="combos-pacotes">
  {ornamento()}
  <h2>Combos e pacotes</h2>
  <p class="secao-intro">Leve junto e pague menos do que avulso.</p>
  <h3 class="subtitulo">Combos</h3>
  <div class="cartoes">{combos}</div>
  <h3 class="subtitulo">Pacotes</h3>
  {_pacotes_bloco()}
</section>'''


def _manutencao():
    return f'''<section id="manutencao">
  <h2>Como funciona a manutenção</h2>
  <p>Seu cílio natural troca sozinho, e o fio aplicado vai junto. Por isso a manutenção faz parte da rotina, e não é sinal de que caiu antes da hora.</p>
  <ul class="regua">
    <li><strong>Até 21 dias</strong><span>é manutenção.</span></li>
    <li><strong>Depois de 21 dias</strong><span>o cílio natural já renovou quase todo, e o certo é uma aplicação nova.</span></li>
  </ul>
  <p class="dica">Dica: marque a próxima manutenção na saída do atendimento. Assim você garante o horário e não perde o prazo.</p>
</section>'''


def _quem_faz(fotos):
    foto = (f'<figure class="retrato">{imagem("laryssa", fotos["laryssa"], ALT_FOTOS["laryssa"], sizes="(min-width: 720px) 320px, 70vw")}</figure>'
            if fotos and fotos.get("laryssa") else "")
    return f'''<section id="quem-faz" class="duas-colunas">
  {foto}
  <div>
    <h2>Quem faz</h2>
    <p>Eu sou a Laryssa. Atendo no studio do {esc(NEGOCIO['bairro'])} e também formo profissionais: já são mais de 100 alunas.</p>
    <p>Cada olhar começa com um mapeamento do seu rosto, porque o desenho que fica bonito em uma pessoa não é o mesmo que fica bonito em outra.</p>
    <p><a href="/academy/">Conhecer a Academy</a></p>
  </div>
</section>'''


def _avaliacoes():
    itens = "".join(
        f'<blockquote class="avaliacao"><p>“{esc(a["texto"])}”</p>'
        f'<footer>{esc(a["nome"])} · avaliação no Google</footer></blockquote>'
        for a in AVALIACOES_STUDIO)
    return f'''<section id="avaliacoes">
  {ornamento()}
  <h2>{esc(NEGOCIO['nota_google'])} no Google, com {NEGOCIO['avaliacoes_google']} avaliações</h2>
  <div class="avaliacoes">{itens}</div>
</section>'''


def _como_chegar():
    n = NEGOCIO
    horarios = "".join(f"<li>{esc(dia)}: {abre} às {fecha}</li>" for dia, abre, fecha, _ in HORARIO)
    return f'''<section id="como-chegar">
  <h2>Como chegar</h2>
  <address>{esc(n['endereco_completo'])}</address>
  <ul class="horario">{horarios}<li>{esc(HORARIO_FECHADO)}</li></ul>
  <p><a href="{esc(n['maps_url'])}" target="_blank" rel="noopener">Abrir no Google Maps</a></p>
  <p>WhatsApp <a href="{esc(n['whatsapp_url'])}" target="_blank" rel="noopener">{esc(n['telefone_exibicao'])}</a></p>
  <iframe class="mapa" title="Mapa do studio Rainha do Olhar" loading="lazy" referrerpolicy="no-referrer-when-downgrade"
    src="https://www.google.com/maps?q=Rainha+do+Olhar,+Rua+Estrela+74,+Rio+Comprido&amp;output=embed"></iframe>
</section>'''


def _perguntas():
    itens = "".join(f"<details><summary>{esc(q)}</summary><p>{esc(r)}</p></details>" for q, r in FAQ)
    return f'''<section id="perguntas">
  <h2>Perguntas frequentes</h2>
  <div class="faq">{itens}</div>
</section>'''


def _rodape():
    n = NEGOCIO
    return f'''<footer class="rodape">
  <img src="/static/logo-monograma.png" alt="" width="46" height="50">
  <p>{esc(n['nome'])} · {esc(n['assinatura'])}</p>
  <p><a href="{esc(n['instagram_url'])}" target="_blank" rel="noopener">@{esc(n['instagram_usuario'])}</a> · <a href="/academy/">Academy</a></p>
</footer>
<div class="barra-agendar">{cta(MAAPP, "Agendar horário", "barra-fixa")}</div>'''


def render_studio(fotos, css_versao, gtm_id=None):
    head = render_head(TITULO, DESCRICAO, "/", [jsonld_script(beauty_salon())], css_versao, gtm_id)
    secoes = [_inicio(fotos), _servicos(fotos), _primeiro_olhar(), _avaliacoes(), _quem_faz(fotos),
              _combos_pacotes(), _manutencao(), _como_chegar(), _perguntas()]
    corpo = "\n".join(s for s in secoes if s)
    return head + "<main>\n" + corpo + "\n</main>\n" + _rodape() + "\n</body>\n</html>\n"
