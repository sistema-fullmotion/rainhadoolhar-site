# Site Rainha do Olhar

Site estático do Rainha do Olhar (studio de cílios e sobrancelhas no Rio Comprido e Academy).
Servido por nginx no EasyPanel, construído a partir do Dockerfile deste repositório.

- Fatos e preços: `data.py` (única fonte do site)
- Gerar: `python build.py` (exige as 10 fotos em `fotos/`) ou `python build.py --sem-fotos`
- Testes: `python -m pytest`
- Conferir preços contra o Maapp: `python verificar_precos.py maapp_services.json`
- Publicar: commit do `dist/`, push, e Implantar no EasyPanel (projeto `rainhadoolhar`, app `site`)
