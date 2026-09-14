from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]


def test_dockerfile_serve_dist_com_nginx():
    linhas = (RAIZ / "Dockerfile").read_text().splitlines()
    assert linhas[0] == "FROM nginx:alpine"
    assert "COPY dist/ /usr/share/nginx/html/" in linhas


def test_nginx_cache_redirect_relativo_e_gzip():
    n = (RAIZ / "nginx.conf").read_text()
    assert "absolute_redirect off;" in n
    assert 'add_header Cache-Control "no-cache, must-revalidate";' in n
    assert "location /img/" in n and "immutable" in n
    assert "gzip on;" in n


def test_fotos_originais_fora_do_git():
    assert "fotos/" in (RAIZ / ".gitignore").read_text().splitlines()
