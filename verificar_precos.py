"""Confere se os serviços que o site lista existem no Maapp e estão liberados para agendamento online.

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


def _servicos_do_site():
    nomes = {item["nome"] for cat in SERVICOS for item in cat["itens"]}
    nomes.update(c["nome"] for c in COMBOS)
    nomes.add(PRIMEIRO_OLHAR["nome"])
    return nomes


def comparar(servicos_maapp):
    site = _servicos_do_site()
    por_nome = {s["name"].strip(): s for s in servicos_maapp}
    erros = []
    for nome_maapp, nome_site in MAAPP_PARA_SITE.items():
        if nome_site not in site:
            continue
        servico = por_nome.get(nome_maapp)
        if servico is None:
            erros.append(f"{nome_site}: não existe mais no Maapp")
            continue
        if not servico.get("onlineSchedulingEnabled"):
            erros.append(f"{nome_site}: está oculto no agendamento online, mas o site manda a cliente para lá")
    return erros


if __name__ == "__main__":
    erros = comparar(json.load(open(sys.argv[1], encoding="utf-8")))
    print("\n".join(erros) if erros else "os serviços do site existem e estão liberados no Maapp")
    sys.exit(1 if erros else 0)
