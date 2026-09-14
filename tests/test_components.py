from components import esc, verificar_texto, cta, imagem, ornamento


def test_esc_protege_html():
    assert esc('<b>"x"</b>') == "&lt;b&gt;&quot;x&quot;&lt;/b&gt;"


def test_verificar_texto_pega_termos_proibidos_na_ordem():
    assert verificar_texto("Um tratamento — permanente") == ["—", "tratamento", "permanente"]
    assert verificar_texto("Longa duração, com paciência e cuidado") == []


def test_cta_abre_em_nova_aba_com_rastreio():
    html = cta("https://online.maapp.com.br/Rainhadoolhar", "Agendar horário", "hero")
    assert 'href="https://online.maapp.com.br/Rainhadoolhar"' in html
    assert 'target="_blank"' in html and 'rel="noopener"' in html
    assert 'data-cta="hero"' in html and ">Agendar horário</a>" in html
    assert 'class="btn btn-primario"' in html


def test_imagem_tem_srcset_e_dimensoes():
    html = imagem("studio", {"larguras": [480, 960], "w": 960, "h": 1200}, "Espaço do studio")
    assert 'src="/img/studio-960.webp"' in html
    assert 'srcset="/img/studio-480.webp 480w, /img/studio-960.webp 960w"' in html
    assert 'width="960" height="1200"' in html and 'loading="lazy"' in html


def test_ornamento_e_decorativo():
    assert 'alt=""' in ornamento() and "/static/ornamento.svg" in ornamento()
