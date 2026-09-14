import re
from page_studio import render_studio
from data import NEGOCIO, ALT_FOTOS

FOTOS = {nome: {"larguras": [480, 960], "w": 960, "h": 1200} for nome in ALT_FOTOS}


def pagina():
    return render_studio(FOTOS, css_versao="teste")


def test_tem_as_dez_secoes_na_ordem():
    ids = re.findall(r'<section id="([a-z-]+)"', pagina())
    assert ids == ["inicio", "resultados", "servicos", "primeiro-olhar", "combos-pacotes",
                   "manutencao", "quem-faz", "avaliacoes", "como-chegar", "perguntas"]


def test_todo_botao_de_agendar_vai_para_o_maapp():
    botoes = re.findall(r'<a [^>]*href="([^"]+)"[^>]*>(?:Agendar|Quero)[^<]*</a>', pagina())
    assert len(botoes) >= 9
    assert set(botoes) == {NEGOCIO["maapp_url"]}


def test_precos_de_servicos_ofertas_e_pacotes():
    h = pagina()
    for valor in ["R$180", "R$150", "R$600", "R$315", "R$220", "R$295", "R$200", "R$395", "R$372", "R$285"]:
        assert valor in h, valor


def test_nap_instagram_e_prova_social():
    h = pagina()
    assert NEGOCIO["endereco_completo"] in h
    assert 'href="https://www.instagram.com/rainhadoolhar_/"' in h
    assert "5,0 no Google" in h and "43 avaliações" in h


def test_aviso_dos_pacotes_e_regua_dos_21_dias():
    h = pagina()
    assert h.count("O pacote é fechado no atendimento.") == 3
    assert "Depois de 21 dias" in h


def test_sem_fotos_a_galeria_some_e_o_resto_fica():
    h = render_studio({}, css_versao="teste")
    assert 'id="resultados"' not in h and 'src="/img/' not in h
    assert 'id="servicos"' in h and 'id="quem-faz"' in h


def test_barra_fixa_e_ficha_do_negocio():
    h = pagina()
    assert 'class="barra-agendar"' in h
    assert '"@type": "BeautySalon"' in h
