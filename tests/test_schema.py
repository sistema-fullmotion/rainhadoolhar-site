import json
from schema import beauty_salon, curso, jsonld_script
from data import CURSOS

PREFIXO = '<script type="application/ld+json">'


def test_beauty_salon_com_nap_exato_e_sem_estrelas():
    s = beauty_salon()
    assert s["@type"] == "BeautySalon"
    assert s["address"]["streetAddress"] == "Rua Estrela, 74"
    assert s["address"]["postalCode"] == "20251-021"
    assert s["telephone"] == "+5521967748281"
    assert (s["geo"]["latitude"], s["geo"]["longitude"]) == (-22.924813, -43.208188)
    assert s["sameAs"] == ["https://www.instagram.com/rainhadoolhar_/"]
    texto = json.dumps(s)
    assert "aggregateRating" not in texto and '"review"' not in texto


def test_beauty_salon_sem_price_range():
    s = beauty_salon()
    assert "priceRange" not in s


def test_horario_no_formato_do_google():
    horarios = beauty_salon()["openingHoursSpecification"]
    assert horarios[0]["dayOfWeek"][0] == "Monday" and horarios[0]["closes"] == "22:00"
    assert horarios[1]["dayOfWeek"] == ["Saturday"] and horarios[1]["closes"] == "17:00"


def test_curso_sem_preco_nas_offers():
    c = curso(CURSOS[0])
    assert c["@type"] == "Course"
    assert c["offers"]["@type"] == "Offer"
    assert c["offers"]["category"] == "Paid"
    assert "price" not in c["offers"]
    assert "priceCurrency" not in c["offers"]
    assert c["hasCourseInstance"]["courseMode"] == "Onsite"
    texto = json.dumps(c)
    assert "R$" not in texto


def test_jsonld_script_nao_quebra_a_tag():
    html = jsonld_script({"x": "</script><b>"})
    assert html.startswith(PREFIXO) and html.endswith("</script>")
    assert html.count("</script>") == 1
    assert json.loads(html[len(PREFIXO):-len("</script>")])["x"] == "</script><b>"
