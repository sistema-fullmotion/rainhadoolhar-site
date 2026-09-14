"""Dados estruturados que o Google lê. Avaliações ficam só como texto na página."""
import json
from data import NEGOCIO, HORARIO


def _endereco():
    n = NEGOCIO
    return {"@type": "PostalAddress", "streetAddress": n["rua"], "addressLocality": n["cidade"],
            "addressRegion": n["uf"], "postalCode": n["cep"], "addressCountry": "BR"}


def beauty_salon():
    n = NEGOCIO
    return {
        "@context": "https://schema.org",
        "@type": "BeautySalon",
        "name": n["nome"],
        "url": n["site_url"] + "/",
        "image": n["site_url"] + "/img/og.jpg",
        "telephone": n["telefone_e164"],
        "priceRange": "R$15 a R$600",
        "address": _endereco(),
        "geo": {"@type": "GeoCoordinates", "latitude": n["lat"], "longitude": n["lng"]},
        "openingHoursSpecification": [
            {"@type": "OpeningHoursSpecification", "dayOfWeek": dias, "opens": abre, "closes": fecha}
            for _, abre, fecha, dias in HORARIO
        ],
        "sameAs": [n["instagram_url"]],
    }


def curso(c):
    return {
        "@context": "https://schema.org",
        "@type": "Course",
        "name": c["nome"],
        "description": c["resumo"],
        "provider": {"@type": "Organization", "name": "Rainha do Olhar Academy",
                     "sameAs": NEGOCIO["site_url"] + "/academy/"},
        "offers": {"@type": "Offer", "category": "Paid", "priceCurrency": "BRL", "price": f"{c['preco']:.2f}"},
        "hasCourseInstance": {"@type": "CourseInstance", "courseMode": "Onsite",
                              "location": {"@type": "Place", "name": NEGOCIO["nome"], "address": _endereco()}},
    }


def jsonld_script(obj):
    texto = json.dumps(obj, ensure_ascii=False, indent=2).replace("</", "<\\/")
    return f'<script type="application/ld+json">{texto}</script>'
