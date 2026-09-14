"""Fonte única dos fatos e preços usados pelo site.

Conferido em 13/09/2026: preços e durações no Maapp (GET /services), endereço,
telefone, horário, nota e Plus Code no Google Maps, Instagram no próprio perfil.
Mudou preço? Muda aqui, roda os testes e publica.
"""

NEGOCIO = {
    "nome": "Rainha do Olhar",
    "assinatura": "Studio & Academy",
    "rua": "Rua Estrela, 74",
    "bairro": "Rio Comprido",
    "cidade": "Rio de Janeiro",
    "uf": "RJ",
    "cep": "20251-021",
    "endereco_completo": "Rua Estrela, 74 - Rio Comprido, Rio de Janeiro - RJ, 20251-021",
    "telefone_exibicao": "(21) 96774-8281",
    "telefone_e164": "+5521967748281",
    "lat": -22.924813,
    "lng": -43.208188,
    "instagram_usuario": "rainhadoolhar_",
    "instagram_url": "https://www.instagram.com/rainhadoolhar_/",
    "maapp_url": "https://online.maapp.com.br/Rainhadoolhar",
    "whatsapp_url": "https://wa.me/message/PJV7QRCWLYD2E1",
    "maps_url": "https://www.google.com/maps/search/?api=1&query=Rainha+do+Olhar+Rua+Estrela+74+Rio+Comprido",
    "site_url": "https://rainhadoolhar.com.br",
    "nota_google": "5,0",
    "avaliacoes_google": 43,
}

HORARIO = [
    ("Segunda a sexta", "08:00", "22:00", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]),
    ("Sábado", "08:00", "17:00", ["Saturday"]),
]
HORARIO_FECHADO = "Domingo fechado"

SERVICOS = [
    {"categoria": "Cílios", "itens": [
        {"nome": "Volume Brasileiro ou Egípcio", "preco": 180, "duracao": "1h30",
         "texto": "O volume mais natural, ideal para a primeira vez. Também no efeito U."},
        {"nome": "Mega Volumes", "preco": 180, "duracao": "2h",
         "texto": "Mais fios e mais preenchimento, alongado ou curtinho."},
        {"nome": "Efeitos (Sirena, Fox, Molhado, Kardashian)", "preco": 200, "duracao": "2h",
         "texto": "Os efeitos do momento, cada um com um desenho diferente no olhar."},
        {"nome": "Manutenção (até 21 dias)", "preco": 150, "duracao": "2h",
         "texto": "Para quem fez a aplicação ou a última manutenção há até 21 dias."},
        {"nome": "Lash lifting", "preco": 120, "duracao": "1h",
         "texto": "Seus próprios cílios alinhados para cima, sem extensão."},
        {"nome": "Remoção", "preco": 15, "duracao": "30 min",
         "texto": "Valor diferente quando a aplicação foi feita por outra profissional."},
    ]},
    {"categoria": "Sobrancelhas", "itens": [
        {"nome": "Design personalizado", "preco": 50, "duracao": "30 min",
         "texto": "Desenho medido para a proporção do seu rosto."},
        {"nome": "Design com henna", "preco": 65, "duracao": "50 min",
         "texto": "O design com cor para preencher as falhas."},
        {"nome": "Design masculino", "preco": 50, "duracao": "30 min",
         "texto": "Limpeza e desenho discretos, sem cara de feito."},
        {"nome": "Brow Lamination", "preco": 95, "duracao": "1h20",
         "texto": "Fios alinhados para cima com efeito de preenchimento. Henna opcional inclusa."},
        {"nome": "Reconstrução de sobrancelhas", "preco": 65, "duracao": "30 min",
         "texto": "Cuidado com os fios para eles voltarem a crescer no desenho certo."},
        {"nome": "Micropigmentação ou microblading", "preco": 600, "duracao": "2h",
         "texto": "Longa duração. O pigmento desbota com o tempo."},
        {"nome": "Epilação de buço", "preco": 15, "duracao": "30 min",
         "texto": "Na cera ou na linha."},
    ]},
    {"categoria": "Lábios", "itens": [
        {"nome": "Hidragloss", "preco": 60, "duracao": "30 min",
         "texto": "Hidratação e cor de volta aos lábios."},
        {"nome": "Micropigmentação labial", "preco": 400, "duracao": "2h",
         "texto": "Cor de longa duração nos lábios, que desbota com o tempo."},
    ]},
]

PRIMEIRO_OLHAR = {
    "nome": "Primeiro Olhar", "preco": 315, "de": 330, "duracao": "1h30",
    "texto": "Aplicação completa no volume brasileiro ou egípcio e a sua primeira manutenção, "
             "que você já marca na saída.",
}

COMBOS = [
    {"nome": "Olhar Completo", "preco": 220, "de": 230,
     "inclui": "Volume brasileiro ou egípcio e design de sobrancelha"},
    {"nome": "Realeza", "preco": 295, "de": 310,
     "inclui": "Cílios com efeito, design de sobrancelha e hidragloss"},
    {"nome": "Manutenção Glow", "preco": 200, "de": 210,
     "inclui": "Manutenção de cílios e hidragloss"},
]

PACOTES = [
    {"nome": "Brow Perfeita", "preco": 395, "de": 415,
     "inclui": "3 Brow Lamination com design e 2 design com henna", "primeira_sessao": "Brow Lamination"},
    {"nome": "Reconstrução", "preco": 372, "de": 390,
     "inclui": "6 sessões de reconstrução de sobrancelhas", "primeira_sessao": "Reconstrução"},
    {"nome": "Plano de manutenção", "preco": 285, "de": 300,
     "inclui": "2 manutenções de cílios por mês", "primeira_sessao": "Manutenção"},
]

_PARTICULAR = [
    "Aula individual",
    "Mentoria com 2 encontros online",
    "Suporte por até 6 meses",
    "Acompanhamento por videochamada nos primeiros atendimentos",
    "Apostila física e em PDF",
    "Kit de treino e box mimo",
    "Fotos e vídeos do seu atendimento para o portfólio",
    "Certificado e coffee break",
]

CURSOS = [
    {"id": "micro-profissional", "grupo": "micropigmentacao",
     "nome": "Formação Profissional em Micropigmentação de Sobrancelhas", "preco": 1497,
     "formato": "Presencial, no studio do Rio Comprido",
     "resumo": "Formação presencial em micropigmentação de sobrancelhas com teoria, biossegurança, "
               "treino em pele sintética e prática em modelo real.",
     "inclui": ["Aula teórica completa", "Biossegurança", "Visagismo e marcação",
                "Colorimetria e escolha dos pigmentos", "Tipos de pele", "Materiais e equipamentos",
                "Técnica e treino em pele sintética", "Prática em modelo real", "Cuidados antes e depois",
                "Orientações para começar a atender", "Apostila digital e certificado",
                "Suporte por 3 meses depois do curso"],
     "aviso": "O kit profissional não está incluso: os materiais da prática são disponibilizados durante o curso."},
    {"id": "micro-vip", "grupo": "micropigmentacao",
     "nome": "Formação VIP em Micropigmentação de Sobrancelhas", "preco": 2297,
     "formato": "Presencial e individual, no studio do Rio Comprido",
     "resumo": "Tudo da formação profissional, com aula individual, kit profissional para levar e "
               "acompanhamento nos primeiros atendimentos.",
     "inclui": ["Tudo da Formação Profissional", "Aula individual e modelo exclusivo",
                "Correção individual da técnica", "Kit profissional inicial para levar",
                "Apostila física e digital e certificado", "2 encontros de mentoria online depois da formação",
                "Suporte por 6 meses", "Acompanhamento nos primeiros atendimentos"]},
    {"id": "design", "grupo": "design-cilios", "nome": "Curso Particular de Design de Sobrancelhas",
     "preco": 797, "formato": "Individual, 12 horas em 2 dias, com modelo real no segundo dia",
     "resumo": "Curso particular e presencial de design de sobrancelhas, com modelo real.",
     "inclui": _PARTICULAR},
    {"id": "cilios", "grupo": "design-cilios", "nome": "Curso Particular de Extensão de Cílios",
     "preco": 997, "formato": "Individual, 12 horas em 2 dias, com modelo real no segundo dia",
     "resumo": "Curso particular e presencial de extensão de cílios, com modelo real.",
     "inclui": _PARTICULAR},
    {"id": "design-cilios", "grupo": "design-cilios", "nome": "Design de Sobrancelhas e Extensão de Cílios",
     "preco": 1597, "de": 1794, "formato": "Os dois cursos particulares, cada um com as suas datas",
     "resumo": "Os cursos particulares de design de sobrancelhas e de extensão de cílios juntos.",
     "inclui": _PARTICULAR},
]

ADICIONAL_FOTOS = 100
PAGAMENTO_CURSOS = "Formas de pagamento e parcelamento a combinar"

AVALIACOES_STUDIO = [
    {"nome": "Ana Luiza",
     "texto": "super acolhedora, ótima profissional, faz um trabalho impecável e muito bem feito. Ela arrasa, confio demais!"},
    {"nome": "Juliana Custodio",
     "texto": "Além de você ser uma profissional extremamente competente e deixar meus cílios impecáveis, "
              "sua energia e doçura tornam o atendimento uma delícia."},
    {"nome": "Roseane Almeida",
     "texto": "Encontrei o perfil da Laryssa por acaso no instagram. Estava a procura de uma profissional pra "
              "fazer minhas sobrancelhas... desde então nunca mais fiz minhas sobrancelhas em outro lugar."},
    {"nome": "Adriana Valentim",
     "texto": "toda vez que eu faço meus cílios, saio renovada com a autoestima lá em cima, rs!!"},
]

AVALIACAO_ACADEMY = {
    "nome": "Myllena Andrade",
    "texto": "Fiz o curso de cílios com ela e dá pra ver o quanto ela domina o que faz. "
             "Explica super bem, tem paciência e passa muita segurança...",
}

FAQ = [
    ("Quanto tempo leva a aplicação de cílios?",
     "O volume brasileiro ou egípcio leva cerca de 1h30. Mega volumes e efeitos, cerca de 2h. "
     "Você fica deitada, de olho fechado, e muita gente cochila."),
    ("De quanto em quanto tempo faço a manutenção?",
     "Até 21 dias depois da aplicação ou da última manutenção. Depois disso o cílio natural já renovou "
     "quase todo e o certo é uma aplicação nova."),
    ("Extensão de cílios estraga o cílio natural?",
     "Não, quando o fio tem o peso certo para o seu cílio e a aplicação é feita fio a fio, "
     "sem colar um cílio no outro."),
    ("Quais cuidados depois da aplicação?",
     "Nas primeiras 24 horas, evite molhar e não esfregue os olhos. Não use rímel nos fios aplicados. "
     "Na saída eu te passo todos os cuidados."),
    ("E se eu tiver alergia?",
     "Reação à cola pode acontecer com qualquer pessoa. Se arder, coçar ou inchar, me chama que eu retiro, "
     "e procure atendimento médico se o incômodo continuar. Se você já teve reação antes, me conta antes de marcar."),
    ("Quanto tempo dura a micropigmentação?",
     "É de longa duração, mas não é para sempre: o pigmento desbota com o tempo."),
    ("Quais as formas de pagamento?",
     "Pix, dinheiro e cartão. Nos pacotes, o valor anunciado é à vista no Pix, e no cartão entra a taxa da maquininha."),
]

ALT_FOTOS = {
    "cilios-classico": "Extensão de cílios com volume brasileiro feita no studio Rainha do Olhar",
    "cilios-mega": "Extensão de cílios com mega volume",
    "cilios-efeito": "Extensão de cílios com efeito",
    "sobrancelha-design": "Design de sobrancelha personalizado",
    "sobrancelha-henna": "Design de sobrancelha com henna",
    "sobrancelha-lamination": "Sobrancelha com brow lamination",
    "sobrancelha-reconstrucao": "Sobrancelha em reconstrução",
    "labios-hidragloss": "Lábios depois do hidragloss",
    "studio": "Espaço do studio Rainha do Olhar no Rio Comprido",
    "laryssa": "Laryssa, do Rainha do Olhar",
    "micropigmentacao-antes": "Sobrancelha antes da micropigmentação",
    "micropigmentacao-depois": "Sobrancelha depois da micropigmentação, no Rainha do Olhar",
}


def preco(nome):
    for categoria in SERVICOS:
        for item in categoria["itens"]:
            if item["nome"] == nome:
                return item["preco"]
    raise KeyError(nome)
