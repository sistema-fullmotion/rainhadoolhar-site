"""Cabeçalho HTML comum às duas páginas."""
from components import esc
from data import NEGOCIO

FONTES = ("https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;1,400"
          "&family=Jost:wght@400;500;600&display=swap")


def _gtm(gtm_id):
    head = ("<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':new Date().getTime(),"
            "event:'gtm.js'});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?"
            "'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;"
            f"f.parentNode.insertBefore(j,f);}})(window,document,'script','dataLayer','{gtm_id}');</script>\n")
    body = (f'<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={gtm_id}" height="0" '
            'width="0" style="display:none;visibility:hidden"></iframe></noscript>\n')
    return head, body


def render_head(titulo, descricao, caminho, jsonlds, css_versao, gtm_id=None):
    url = NEGOCIO["site_url"] + caminho
    gtm_head, gtm_body = _gtm(gtm_id) if gtm_id else ("", "")
    return (
        '<!DOCTYPE html>\n<html lang="pt-BR">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f"<title>{esc(titulo)}</title>\n"
        f'<meta name="description" content="{esc(descricao)}">\n'
        f'<link rel="canonical" href="{esc(url)}">\n'
        f'<meta property="og:title" content="{esc(titulo)}">\n'
        f'<meta property="og:description" content="{esc(descricao)}">\n'
        f'<meta property="og:url" content="{esc(url)}">\n'
        '<meta property="og:type" content="website">\n'
        f'<meta property="og:image" content="{NEGOCIO["site_url"]}/img/og.jpg">\n'
        '<meta name="theme-color" content="#F6F1E7">\n'
        '<link rel="icon" type="image/png" href="/static/logo-monograma.png">\n'
        '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
        f'<link rel="stylesheet" href="{esc(FONTES)}">\n'
        f'<link rel="stylesheet" href="/static/style.css?v={esc(css_versao)}">\n'
        + "\n".join(jsonlds) + "\n" + gtm_head
        + "</head>\n<body>\n" + gtm_body
    )
