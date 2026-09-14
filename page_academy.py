"""Página da Academy: cursos com preço e contato pelo WhatsApp."""
from components import esc, brl, cta, ornamento
from data import NEGOCIO, CURSOS, ADICIONAL_FOTOS, PAGAMENTO_CURSOS, AVALIACAO_ACADEMY
from head import render_head
from schema import curso, jsonld_script

TITULO = "Curso de micropigmentação no Rio de Janeiro | Rainha do Olhar Academy"
DESCRICAO = ("Formação em micropigmentação de sobrancelhas e cursos particulares de design e extensão de cílios, "
             "presenciais no Rio Comprido, com prática em modelo real.")
BOTAO = "Quero saber das próximas datas"


def _curso(c):
    de = f"<s>{brl(c['de'])}</s> " if c.get("de") else ""
    inclui = "".join(f"<li>{esc(item)}</li>" for item in c["inclui"])
    aviso = f'<p class="aviso">{esc(c["aviso"])}</p>' if c.get("aviso") else ""
    return (f'<article class="cartao"><h3>{esc(c["nome"])}</h3><p class="formato">{esc(c["formato"])}</p>'
            f'<p class="preco-oferta">{de}{brl(c["preco"])}</p><ul class="inclui">{inclui}</ul>{aviso}</article>')


def render_academy(css_versao, gtm_id=None):
    n = NEGOCIO
    a = AVALIACAO_ACADEMY
    micro = "".join(_curso(c) for c in CURSOS if c["grupo"] == "micropigmentacao")
    particulares = "".join(_curso(c) for c in CURSOS if c["grupo"] == "design-cilios")
    head = render_head(TITULO, DESCRICAO, "/academy/", [jsonld_script(curso(c)) for c in CURSOS], css_versao, gtm_id)
    corpo = f'''<section id="inicio" class="hero">
  <img class="hero-logo" src="/static/logo-lockup.png" alt="{esc(n['nome'])} Academy" width="398" height="178">
  <p class="eyebrow">Rainha do Olhar Academy</p>
  <h1>Aprenda com quem <em>forma profissionais.</em></h1>
  <p class="lead">Cursos presenciais no studio do {esc(n['bairro'])}, com prática em modelo real. Já são mais de 100 alunas formadas.</p>
  {cta(n['whatsapp_url'], BOTAO, "academy-hero")}
</section>
<section id="micropigmentacao">
  {ornamento()}
  <h2>Formação em micropigmentação de sobrancelhas</h2>
  <div class="cartoes">{micro}</div>
</section>
<section id="design-cilios">
  {ornamento()}
  <h2>Cursos particulares de design e cílios</h2>
  <p class="secao-intro">Aula individual: cada data é de uma aluna só.</p>
  <div class="cartoes">{particulares}</div>
  <blockquote class="avaliacao"><p>“{esc(a['texto'])}”</p><footer>{esc(a['nome'])} · avaliação no Google</footer></blockquote>
</section>
<section id="pagamento">
  <h2>Valores e pagamento</h2>
  <p>{esc(PAGAMENTO_CURSOS)}.</p>
  <p>Adicional: pacote de fotos prontas para o seu portfólio, {brl(ADICIONAL_FOTOS)}. As fotos e vídeos do atendimento que você faz no curso já estão inclusos.</p>
  <p>Curso não garante agenda cheia. Garante técnica, biossegurança e prática de verdade.</p>
</section>
<section id="contato" class="destaque">
  <h2>Quer saber das próximas datas?</h2>
  <p>Me chama no WhatsApp e eu te explico qual curso combina com o seu momento.</p>
  {cta(n['whatsapp_url'], BOTAO, "academy-contato")}
</section>'''
    rodape = f'''<footer class="rodape">
  <img src="/static/logo-monograma.png" alt="" width="46" height="50">
  <p>{esc(n['nome'])} · {esc(n['assinatura'])}</p>
  <p><a href="/">Studio</a> · <a href="{esc(n['instagram_url'])}" target="_blank" rel="noopener">@{esc(n['instagram_usuario'])}</a></p>
</footer>
<div class="barra-agendar">{cta(n['whatsapp_url'], BOTAO, "barra-fixa")}</div>'''
    return head + "<main>\n" + corpo + "\n</main>\n" + rodape + "\n</body>\n</html>\n"
