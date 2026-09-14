import json
import re
from page_academy import render_academy
from data import NEGOCIO


def pagina():
    return render_academy(css_versao="teste")


def test_precos_dos_cursos():
    h = pagina()
    for valor in ["R$1.497", "R$2.297", "R$797", "R$997", "R$1.597", "R$1.794", "R$100"]:
        assert valor in h, valor


def test_botoes_vao_para_o_whatsapp():
    botoes = re.findall(r'<a [^>]*href="([^"]+)"[^>]*>Quero saber das próximas datas</a>', pagina())
    assert len(botoes) == 3
    assert set(botoes) == {NEGOCIO["whatsapp_url"]}


def test_depoimento_da_myllena_so_no_bloco_de_design_e_cilios():
    h = pagina()
    bloco = h.split('<section id="design-cilios">')[1].split("</section>")[0]
    assert "Myllena Andrade" in bloco
    assert h.count("Myllena Andrade") == 1


def test_um_course_por_curso_no_jsonld():
    blocos = re.findall(r'<script type="application/ld\+json">(.*?)</script>', pagina(), re.S)
    assert [json.loads(b)["@type"] for b in blocos].count("Course") == 5


def test_kit_nao_incluso_e_pagamento_a_combinar():
    h = pagina()
    assert "O kit profissional não está incluso" in h
    assert "Formas de pagamento e parcelamento a combinar" in h
