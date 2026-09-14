import re
import build as modulo
from page_studio import render_studio
from data import NEGOCIO, ALT_FOTOS, FOTO_SERVICO, PACOTES

FOTOS = {nome: {"larguras": [480, 960], "w": 960, "h": 1200} for nome in ALT_FOTOS}


def pagina():
    return render_studio(FOTOS, css_versao="teste")


def test_tem_as_nove_secoes_na_ordem():
    ids = re.findall(r'<section id="([a-z-]+)"', pagina())
    assert ids == ["inicio", "servicos", "primeiro-olhar", "avaliacoes", "quem-faz",
                   "combos-pacotes", "manutencao", "como-chegar", "perguntas"]


def test_nao_existe_mais_secao_resultados():
    assert 'id="resultados"' not in pagina()
    assert 'class="galeria"' not in pagina()


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


def test_combos_pacotes_sem_aviso_repetido():
    h = pagina()
    assert "O pacote é fechado no atendimento." not in h
    assert h.count("você agenda a primeira sessão e fecha o pacote com a Laryssa no dia.") == 1
    for p in PACOTES:
        assert p["nome"] in h


def test_regua_dos_21_dias():
    h = pagina()
    assert "Depois de 21 dias" in h


def test_sem_fotos_a_pagina_nao_mostra_nenhuma_imagem_de_conteudo():
    h = render_studio({}, css_versao="teste")
    assert 'src="/img/' not in h
    assert 'id="servicos"' in h and 'id="quem-faz"' in h and 'id="inicio"' in h


def test_barra_fixa_e_ficha_do_negocio():
    h = pagina()
    assert 'class="barra-agendar"' in h
    assert '"@type": "BeautySalon"' in h


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


def test_instagram_no_fim_de_servicos_sem_espaco_antes_de_fechar_o_link():
    h = pagina()
    m = re.search(r'<a href="https://www\.instagram\.com/rainhadoolhar_/"[^>]*>([^<]*)</a>', h)
    assert m, "link do Instagram não encontrado"
    assert m.group(1) == "Ver mais no Instagram @rainhadoolhar_"
    assert not m.group(1).endswith(" ")


# --- Hero com foto ---

def test_hero_com_foto_carrega_eager_e_com_prioridade():
    h = pagina()
    assert 'id="inicio"' in h
    trecho_hero = h.split('id="servicos"')[0]
    assert "hero-960.webp" in trecho_hero
    assert 'loading="eager"' in trecho_hero
    assert 'fetchpriority="high"' in trecho_hero
    assert ALT_FOTOS["hero"] in trecho_hero


def test_hero_mantem_h1_e_cta_originais():
    h = pagina()
    assert "<h1>Um olhar pra cada mulher. <em>Escolha o seu.</em></h1>" in h
    assert 'data-cta="hero"' in h


def test_hero_sem_foto_nao_quebra():
    h = render_studio({}, css_versao="teste")
    assert 'id="inicio"' in h
    assert "<h1>Um olhar pra cada mulher. <em>Escolha o seu.</em></h1>" in h
    assert 'class="hero-foto"' not in h


# --- Serviços viram cartão com foto quando existe foto ---

def test_servicos_com_foto_viram_cartoes():
    h = pagina()
    assert h.count('class="cartao-servico"') == len(FOTO_SERVICO)
    for nome, foto in FOTO_SERVICO.items():
        assert f"{foto}-960.webp" in h
        assert nome in h


def test_servico_sem_foto_cai_para_lista_compacta_quando_falta_a_foto():
    fotos = {n: v for n, v in FOTOS.items() if n != "sobrancelha-reconstrucao"}
    h = render_studio(fotos, css_versao="teste")
    assert h.count('class="cartao-servico"') == len(FOTO_SERVICO) - 1
    assert "Reconstrução de sobrancelhas" in h
    assert "sobrancelha-reconstrucao" not in h


def test_servicos_sem_mapeamento_de_foto_ficam_em_lista_compacta():
    h = pagina()
    sem_foto = ["Manutenção (até 21 dias)", "Lash lifting", "Remoção", "Design masculino",
                "Micropigmentação ou microblading", "Epilação de buço", "Micropigmentação labial"]
    for nome in sem_foto:
        assert nome not in FOTO_SERVICO
        assert nome in h


def test_cartao_servico_tem_botao_agendar_com_rastreio():
    h = pagina()
    assert re.search(r'class="cartao-servico">.*?data-cta="servico-cilios-classico"', h, re.S)
