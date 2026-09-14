"""Confere se os preços do site batem com o Maapp e se as ofertas estão visíveis no agendamento.

Uso: python verificar_precos.py maapp_services.json
"""
import json
import sys
from data import SERVICOS, COMBOS, PRIMEIRO_OLHAR

MAAPP_PARA_SITE = {
    "Volume Brasileiro / Egípcio": "Volume Brasileiro ou Egípcio",
    "Mega Volumes (5D/ Egípcio/ Brasileiro)": "Mega Volumes",
    "Efeito Sirena / Fox/ Molhado /Kim Kardashian": "Efeitos (Sirena, Fox, Molhado, Kardashian)",
    "Manutenção de cílios (até 21 dias)": "Manutenção (até 21 dias)",
    "Lash lifting": "Lash lifting",
    "Remoção cílios (30,00 vindo de outra profissional)": "Remoção",
    "Design Personalizado": "Design personalizado",
    "Design com Henna": "Design com henna",
    "Design Masculino": "Design masculino",
    "Brown Lamination": "Brow Lamination",
    "Reconstrução de sobrancelhas": "Reconstrução de sobrancelhas",
    "Micropigmentação ou Microblading": "Micropigmentação ou microblading",
    "Epilação buço": "Epilação de buço",
    "Hidragloss": "Hidragloss",
    "Micropigmentação nos lábios": "Micropigmentação labial",
    "Combo Olhar Completo": "Olhar Completo",
    "Combo Realeza": "Realeza",
    "Combo Manutenção Glow": "Manutenção Glow",
    "Primeiro Olhar": "Primeiro Olhar",
}


def _precos_do_site():
    precos = {item["nome"]: item["preco"] for cat in SERVICOS for item in cat["itens"]}
    precos.update({c["nome"]: c["preco"] for c in COMBOS})
    precos[PRIMEIRO_OLHAR["nome"]] = PRIMEIRO_OLHAR["preco"]
    return precos


def comparar(servicos_maapp):
    site = _precos_do_site()
    por_nome = {s["name"].strip(): s for s in servicos_maapp}
    erros = []
    for nome_maapp, nome_site in MAAPP_PARA_SITE.items():
        servico = por_nome.get(nome_maapp)
        if servico is None:
            erros.append(f"{nome_site}: não existe mais no Maapp")
            continue
        valor = int(round(float(servico["price"])))
        if valor != site[nome_site]:
            erros.append(f"{nome_site}: Maapp R${valor}, site R${site[nome_site]}")
        if not servico.get("onlineSchedulingEnabled"):
            erros.append(f"{nome_site}: está oculto no agendamento online, mas o site manda a cliente para lá")
    return erros


if __name__ == "__main__":
    erros = comparar(json.load(open(sys.argv[1], encoding="utf-8")))
    print("\n".join(erros) if erros else "preços do site batem com o Maapp")
    sys.exit(1 if erros else 0)
