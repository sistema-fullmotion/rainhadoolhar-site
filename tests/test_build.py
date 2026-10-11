import copy
import json
import re
import shutil

import pytest
from PIL import Image
import build as modulo
from build import build
from components import verificar_texto
from images import FOTOS_OBRIGATORIAS, faltando


def _fotos(pasta):
    pasta.mkdir()
    for nome in FOTOS_OBRIGATORIAS:
        Image.new("RGB", (1080, 1350), (190, 170, 150)).save(pasta / f"{nome}.jpg")
    Image.new("RGB", (1080, 1350), (190, 170, 150)).save(pasta / "studio.jpg")


def test_build_completo_gera_paginas_e_assets(tmp_path):
    _fotos(tmp_path / "fotos")
    saida = tmp_path / "dist"
    build(saida, tmp_path / "fotos", exigir_fotos=True)
    for rel in ["index.html", "academy/index.html", "static/style.css", "static/ornamento.svg",
                "static/logo-lockup.png", "img/og.jpg", "img/studio-960.webp", "robots.txt", "sitemap.xml"]:
        assert (saida / rel).exists(), rel
    assert "?v=" in (saida / "index.html").read_text(encoding="utf-8")


def test_build_funciona_sem_a_foto_de_reconstrucao(tmp_path):
    pasta = tmp_path / "fotos"
    _fotos(pasta)
    assert not (pasta / "sobrancelha-reconstrucao.jpg").exists()
    saida = tmp_path / "dist"
    build(saida, pasta, exigir_fotos=True)
    pagina = (saida / "index.html").read_text(encoding="utf-8")
    assert "sobrancelha-reconstrucao" not in pagina
    assert not (saida / "img" / "sobrancelha-reconstrucao-960.webp").exists()
    assert (saida / "img" / "studio-960.webp").exists()


def test_build_funciona_sem_a_foto_do_studio_e_og_usa_outra_foto(tmp_path):
    pasta = tmp_path / "fotos"
    _fotos(pasta)
    (pasta / "studio.jpg").unlink()
    saida = tmp_path / "dist"
    build(saida, pasta, exigir_fotos=True)
    assert not (saida / "img" / "studio-960.webp").exists()
    assert (saida / "img" / "og.jpg").exists()
    pagina = (saida / "index.html").read_text(encoding="utf-8")
    assert 'src="/img/studio-' not in pagina


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
                        lambda fotos, css_versao, gtm_id=None: "<html><body><p>Um tratamento</p></body></html>")
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


def test_build_copia_o_script_e_gera_as_fotos_do_provador(tmp_path):
    pasta = tmp_path / "fotos"
    _fotos(pasta)
    for nome in ["provador-cilios-marcante", "provador-sobrancelha-lamination"]:
        Image.new("RGB", (1080, 1350), (190, 170, 150)).save(pasta / f"{nome}.jpg")
    saida = tmp_path / "dist"
    build(saida, pasta, exigir_fotos=True)
    assert (saida / "static" / "provador.js").exists()
    assert (saida / "img" / "provador-cilios-marcante-960.webp").exists()
    pagina = (saida / "index.html").read_text(encoding="utf-8")
    assert "/static/provador.js?v=" in pagina
    assert 'data-opcao="micropigmentado"' not in pagina


def test_versao_dos_estaticos_muda_quando_o_script_muda(tmp_path, monkeypatch):
    (tmp_path / "fotos").mkdir()
    build(tmp_path / "a", tmp_path / "fotos", exigir_fotos=False)
    versao_a = re.search(r"provador\.js\?v=(\w+)", (tmp_path / "a" / "index.html").read_text(encoding="utf-8")).group(1)
    estatico = tmp_path / "static"
    shutil.copytree(modulo.RAIZ / "static", estatico)
    (estatico / "provador.js").write_text("/* mudou */", encoding="utf-8")
    monkeypatch.setattr(modulo, "RAIZ", tmp_path)
    build(tmp_path / "b", tmp_path / "fotos", exigir_fotos=False)
    versao_b = re.search(r"provador\.js\?v=(\w+)", (tmp_path / "b" / "index.html").read_text(encoding="utf-8")).group(1)
    assert versao_a != versao_b


def _provador_com(monkeypatch, campo, valor):
    grupos = copy.deepcopy(modulo.data.PROVADOR)
    grupos[0]["opcoes"][1][campo] = valor
    monkeypatch.setattr(modulo.data, "PROVADOR", grupos)


@pytest.mark.parametrize("campo", ["rotulo", "mensagem", "alt"])
def test_build_barra_texto_proibido_no_provador(tmp_path, monkeypatch, campo):
    _provador_com(monkeypatch, campo, "cílios permanente")
    (tmp_path / "fotos").mkdir()
    with pytest.raises(SystemExit) as erro:
        build(tmp_path / "dist", tmp_path / "fotos", exigir_fotos=False)
    msg = str(erro.value)
    assert "permanente" in msg and "marcante" in msg and campo in msg


def test_build_barra_texto_proibido_na_mensagem_padrao_do_provador(tmp_path, monkeypatch):
    monkeypatch.setattr(modulo.data, "PROVADOR_MENSAGEM_PADRAO", "Oi, quero algo grátis")
    (tmp_path / "fotos").mkdir()
    with pytest.raises(SystemExit) as erro:
        build(tmp_path / "dist", tmp_path / "fotos", exigir_fotos=False)
    assert "grátis" in str(erro.value)


def test_provador_sem_arquivos_proprios_nao_gera_webp_duplicado(tmp_path):
    pasta = tmp_path / "fotos"
    _fotos(pasta)
    saida = tmp_path / "dist"
    build(saida, pasta, exigir_fotos=True)
    assert not list((saida / "img").glob("provador-*"))
    pagina = (saida / "index.html").read_text(encoding="utf-8")
    assert "/img/cilios-efeito-960.webp" in pagina
    assert "/img/provador-" not in pagina


FOTOS_REAIS = modulo.RAIZ / "fotos"


@pytest.mark.skipif(faltando(FOTOS_REAIS), reason="fotos reais não estão em fotos/")
def test_webp_usados_pelo_provador_pesam_no_maximo_120_kb(tmp_path):
    saida = tmp_path / "dist"
    build(saida, FOTOS_REAIS, exigir_fotos=True)
    pagina = (saida / "index.html").read_text(encoding="utf-8")
    dados = json.loads(re.search(r'id="provador-dados">(.*?)</script>', pagina, re.S).group(1))
    usados = {f.name for f in (saida / "img").glob("provador-*.webp")}
    for g in dados["grupos"]:
        for o in g["opcoes"]:
            if o["foto"]:
                usados |= set(re.findall(r"/img/([\w-]+\.webp)", o["foto"]["srcset"] + o["foto"]["mini"]))
    assert usados
    for nome in usados:
        assert (saida / "img" / nome).stat().st_size <= 120 * 1024, nome


def test_academy_recebe_as_fotos_otimizadas(tmp_path):
    pasta = tmp_path / "fotos"
    _fotos(pasta)
    for nome in ["micropigmentacao-antes", "micropigmentacao-depois"]:
        Image.new("RGB", (1080, 1350), (190, 170, 150)).save(pasta / f"{nome}.jpg")
    saida = tmp_path / "dist"
    build(saida, pasta, exigir_fotos=True)
    academy = (saida / "academy" / "index.html").read_text(encoding="utf-8")
    for nome in ["laryssa", "studio", "sobrancelha-design",
                 "micropigmentacao-antes", "micropigmentacao-depois"]:
        assert f"/img/{nome}-960.webp" in academy, nome


def test_academy_sem_a_foto_do_studio_continua_de_pe(tmp_path):
    pasta = tmp_path / "fotos"
    _fotos(pasta)
    (pasta / "studio.jpg").unlink()
    saida = tmp_path / "dist"
    build(saida, pasta, exigir_fotos=True)
    academy = (saida / "academy" / "index.html").read_text(encoding="utf-8")
    assert 'src="/img/studio-' not in academy
    assert 'id="onde-e"' in academy


def test_academy_da_previa_sem_fotos_nao_cita_nenhum_webp(tmp_path):
    (tmp_path / "fotos").mkdir()
    build(tmp_path / "dist", tmp_path / "fotos", exigir_fotos=False)
    academy = (tmp_path / "dist" / "academy" / "index.html").read_text(encoding="utf-8")
    assert ".webp" not in academy
