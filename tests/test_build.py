import pytest
from PIL import Image
import build as modulo
from build import build
from components import verificar_texto
from images import FOTOS_OBRIGATORIAS


def _fotos(pasta):
    pasta.mkdir()
    for nome in FOTOS_OBRIGATORIAS:
        Image.new("RGB", (1080, 1350), (190, 170, 150)).save(pasta / f"{nome}.jpg")


def test_build_completo_gera_paginas_e_assets(tmp_path):
    _fotos(tmp_path / "fotos")
    saida = tmp_path / "dist"
    build(saida, tmp_path / "fotos", exigir_fotos=True)
    for rel in ["index.html", "academy/index.html", "static/style.css", "static/ornamento.svg",
                "static/logo-lockup.png", "img/og.jpg", "img/studio-960.webp", "robots.txt", "sitemap.xml"]:
        assert (saida / rel).exists(), rel
    assert "?v=" in (saida / "index.html").read_text(encoding="utf-8")


def test_build_sem_foto_obrigatoria_falha_listando(tmp_path):
    (tmp_path / "fotos").mkdir()
    with pytest.raises(SystemExit) as erro:
        build(tmp_path / "dist", tmp_path / "fotos", exigir_fotos=True)
    assert "laryssa" in str(erro.value)


def test_build_previa_sem_fotos(tmp_path):
    (tmp_path / "fotos").mkdir()
    build(tmp_path / "dist", tmp_path / "fotos", exigir_fotos=False)
    assert 'id="resultados"' not in (tmp_path / "dist" / "index.html").read_text(encoding="utf-8")


def test_build_barra_texto_proibido(tmp_path, monkeypatch):
    monkeypatch.setattr(modulo, "render_academy",
                        lambda css_versao, gtm_id=None: "<html><body><p>Um tratamento</p></body></html>")
    (tmp_path / "fotos").mkdir()
    with pytest.raises(SystemExit) as erro:
        build(tmp_path / "dist", tmp_path / "fotos", exigir_fotos=False)
    assert "tratamento" in str(erro.value)


def test_paginas_reais_passam_na_regra_de_texto(tmp_path):
    (tmp_path / "fotos").mkdir()
    build(tmp_path / "dist", tmp_path / "fotos", exigir_fotos=False)
    for rel in ["index.html", "academy/index.html"]:
        pagina = (tmp_path / "dist" / rel).read_text(encoding="utf-8")
        assert verificar_texto(modulo._texto_visivel(pagina)) == [], rel


def test_paginas_reais_nao_mostram_precos(tmp_path):
    (tmp_path / "fotos").mkdir()
    build(tmp_path / "dist", tmp_path / "fotos", exigir_fotos=False)
    for rel in ["index.html", "academy/index.html"]:
        pagina = (tmp_path / "dist" / rel).read_text(encoding="utf-8")
        assert "R$" not in pagina, rel
