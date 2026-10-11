"""Regras de CSS e do script do provador que não dependem de node."""
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
CSS = (RAIZ / "static" / "style.css").read_text(encoding="utf-8")
JS = (RAIZ / "static" / "provador.js").read_text(encoding="utf-8")


def regra(seletor):
    achou = re.search(re.escape(seletor) + r"\s*\{([^}]*)\}", CSS)
    assert achou, seletor
    return achou.group(1)


def test_css_tem_estado_marcado_e_botao_do_whatsapp():
    assert '.provador-opcao[aria-pressed="true"]' in CSS
    assert ".btn-whatsapp{" in CSS
    assert "body.provador-visivel .barra-agendar" in CSS
    assert ".hero.tem-foto" not in CSS


def test_opcao_nao_marcada_tem_borda_dourada_visivel():
    assert "border:1px solid var(--dourado)" in regra(".provador-opcao")
    assert "border-color:var(--dourado-texto)" in regra('.provador-opcao[aria-pressed="true"]')


def test_foto_do_provador_limita_a_altura_no_celular():
    assert re.search(r"@media \(max-width:719px\)\{[^@]*\.provador-foto\{max-height:42vh\}"
                     r"[^@]*\.provador-foto img\{height:100%\}", CSS)


def test_barra_escondida_tambem_sai_da_ordem_de_foco():
    escondida = regra("body.provador-visivel .barra-agendar")
    assert "visibility:hidden" in escondida
    # o atraso fica só na ida: a barra sai da ordem de foco depois de deslizar, e volta a aparecer já deslizando
    assert "transition:transform .25s ease, visibility 0s .25s" in escondida
    assert "transition:transform .25s ease, visibility 0s}" in CSS


def test_link_da_agenda_tem_area_de_toque():
    assert "padding:11px 4px" in regra(".provador-agenda a")
    assert "display:inline-block" in regra(".provador-agenda a")


def test_script_protege_os_ganchos_e_o_json():
    assert "try {" in JS and "JSON.parse(fonte.textContent)" in JS
    assert "!resumo || !zap || !miniaturas" in JS


def test_precarrega_com_prioridade_baixa_e_pula_a_foto_exibida():
    assert 'img.fetchPriority = "low"' in JS
    assert 'foto.getAttribute("src")' in JS


def test_tema_escuro_da_academy_e_escopado_no_body():
    assert "body.academy{" in CSS
    for seletor in ["body.academy .ac-hero{", "body.academy .ac-curso{", "body.academy .barra-agendar{"]:
        assert seletor in CSS, seletor
    # nada do tema escuro pode vazar para o studio
    for bloco in re.findall(r"(?m)^[^@{]*\{[^}]*\}", CSS):
        if "--ac-" in bloco.split("{")[1] and "body.academy" not in bloco.split("{")[0]:
            assert False, bloco.split("{")[0]


def test_css_nao_guarda_o_hero_antigo_que_ninguem_usa():
    assert ".hero{" not in CSS
    assert ".hero p{" not in CSS
    assert ".hero-logo{" in CSS


def test_academy_respeita_reducao_de_movimento():
    assert ".ac-foto img,body.academy .btn{transition:none}" in CSS
