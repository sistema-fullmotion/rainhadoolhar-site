"""Pedaços de HTML das duas páginas e a regra de texto da marca."""
import html
from urllib.parse import quote

PROIBIDAS = ["—", "tratamento", "paciente", "clínica", "clinica", "zero risco", "não cai",
             "dura para sempre", "dura pra sempre", "permanente", "grátis", "gratis"]


def esc(texto):
    return html.escape(str(texto), quote=True)


def verificar_texto(texto):
    baixo = texto.lower()
    return [termo for termo in PROIBIDAS if termo in baixo]


def link_whatsapp(numero_e164, texto):
    """Link do WhatsApp com a mensagem já escrita (wa.me com ?text=)."""
    return f"https://wa.me/{numero_e164.lstrip('+')}?text={quote(texto)}"


def cta(href, texto, rastreio, variante="primario"):
    return (f'<a class="btn btn-{variante}" href="{esc(href)}" target="_blank" rel="noopener" '
            f'data-cta="{esc(rastreio)}">{esc(texto)}</a>')


def caminhos_imagem(nome, info):
    """src (maior largura), srcset e a maior largura de uma foto otimizada."""
    larguras = info["larguras"]
    srcset = ", ".join(f"/img/{nome}-{largura}.webp {largura}w" for largura in larguras)
    return f"/img/{nome}-{larguras[-1]}.webp", srcset, larguras[-1]


def imagem(nome, info, alt, sizes="(min-width: 720px) 25vw, 50vw", carregar="lazy", prioridade=False, extra=""):
    src, srcset, _ = caminhos_imagem(nome, info)
    prio = ' fetchpriority="high"' if prioridade else ""
    adicional = f" {extra}" if extra else ""
    return (f'<img src="{src}" srcset="{srcset}" sizes="{esc(sizes)}" '
            f'width="{info["w"]}" height="{info["h"]}" alt="{esc(alt)}" loading="{carregar}" decoding="async"{prio}{adicional}>')


def ornamento():
    return '<img class="ornamento" src="/static/ornamento.svg" alt="" width="190" height="26">'
