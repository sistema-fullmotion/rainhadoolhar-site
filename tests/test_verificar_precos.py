from verificar_precos import comparar

BASE = [
    ("Volume Brasileiro / Egípcio", 180), ("Mega Volumes (5D/ Egípcio/ Brasileiro)", 180),
    ("Efeito Sirena / Fox/ Molhado /Kim Kardashian", 200), ("Manutenção de cílios (até 21 dias)", 150),
    ("Lash lifting", 120), ("Remoção cílios (30,00 vindo de outra profissional)", 15),
    ("Design Personalizado", 50), ("Design com Henna", 65), ("Design Masculino", 50),
    ("Brown Lamination", 95), ("Reconstrução de sobrancelhas", 65), ("Micropigmentação ou Microblading", 600),
    ("Epilação buço", 15), ("Hidragloss", 60), ("Micropigmentação nos lábios", 400),
    ("Combo Olhar Completo", 220), ("Combo Realeza", 295), ("Combo Manutenção Glow", 200), ("Primeiro Olhar", 315),
]


def maapp(**trocas):
    lista = [{"name": nome, "price": valor, "onlineSchedulingEnabled": True} for nome, valor in BASE]
    for item in lista:
        item.update(trocas.get(item["name"], {}))
    return lista


def test_tudo_igual_nao_acusa_nada():
    assert comparar(maapp()) == []


def test_preco_diferente_e_acusado():
    assert comparar(maapp(**{"Hidragloss": {"price": 70}})) == ["Hidragloss: Maapp R$70, site R$60"]


def test_oferta_oculta_no_agendamento_e_acusada():
    erros = comparar(maapp(**{"Primeiro Olhar": {"onlineSchedulingEnabled": False}}))
    assert erros == ["Primeiro Olhar: está oculto no agendamento online, mas o site manda a cliente para lá"]


def test_servico_sumido_do_maapp_e_acusado():
    lista = [s for s in maapp() if s["name"] != "Lash lifting"]
    assert comparar(lista) == ["Lash lifting: não existe mais no Maapp"]
