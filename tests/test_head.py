from head import render_head


def test_head_tem_titulo_descricao_canonical_e_css_versionado():
    h = render_head("Título", "Descrição", "/academy/", [], css_versao="abc12345")
    assert h.startswith("<!DOCTYPE html>")
    assert "<title>Título</title>" in h
    assert '<meta name="description" content="Descrição">' in h
    assert '<link rel="canonical" href="https://rainhadoolhar.com.br/academy/">' in h
    assert 'href="/static/style.css?v=abc12345"' in h
    assert h.rstrip().endswith("<body>")
    assert "googletagmanager" not in h


def test_head_com_gtm_quando_informado():
    h = render_head("T", "D", "/", ['<script type="application/ld+json">{}</script>'],
                    css_versao="x", gtm_id="GTM-TESTE1")
    assert h.count("GTM-TESTE1") == 2
    assert '<script type="application/ld+json">{}</script>' in h
