import json
import re
from urllib.parse import unquote

import build as modulo
from components import verificar_texto
from data import FOTOS_PROVADOR, NEGOCIO
from provador import render_provador, link_whatsapp

INFO = {"larguras": [480, 960], "w": 960, "h": 1200}
FOTOS = {nome: dict(INFO) for nome in FOTOS_PROVADOR if nome != "provador-labios-micropigmentado"}
ZAP = NEGOCIO["telefone_e164"]
AGENDA = NEGOCIO["maapp_url"]


def html(fotos=FOTOS):
    return render_provador(fotos, ZAP, AGENDA)


def dados(pagina):
    bruto = re.search(r'<script type="application/json" id="provador-dados">(.*?)</script>', pagina, re.S)
    return json.loads(bruto.group(1))


def test_link_whatsapp_usa_numero_e_texto_codificado():
    assert (link_whatsapp("+5521967748281", "Oi, Laryssa! Quero agendar.")
            == "https://wa.me/5521967748281?text=Oi%2C%20Laryssa%21%20Quero%20agendar.")


def test_topo_mantem_h1_e_id_inicio():
    h = html()
    assert '<section id="inicio" class="provador">' in h
    assert "<h1>Um olhar pra cada mulher. <em>Escolha o seu.</em></h1>" in h


def test_tres_grupos_com_as_opcoes_na_ordem():
    h = html()
    assert re.findall(r'role="group" aria-label="([^"]+)"', h) == ["Cílios", "Sobrancelha", "Lábios"]
    assert re.findall(r'data-grupo="([a-z]+)" data-opcao="([a-z]+)"', h) == [
        ("cilios", "natural"), ("cilios", "marcante"), ("cilios", "dramatico"),
        ("sobrancelha", "design"), ("sobrancelha", "henna"), ("sobrancelha", "lamination"),
        ("labios", "natural"), ("labios", "hidratado")]


def test_micropigmentado_so_aparece_quando_existe_a_foto():
    assert 'data-opcao="micropigmentado"' not in html()
    com_foto = dict(FOTOS, **{"provador-labios-micropigmentado": dict(INFO)})
    h = html(com_foto)
    assert 'data-opcao="micropigmentado"' in h
    labios = [g for g in dados(h)["grupos"] if g["grupo"] == "labios"][0]
    assert [o["id"] for o in labios["opcoes"]] == ["natural", "hidratado", "micropigmentado"]


def test_um_botao_marcado_por_grupo_na_escolha_inicial():
    h = html()
    marcados = re.findall(r'data-grupo="([a-z]+)" data-opcao="([a-z]+)" aria-pressed="true"', h)
    assert marcados == [("cilios", "marcante"), ("sobrancelha", "lamination"), ("labios", "natural")]
    assert h.count('aria-pressed="true"') == 3


def test_foto_inicial_e_marcante_com_prioridade_e_resumo():
    h = html()
    img = re.search(r"<img data-provador-foto [^>]+>", h).group(0)
    assert "/img/provador-cilios-marcante-960.webp" in img
    assert 'loading="eager"' in img and 'fetchpriority="high"' in img
    assert 'data-provador-resumo aria-live="polite">Marcante · Lamination · Natural</b>' in h


def test_whatsapp_inicial_tem_mensagem_padrao_e_numero_oficial():
    h = html()
    href = re.search(r'<a class="btn btn-whatsapp" href="([^"]+)"', h).group(1)
    assert href.startswith("https://wa.me/5521967748281?text=")
    assert unquote(href.split("text=", 1)[1]) == "Oi, Laryssa! Vim pelo site e quero agendar."
    assert 'data-cta="provador-whatsapp"' in h and "data-provador-whatsapp" in h


def test_link_da_agenda_vai_para_o_maapp():
    assert (f'<a href="{AGENDA}" target="_blank" rel="noopener" data-cta="provador-agenda">'
            "Prefiro escolher o horário na agenda</a>") in html()


def test_json_embutido_bate_com_os_dados():
    d = dados(html())
    assert d["whatsapp"] == "5521967748281"
    assert [g["grupo"] for g in d["grupos"]] == ["cilios", "sobrancelha", "labios"]
    marcante = d["grupos"][0]["opcoes"][1]
    assert marcante["id"] == "marcante" and marcante["mensagem"] == "cílios marcante (efeito)"
    assert marcante["foto"]["src"] == "/img/provador-cilios-marcante-960.webp"
    assert marcante["foto"]["mini"] == "/img/provador-cilios-marcante-480.webp"
    assert marcante["foto"]["srcset"] == ("/img/provador-cilios-marcante-480.webp 480w, "
                                          "/img/provador-cilios-marcante-960.webp 960w")
    natural_labios = d["grupos"][2]["opcoes"][0]
    assert natural_labios["foto"] is None and natural_labios["mensagem"] == ""


def test_json_nao_fecha_a_tag_script_antes_da_hora():
    bruto = re.search(r'id="provador-dados">(.*?)</script>', html(), re.S).group(1)
    assert "</" not in bruto


def test_miniaturas_iniciais_de_cilios_e_sobrancelha():
    h = html()
    minis = re.search(r'<div class="provador-miniaturas" data-provador-miniaturas>(.*?)</div>', h).group(1)
    assert re.findall(r'src="([^"]+)"', minis) == ["/img/provador-cilios-marcante-480.webp",
                                                  "/img/provador-sobrancelha-lamination-480.webp"]


def test_sem_fotos_o_topo_continua_de_pe():
    h = render_provador({}, ZAP, AGENDA)
    assert 'src="/img/' not in h
    assert 'class="provador-foto sem-foto"' in h
    assert "<h1>Um olhar pra cada mulher. <em>Escolha o seu.</em></h1>" in h


def test_sem_preco_nem_texto_proibido():
    h = html()
    assert "R$" not in h
    assert verificar_texto(modulo._texto_visivel(h)) == []
