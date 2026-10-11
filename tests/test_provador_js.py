import json
import shutil
import subprocess
from pathlib import Path

import pytest

JS = Path(__file__).resolve().parents[1] / "static" / "provador.js"
pytestmark = pytest.mark.skipif(shutil.which("node") is None, reason="node não instalado")

EXECUTOR = (
    "const p = require(process.argv[1]); let entrada = '';"
    "process.stdin.setEncoding('utf8');"
    "process.stdin.on('data', c => entrada += c).on('end', () => {"
    "  const a = JSON.parse(entrada);"
    "  process.stdout.write(JSON.stringify(p[a.funcao](...a.argumentos)));"
    "});"
)


def chamar(funcao, *argumentos):
    saida = subprocess.run(["node", "-e", EXECUTOR, str(JS)], input=json.dumps({"funcao": funcao, "argumentos": argumentos}),
                           capture_output=True, text=True, encoding="utf-8", check=True)
    return json.loads(saida.stdout)


def test_mensagem_junta_as_escolhas_e_pula_labios_natural():
    escolhas = [{"mensagem": "cílios marcante (efeito)"}, {"mensagem": "sobrancelha com brow lamination"},
                {"mensagem": ""}]
    assert chamar("montarMensagem", escolhas) == (
        "Oi, Laryssa! Montei meu olhar no site: cílios marcante (efeito), "
        "sobrancelha com brow lamination. Quero agendar!")


def test_mensagem_com_labios_hidratados():
    escolhas = [{"mensagem": "cílios natural (volume brasileiro)"}, {"mensagem": "sobrancelha com henna"},
                {"mensagem": "lábios hidratados (hidragloss)"}]
    assert chamar("montarMensagem", escolhas) == (
        "Oi, Laryssa! Montei meu olhar no site: cílios natural (volume brasileiro), "
        "sobrancelha com henna, lábios hidratados (hidragloss). Quero agendar!")


def test_link_whatsapp_codifica_o_texto():
    assert chamar("linkWhatsapp", "5521967748281", "Oi, Laryssa! Quero agendar.") == (
        "https://wa.me/5521967748281?text=Oi%2C%20Laryssa!%20Quero%20agendar.")
