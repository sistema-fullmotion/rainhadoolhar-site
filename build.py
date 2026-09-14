"""Gera o site em dist/.

    python build.py              # exige as 10 fotos em fotos/
    python build.py --sem-fotos  # prévia sem galeria, retrato e foto do studio
"""
import hashlib
import html
import re
import shutil
import sys
from pathlib import Path

from components import verificar_texto
from data import NEGOCIO
from images import faltando, otimizar, gerar_og, _achar
from page_academy import render_academy
from page_studio import render_studio

RAIZ = Path(__file__).resolve().parent
GTM_ID = None  # trocar pelo ID do container (formato "GTM-XXXXXXX") quando ele for criado


def _texto_visivel(pagina):
    sem_codigo = re.sub(r"<(script|style)\b.*?</\1>", " ", pagina, flags=re.S | re.I)
    return html.unescape(re.sub(r"<[^>]+>", " ", sem_codigo))


def build(saida: Path, pasta_fotos: Path, exigir_fotos: bool = True) -> None:
    ausentes = faltando(pasta_fotos)
    if exigir_fotos and ausentes:
        raise SystemExit(f"faltam fotos em {pasta_fotos}: {', '.join(ausentes)}")
    if saida.exists():
        shutil.rmtree(saida)
    (saida / "academy").mkdir(parents=True)
    shutil.copytree(RAIZ / "static", saida / "static")
    css_versao = hashlib.sha1((RAIZ / "static" / "style.css").read_bytes()).hexdigest()[:8]

    fotos = {}
    if not ausentes:
        fotos = otimizar(pasta_fotos, saida / "img")
        foto_capa = (_achar(pasta_fotos, "studio") or _achar(pasta_fotos, "hero")
                    or _achar(pasta_fotos, "laryssa"))
        if foto_capa:
            gerar_og(foto_capa, saida / "img" / "og.jpg")

    paginas = {
        saida / "index.html": render_studio(fotos, css_versao=css_versao, gtm_id=GTM_ID),
        saida / "academy" / "index.html": render_academy(css_versao=css_versao, gtm_id=GTM_ID),
    }
    for caminho, conteudo in paginas.items():
        proibidos = verificar_texto(_texto_visivel(conteudo))
        if proibidos:
            raise SystemExit(f"texto proibido em {caminho.relative_to(saida)}: {', '.join(proibidos)}")
        caminho.write_text(conteudo, encoding="utf-8")

    base = NEGOCIO["site_url"]
    (saida / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {base}/sitemap.xml\n", encoding="utf-8")
    (saida / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"<url><loc>{base}/</loc></url>\n<url><loc>{base}/academy/</loc></url>\n</urlset>\n",
        encoding="utf-8")
    print(f"site gerado em {saida} com {len(fotos)} fotos")


if __name__ == "__main__":
    build(RAIZ / "dist", RAIZ / "fotos", exigir_fotos="--sem-fotos" not in sys.argv)
