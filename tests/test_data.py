from data import (NEGOCIO, SERVICOS, PRIMEIRO_OLHAR, COMBOS, PACOTES, CURSOS, FAQ,
                  AVALIACOES_STUDIO, ALT_FOTOS, preco)


def test_nap_igual_ao_google():
    assert NEGOCIO["endereco_completo"] == "Rua Estrela, 74 - Rio Comprido, Rio de Janeiro - RJ, 20251-021"
    assert NEGOCIO["telefone_exibicao"] == "(21) 96774-8281"
    assert NEGOCIO["instagram_usuario"] == "rainhadoolhar_"
    assert (NEGOCIO["nota_google"], NEGOCIO["avaliacoes_google"]) == ("5,0", 43)
    assert (NEGOCIO["lat"], NEGOCIO["lng"]) == (-22.924813, -43.208188)


def test_primeiro_olhar_soma_aplicacao_e_manutencao():
    assert PRIMEIRO_OLHAR["de"] == preco("Volume Brasileiro ou Egípcio") + preco("Manutenção (até 21 dias)")


def test_combos_valor_de_bate_com_avulsos():
    esperado = {
        "Olhar Completo": preco("Volume Brasileiro ou Egípcio") + preco("Design personalizado"),
        "Realeza": preco("Efeitos (Sirena, Fox, Molhado, Kardashian)") + preco("Design personalizado") + preco("Hidragloss"),
        "Manutenção Glow": preco("Manutenção (até 21 dias)") + preco("Hidragloss"),
    }
    assert {c["nome"]: c["de"] for c in COMBOS} == esperado


def test_pacotes_valor_de_bate_com_avulsos():
    esperado = {
        "Brow Perfeita": 3 * preco("Brow Lamination") + 2 * preco("Design com henna"),
        "Reconstrução": 6 * preco("Reconstrução de sobrancelhas"),
        "Plano de manutenção": 2 * preco("Manutenção (até 21 dias)"),
    }
    assert {p["nome"]: p["de"] for p in PACOTES} == esperado


def test_desconto_de_conjunto_no_maximo_5_por_cento():
    for oferta in [PRIMEIRO_OLHAR, *COMBOS, *PACOTES]:
        assert oferta["preco"] >= oferta["de"] * 0.95, oferta["nome"]


def test_fora_do_site_microderme_express_e_cortesia():
    nomes = [it["nome"].lower() for cat in SERVICOS for it in cat["itens"]]
    assert not any("microderme" in n or "express" in n for n in nomes)
    assert "130" not in str([SERVICOS, PRIMEIRO_OLHAR, COMBOS, PACOTES, FAQ])


def test_cinco_cursos_com_os_precos_da_academy():
    assert [c["preco"] for c in CURSOS] == [1497, 2297, 797, 997, 1597]


def test_avaliacoes_e_fotos_prontas():
    assert len(AVALIACOES_STUDIO) == 4
    assert len(ALT_FOTOS) == 12


def test_volume_brasileiro_ou_egipcio_cita_o_efeito_u():
    texto = next(it["texto"] for cat in SERVICOS for it in cat["itens"]
                 if it["nome"] == "Volume Brasileiro ou Egípcio")
    assert "efeito U" in texto
