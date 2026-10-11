"""Página da Academy: tema escuro próprio, cursos e contato pelo WhatsApp.

A identidade escura mora na classe academy do <body> (ver static/style.css).
Toda foto é opcional: sem o arquivo, a seção continua de pé, só sem imagem.
"""
from components import esc, cta, imagem, ornamento
from data import (NEGOCIO, CURSOS, PAGAMENTO_CURSOS, AVALIACAO_ACADEMY, FAQ_ACADEMY,
                  ALT_FOTOS)
from head import render_head
from schema import curso, jsonld_script

TITULO = "Curso de micropigmentação no Rio de Janeiro | Rainha do Olhar Academy"
DESCRICAO = ("Formação em micropigmentação de sobrancelhas e cursos particulares de design e extensão de cílios, "
             "presenciais no Rio Comprido, com prática em modelo real.")
BOTAO = "Quero saber das próximas datas"
CLASSE_BODY = "academy"
COR_TEMA = "#17120C"

# Para quem é. Fala da intenção de quem lê, nunca do resultado que ela vai ter.
PERFIS = [
    ("Você quer começar do zero",
     "Nunca pegou numa pinça e quer aprender uma profissão nova, da aula teórica ao primeiro atendimento."),
    ("Você já faz cílios",
     "Quer somar a sobrancelha ao que já oferece e atender a mesma cliente por dois motivos."),
    ("Você já atende e quer subir o ticket",
     "Quer entrar na micropigmentação de sobrancelhas com técnica, colorimetria e prática em modelo real."),
]

# O que você leva. Cada linha só repete o que já está no "inclui" dos cursos em data.CURSOS.
LEVA = [
    ("Técnica e biossegurança",
     "Aula teórica completa, biossegurança, visagismo, marcação, colorimetria e tipos de pele."),
    ("Prática em modelo real",
     "Na micropigmentação, treino em pele sintética antes. Nos particulares, modelo real no segundo dia."),
    ("Apostila e certificado",
     "Apostila em PDF, também física nos cursos particulares e na VIP, e certificado em todos."),
    ("Suporte depois do curso",
     "3 meses na Formação Profissional, 6 meses na VIP e até 6 meses nos particulares."),
    ("Fotos e vídeos para o portfólio",
     "As imagens do atendimento que você faz no curso saem de lá com você."),
    ("Orientação para começar a atender",
     "Cuidados antes e depois, materiais, equipamentos e acompanhamento nos primeiros atendimentos."),
]


def _fio():
    """Fio dourado de 1px com o ornamento da marca no meio."""
    return f'<div class="ac-fio">{ornamento()}</div>'


def _rotulo(texto):
    return f'<p class="eyebrow">{esc(texto)}</p>'


def _figura(fotos, nome, legenda, sizes, classe="ac-foto", carregar="lazy", prioridade=False):
    """Figura só existe quando a foto existe. Sem foto, devolve string vazia."""
    if not fotos or not fotos.get(nome):
        return ""
    img = imagem(nome, fotos[nome], ALT_FOTOS[nome], sizes=sizes,
                 carregar=carregar, prioridade=prioridade)
    legenda_html = f"<figcaption>{esc(legenda)}</figcaption>" if legenda else ""
    return f'<figure class="{classe}"><div class="ac-moldura">{img}</div>{legenda_html}</figure>'


def _curso(c):
    inclui = "".join(f"<li>{esc(item)}</li>" for item in c["inclui"])
    aviso = f'<p class="aviso">{esc(c["aviso"])}</p>' if c.get("aviso") else ""
    return (f'<article class="ac-curso"><h3>{esc(c["nome"])}</h3>'
            f'<p class="formato">{esc(c["formato"])}</p>'
            f'<ul class="inclui">{inclui}</ul>{aviso}</article>')


def _curso_enxuto(c):
    return (f'<article class="ac-curso ac-curso-enxuto"><h3>{esc(c["nome"])}</h3>'
            f'<p class="formato">{esc(c["formato"])}</p></article>')


def _cursos(grupo):
    return "".join(_curso(c) for c in CURSOS if c["grupo"] == grupo)


def _inclui_comum(cursos):
    """Quando os cursos do grupo incluem exatamente a mesma coisa, a lista aparece uma vez só."""
    primeiro = cursos[0]["inclui"]
    return primeiro if all(c["inclui"] == primeiro for c in cursos[1:]) else None


def _inicio(fotos):
    n = NEGOCIO
    foto = _figura(fotos, "laryssa", "", sizes="(min-width: 760px) 44vw, 100vw",
                   classe="ac-foto ac-hero-foto", carregar="eager", prioridade=True)
    return f'''<section id="inicio" class="ac-hero">
  <div class="ac-hero-texto">
    <img class="ac-logo" src="/static/logo-lockup-creme.png" alt="" width="398" height="178">
    {_rotulo("Rainha do Olhar Academy")}
    <h1>Aprenda com quem <em>forma profissionais.</em></h1>
    <p class="lead">Formação em micropigmentação e cursos particulares de design e cílios, presenciais no studio do {esc(n['bairro'])}, com prática em modelo real.</p>
    {cta(n['whatsapp_url'], BOTAO, "academy-hero")}
    <p class="ac-selo"><span>Mais de 100 alunas formadas</span><span>{esc(n['nota_google'])} no Google com {n['avaliacoes_google']} avaliações</span></p>
  </div>
  {foto}
</section>'''


def _para_quem():
    itens = "".join(
        f'<article class="ac-perfil"><h3>{esc(titulo)}</h3><p>{esc(texto)}</p></article>'
        for titulo, texto in PERFIS)
    return f'''<section id="para-quem">
  {_rotulo("Para quem é")}
  <h2>Três mulheres diferentes entram <em>na mesma sala.</em></h2>
  <div class="ac-perfis">{itens}</div>
</section>'''


def _o_que_leva():
    itens = "".join(
        f'<article class="ac-item"><span class="ac-num">{i:02d}</span>'
        f'<h3>{esc(titulo)}</h3><p>{esc(texto)}</p></article>'
        for i, (titulo, texto) in enumerate(LEVA, 1))
    return f'''<section id="o-que-leva">
  {_rotulo("O que você leva")}
  <h2>Sai de lá com <em>a técnica na mão.</em></h2>
  <div class="ac-itens">{itens}</div>
</section>'''


def _antes_depois(fotos):
    if not fotos or not fotos.get("micropigmentacao-antes") or not fotos.get("micropigmentacao-depois"):
        return ""
    sizes = "(min-width: 760px) 18vw, 44vw"
    antes = imagem("micropigmentacao-antes", fotos["micropigmentacao-antes"],
                   ALT_FOTOS["micropigmentacao-antes"], sizes=sizes)
    depois = imagem("micropigmentacao-depois", fotos["micropigmentacao-depois"],
                    ALT_FOTOS["micropigmentacao-depois"], sizes=sizes)
    return f'''<div class="ac-lado">
    <div class="ac-par">
      <figure class="ac-foto"><div class="ac-moldura">{antes}</div><figcaption>Antes</figcaption></figure>
      <figure class="ac-foto"><div class="ac-moldura">{depois}</div><figcaption>Depois</figcaption></figure>
    </div>
    <p class="ac-credito">Micropigmentação feita pela Laryssa, não por aluna.</p>
  </div>'''


def _micropigmentacao(fotos):
    return f'''<section id="micropigmentacao">
  {_rotulo("Formação")}
  <h2>Micropigmentação <em>de sobrancelhas.</em></h2>
  <p class="secao-intro">Dois caminhos para a mesma formação: a Profissional e a VIP, individual e com kit profissional para levar.</p>
  <div class="ac-colunas">
    <div class="ac-cursos">{_cursos("micropigmentacao")}
      {cta(NEGOCIO['whatsapp_url'], "Falar sobre a formação", "academy-micro", "secundario")}
    </div>
    {_antes_depois(fotos)}
  </div>
</section>'''


def _design_cilios(fotos):
    cursos = [c for c in CURSOS if c["grupo"] == "design-cilios"]
    comum = _inclui_comum(cursos)
    cartoes = "".join((_curso_enxuto(c) if comum else _curso(c)) for c in cursos)
    lista = ""
    if comum:
        itens = "".join(f"<li>{esc(item)}</li>" for item in comum)
        lista = (f'<div class="ac-comum"><h3>Os três incluem</h3>'
                 f'<ul class="inclui">{itens}</ul></div>')
    foto = _figura(fotos, "sobrancelha-design", "Mapeamento feito pela Laryssa, no studio.",
                   sizes="(min-width: 760px) 34vw, 100vw")
    lado = f'<div class="ac-lado">{foto}</div>' if foto else ""
    return f'''<section id="design-cilios">
  {_rotulo("Cursos particulares")}
  <h2>Design de sobrancelhas <em>e extensão de cílios.</em></h2>
  <p class="secao-intro">Aula individual: cada data é de uma aluna só.</p>
  <div class="ac-colunas">
    <div class="ac-cursos">{cartoes}</div>
    {lado}
  </div>
  {lista}
  <div class="centro">{cta(NEGOCIO['whatsapp_url'], "Falar sobre os particulares", "academy-particulares", "secundario")}</div>
</section>'''


def _onde_e(fotos):
    n = NEGOCIO
    foto = _figura(fotos, "studio", "", sizes="(min-width: 760px) 44vw, 100vw",
                   classe="ac-foto ac-foto-larga")
    # O href do Maps vai sem escape de propósito: o parâmetro query precisa chegar inteiro,
    # do jeito que o Google espera, e é um endereço fixo de data.py (não vem de fora).
    return f'''<section id="onde-e">
  {foto}
  <div class="ac-onde-texto">
    {_rotulo("Onde é")}
    <h2>No studio do <em>Rio Comprido.</em></h2>
    <p>Você aprende na mesma sala em que a Laryssa atende, com os materiais e os equipamentos do dia a dia.</p>
    <address>{esc(n['endereco_completo'])}</address>
    <p><a class="ac-link" href="{n['maps_url']}" target="_blank" rel="noopener">Abrir no Google Maps</a></p>
  </div>
</section>'''


def _prova():
    a = AVALIACAO_ACADEMY
    return f'''<section id="prova">
  {_rotulo("Prova")}
  <blockquote class="ac-prova">
    <p>“{esc(a['texto'])}”</p>
    <footer>{esc(a['nome'])} · avaliação no Google</footer>
  </blockquote>
</section>'''


def _perguntas():
    itens = "".join(f"<details><summary>{esc(q)}</summary><p>{esc(r)}</p></details>"
                    for q, r in FAQ_ACADEMY)
    return f'''<section id="perguntas">
  {_rotulo("Perguntas frequentes")}
  <h2>O que as alunas <em>perguntam antes.</em></h2>
  <div class="faq ac-faq">{itens}</div>
</section>'''


def _pagamento():
    return f'''<section id="pagamento">
  <div class="ac-pagamento-texto">
    {_rotulo("Pagamento")}
    <h2>A gente combina <em>no WhatsApp.</em></h2>
    <p>{esc(PAGAMENTO_CURSOS)}.</p>
    <p>Adicional: pacote de fotos prontas para o seu portfólio. As fotos e vídeos do atendimento que você faz no curso já estão inclusos.</p>
  </div>
  <p class="ac-promessa">Curso não garante agenda cheia. <em>Garante técnica, biossegurança e prática de verdade.</em></p>
</section>'''


def _contato():
    n = NEGOCIO
    return f'''<section id="contato">
  {_fio()}
  <div class="ac-final">
    <h2>Quer saber das <em>próximas datas?</em></h2>
    <p>Me chama no WhatsApp e eu te explico qual curso combina com o seu momento.</p>
    {cta(n['whatsapp_url'], BOTAO, "academy-contato")}
  </div>
</section>'''


def _rodape():
    n = NEGOCIO
    return f'''<footer class="rodape">
  <img src="/static/logo-monograma-dourado.png" alt="" width="46" height="50">
  <p>{esc(n['nome'])} · {esc(n['assinatura'])}</p>
  <p><a href="/">Studio</a> · <a href="{esc(n['instagram_url'])}" target="_blank" rel="noopener">@{esc(n['instagram_usuario'])}</a></p>
</footer>
<div class="barra-agendar">{cta(n['whatsapp_url'], BOTAO, "barra-fixa")}</div>'''


def render_academy(fotos, css_versao, gtm_id=None):
    head = render_head(TITULO, DESCRICAO, "/academy/", [jsonld_script(curso(c)) for c in CURSOS],
                       css_versao, gtm_id, classe_body=CLASSE_BODY, cor_tema=COR_TEMA)
    secoes = [_inicio(fotos), _para_quem(), _o_que_leva(), _micropigmentacao(fotos),
              _design_cilios(fotos), _onde_e(fotos), _prova(), _perguntas(), _pagamento(), _contato()]
    return head + "<main>\n" + "\n".join(secoes) + "\n</main>\n" + _rodape() + "\n</body>\n</html>\n"
