import json
import re
from pathlib import Path
import build as modulo
from page_academy import render_academy
from data import NEGOCIO, ALT_FOTOS, FAQ_ACADEMY

FOTOS = {nome: {"larguras": [480, 960], "w": 960, "h": 1200} for nome in ALT_FOTOS}

SECOES = ["inicio", "para-quem", "o-que-leva", "micropigmentacao", "design-cilios",
          "onde-e", "prova", "perguntas", "pagamento", "contato"]


def pagina(fotos=None):
    return render_academy(FOTOS if fotos is None else fotos, css_versao="teste")


def test_pagina_nao_mostra_nenhum_preco():
    h = pagina()
    assert "R$" not in modulo._texto_visivel(h)
    assert "R$" not in h
    assert "<s>" not in h
    assert 'class="preco-oferta"' not in h


def test_botoes_vao_para_o_whatsapp():
    botoes = re.findall(r'<a [^>]*href="([^"]+)"[^>]*>Quero saber das próximas datas</a>', pagina())
    assert len(botoes) == 3
    assert set(botoes) == {NEGOCIO["whatsapp_url"]}


def test_todo_botao_da_academy_vai_para_o_whatsapp():
    hrefs = re.findall(r'<a class="btn[^"]*" href="([^"]+)"', pagina())
    assert len(hrefs) == 5
    assert set(hrefs) == {NEGOCIO["whatsapp_url"]}


def test_um_course_por_curso_no_jsonld():
    blocos = re.findall(r'<script type="application/ld\+json">(.*?)</script>', pagina(), re.S)
    assert [json.loads(b)["@type"] for b in blocos].count("Course") == 5


def test_kit_nao_incluso_e_pagamento_a_combinar():
    h = pagina()
    assert "O kit profissional não está incluso" in h
    assert "Formas de pagamento e parcelamento a combinar" in h


# --- identidade própria (tema escuro escopado no body) ---

def test_body_da_academy_tem_a_classe_academy_e_cor_de_tema_escura():
    h = pagina()
    assert '<body class="academy">' in h
    assert '<meta name="theme-color" content="#17120C">' in h


def test_hero_da_academy_usa_a_classe_que_existe_no_css():
    css = (Path(__file__).resolve().parents[1] / "static" / "style.css").read_text(encoding="utf-8")
    assert 'class="ac-hero"' in pagina()
    assert "body.academy .ac-hero{" in css
    assert "body.academy .ac-hero p{" in css


def test_as_dez_secoes_na_ordem_do_brief():
    assert re.findall(r'<section id="([a-z-]+)"', pagina()) == SECOES


# --- prova social ---

def test_selo_do_topo_traz_alunas_e_a_nota_do_google():
    h = pagina().split('</section>')[0]
    assert "Mais de 100 alunas formadas" in h
    assert f"{NEGOCIO['nota_google']} no Google com {NEGOCIO['avaliacoes_google']} avaliações" in h


def test_myllena_fica_na_secao_de_prova_e_fora_da_micropigmentacao():
    h = pagina()
    assert h.count("Myllena Andrade") == 1
    micro = h.split('<section id="micropigmentacao">')[1].split("</section>")[0]
    assert "Myllena" not in micro
    prova = h.split('<section id="prova">')[1].split("</section>")[0]
    assert "Myllena Andrade" in prova
    assert "avaliação no Google" in prova
    assert h.index('<section id="design-cilios">') < h.index('<section id="prova">')


# --- perguntas frequentes da Academy ---

def test_faq_da_academy_vem_de_data_py_e_nao_do_html():
    h = pagina()
    perguntas = h.split('<section id="perguntas">')[1].split("</section>")[0]
    assert perguntas.count("<details>") == len(FAQ_ACADEMY) == 6
    for q, r in FAQ_ACADEMY:
        assert f"<summary>{q}</summary>" in perguntas
        assert r in perguntas


def test_frase_de_expectativa_no_pagamento():
    pag = pagina().split('<section id="pagamento">')[1].split("</section>")[0]
    assert "Curso não garante agenda cheia." in pag
    assert "Garante técnica, biossegurança e prática de verdade." in pag


# --- fotos, todas opcionais ---

def test_fotos_entram_quando_existem():
    h = pagina()
    for nome in ["laryssa", "studio", "micropigmentacao-antes", "micropigmentacao-depois",
                 "sobrancelha-design"]:
        assert f'/img/{nome}-960.webp' in h, nome
        assert ALT_FOTOS[nome] in h, nome


def test_pagina_sem_nenhuma_foto_mantem_as_secoes_e_nao_quebra():
    h = pagina(fotos={})
    assert re.findall(r'<section id="([a-z-]+)"', h) == SECOES
    assert "/img/" not in h.replace("/img/og.jpg", "")
    assert NEGOCIO["endereco_completo"] in h


def test_antes_e_depois_so_aparece_com_as_duas_fotos():
    so_antes = {"micropigmentacao-antes": FOTOS["micropigmentacao-antes"]}
    h = pagina(fotos=so_antes)
    assert "micropigmentacao-antes" not in h
    assert "Antes" not in h


def test_legendas_dizem_que_o_trabalho_e_da_laryssa():
    h = pagina()
    assert "Micropigmentação feita pela Laryssa" in h
    assert "Mapeamento feito pela Laryssa" in h


# --- onde é ---

def test_onde_e_traz_endereco_e_maps_sem_iframe():
    onde = pagina().split('<section id="onde-e">')[1].split("</section>")[0]
    assert NEGOCIO["endereco_completo"] in onde
    assert f'href="{NEGOCIO["maps_url"]}"' in onde
    assert "Abrir no Google Maps" in onde
    assert "<iframe" not in pagina()


# --- para quem é / o que você leva ---

def test_tres_perfis_e_seis_itens():
    h = pagina()
    perfis = h.split('<section id="para-quem">')[1].split("</section>")[0]
    assert perfis.count("<h3>") == 3
    leva = h.split('<section id="o-que-leva">')[1].split("</section>")[0]
    assert leva.count("<h3>") == 6
