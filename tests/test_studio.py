import re
import build as modulo
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


def test_pagina_nao_mostra_nenhum_preco():
    h = pagina()
    assert "R$" not in modulo._texto_visivel(h)
    assert "R$" not in h
    assert "<s>" not in h
    assert 'class="preco"' not in h
    assert 'class="preco-grande"' not in h
    assert 'class="preco-oferta"' not in h


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


def test_galeria_nao_quebra_sem_a_foto_de_reconstrucao():
    fotos = {n: v for n, v in FOTOS.items() if n != "sobrancelha-reconstrucao"}
    h = render_studio(fotos, css_versao="teste")
    assert "sobrancelha-reconstrucao" not in h
    assert 'id="resultados"' in h


def test_galeria_completa_com_a_foto_de_reconstrucao():
    h = pagina()
    assert "sobrancelha-reconstrucao-960.webp" in h


def test_antes_depois_micropigmentacao_aparece_com_as_duas_fotos():
    h = pagina()
    assert "micropigmentacao-antes-960.webp" in h
    assert "micropigmentacao-depois-960.webp" in h
    assert ALT_FOTOS["micropigmentacao-antes"] in h
    assert ALT_FOTOS["micropigmentacao-depois"] in h
    assert h.count(">Antes<") == 1
    assert h.count(">Depois<") == 1


def test_antes_depois_micropigmentacao_some_sem_as_duas_fotos():
    fotos = {n: v for n, v in FOTOS.items() if n not in ("micropigmentacao-antes", "micropigmentacao-depois")}
    h = render_studio(fotos, css_versao="teste")
    assert "micropigmentacao-antes" not in h
    assert "micropigmentacao-depois" not in h
    assert ">Antes<" not in h and ">Depois<" not in h


def test_antes_depois_some_se_so_uma_das_duas_existir():
    fotos = {n: v for n, v in FOTOS.items() if n != "micropigmentacao-depois"}
    h = render_studio(fotos, css_versao="teste")
    assert "micropigmentacao-antes" not in h
    assert "micropigmentacao-depois" not in h
