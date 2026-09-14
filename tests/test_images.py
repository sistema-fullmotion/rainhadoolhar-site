from pathlib import Path
from PIL import Image
from images import otimizar, gerar_og, faltando, FOTOS_OBRIGATORIAS
from data import ALT_FOTOS


def _cria(pasta: Path, nome: str, tamanho=(1080, 1350)):
    Image.new("RGB", tamanho, (200, 180, 160)).save(pasta / f"{nome}.jpg", quality=90)


def test_lista_de_fotos_bate_com_os_textos_alternativos():
    assert sorted(FOTOS_OBRIGATORIAS) == sorted(ALT_FOTOS)


def test_faltando_lista_as_ausentes(tmp_path):
    _cria(tmp_path, "studio")
    ausentes = faltando(tmp_path)
    assert "studio" not in ausentes and "laryssa" in ausentes
    assert len(ausentes) == len(FOTOS_OBRIGATORIAS) - 1


def test_otimizar_gera_webp_nas_duas_larguras(tmp_path):
    origem, destino = tmp_path / "o", tmp_path / "d"
    origem.mkdir()
    _cria(origem, "studio")
    info = otimizar(origem, destino)
    assert info["studio"] == {"larguras": [480, 960], "w": 960, "h": 1200}
    assert Image.open(destino / "studio-960.webp").size == (960, 1200)
    assert Image.open(destino / "studio-480.webp").size == (480, 600)


def test_foto_pequena_nao_e_ampliada(tmp_path):
    origem, destino = tmp_path / "o", tmp_path / "d"
    origem.mkdir()
    _cria(origem, "laryssa", (600, 750))
    assert otimizar(origem, destino)["laryssa"] == {"larguras": [480, 600], "w": 600, "h": 750}


def test_og_tem_1200_por_630(tmp_path):
    _cria(tmp_path, "studio")
    gerar_og(tmp_path / "studio.jpg", tmp_path / "og.jpg")
    assert Image.open(tmp_path / "og.jpg").size == (1200, 630)
