"""Transforma as fotos originais de fotos/ em WebP leves para o site."""
from pathlib import Path
from PIL import Image, ImageOps

FOTOS_OBRIGATORIAS = ["cilios-classico", "cilios-mega", "cilios-efeito", "sobrancelha-design",
                      "sobrancelha-henna", "sobrancelha-lamination",
                      "labios-hidragloss", "laryssa"]
# Fotos que aparecem quando existem em fotos/, mas não travam o build se ainda não chegaram.
# "studio" fica opcional porque a foto do espaço não é mais exibida na página (só serve de
# reserva para a imagem de og.jpg quando presente).
FOTOS_OPCIONAIS = ["sobrancelha-reconstrucao", "micropigmentacao-antes", "micropigmentacao-depois",
                   "studio", "hero"]
TODAS_FOTOS = FOTOS_OBRIGATORIAS + FOTOS_OPCIONAIS
LARGURAS = (480, 960)
EXTENSOES = (".jpg", ".jpeg", ".png", ".webp")


def _achar(pasta: Path, nome: str):
    for ext in EXTENSOES:
        arquivo = pasta / f"{nome}{ext}"
        if arquivo.exists():
            return arquivo
    return None


def faltando(pasta: Path):
    return [nome for nome in FOTOS_OBRIGATORIAS if _achar(pasta, nome) is None]


def _abrir(arquivo: Path):
    return ImageOps.exif_transpose(Image.open(arquivo)).convert("RGB")


def otimizar(origem: Path, destino: Path) -> dict:
    destino.mkdir(parents=True, exist_ok=True)
    info = {}
    for nome in TODAS_FOTOS:
        arquivo = _achar(origem, nome)
        if arquivo is None:
            continue
        img = _abrir(arquivo)
        larguras = sorted({min(largura, img.width) for largura in LARGURAS})
        for largura in larguras:
            altura = round(img.height * largura / img.width)
            img.resize((largura, altura), Image.Resampling.LANCZOS).save(
                destino / f"{nome}-{largura}.webp", "WEBP", quality=80, method=6)
        maior = larguras[-1]
        info[nome] = {"larguras": larguras, "w": maior, "h": round(img.height * maior / img.width)}
    return info


def gerar_og(foto: Path, saida: Path) -> None:
    saida.parent.mkdir(parents=True, exist_ok=True)
    ImageOps.fit(_abrir(foto), (1200, 630), Image.Resampling.LANCZOS).save(saida, "JPEG", quality=85)
