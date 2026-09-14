"""Nota de performance mobile pela API pública do PageSpeed. Uso: python pagespeed.py URL [URL...]"""
import json
import sys
import urllib.parse
import urllib.request


def nota(url):
    consulta = urllib.parse.urlencode({"url": url, "strategy": "mobile", "category": "performance"})
    with urllib.request.urlopen("https://www.googleapis.com/pagespeedonline/v5/runPagespeed?" + consulta,
                                timeout=180) as resposta:
        dados = json.load(resposta)
    return round(dados["lighthouseResult"]["categories"]["performance"]["score"] * 100)


if __name__ == "__main__":
    for endereco in sys.argv[1:]:
        print(endereco, nota(endereco))
