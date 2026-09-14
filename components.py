"""Pedaços de HTML das duas páginas e a regra de texto da marca."""
import html

PROIBIDAS = ["—", "tratamento", "paciente", "clínica", "clinica", "zero risco", "não cai",
             "dura para sempre", "dura pra sempre", "permanente", "grátis", "gratis"]


def esc(texto):
    return html.escape(str(texto), quote=True)


def verificar_texto(texto):
    baixo = texto.lower()
    return [termo for termo in PROIBIDAS if termo in baixo]


def cta(href, texto, rastreio, variante="primario"):
    return (f'<a class="btn btn-{variante}" href="{esc(href)}" target="_blank" rel="noopener" '
            f'data-cta="{esc(rastreio)}">{esc(texto)}</a>')


def imagem(nome, info, alt, sizes="(min-width: 720px) 25vw, 50vw", carregar="lazy", prioridade=False):
    srcset = ", ".join(f"/img/{nome}-{largura}.webp {largura}w" for largura in info["larguras"])
    maior = info["larguras"][-1]
    extra = ' fetchpriority="high"' if prioridade else ""
    return (f'<img src="/img/{nome}-{maior}.webp" srcset="{srcset}" sizes="{esc(sizes)}" '
            f'width="{info["w"]}" height="{info["h"]}" alt="{esc(alt)}" loading="{carregar}" decoding="async"{extra}>')


def ornamento():
    return '<img class="ornamento" src="/static/ornamento.svg" alt="" width="190" height="26">'
