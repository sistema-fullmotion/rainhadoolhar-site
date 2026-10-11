# Site Rainha do Olhar

Site estático do Rainha do Olhar (studio de cílios e sobrancelhas no Rio Comprido e Academy).
Servido por nginx no EasyPanel, construído a partir do Dockerfile deste repositório.

- Fatos e preços: `data.py` (única fonte do site)
- Gerar: `python build.py` (exige as fotos obrigatórias em `fotos/`, ver `images.py`) ou `python build.py --sem-fotos`
- Testes: `python -m pytest`
- Conferir se os serviços do site existem e estão liberados no Maapp: `python verificar_precos.py maapp_services.json`
- Publicar: commit do `dist/`, push, e Implantar no EasyPanel (projeto `rainhadoolhar`, app `site`)

## Provador de olhar (topo do studio)

As opções ficam em `data.PROVADOR`. Cada opção usa uma foto em `fotos/` com o nome `provador-<grupo>-<opção>` (jpg, jpeg, png ou webp):
`provador-cilios-natural`, `provador-cilios-marcante`, `provador-cilios-dramatico`, `provador-sobrancelha-design`,
`provador-sobrancelha-henna`, `provador-sobrancelha-lamination`, `provador-labios-hidratado`.

A opção **Micropigmentado** só aparece quando existir `fotos/provador-labios-micropigmentado.*`. Para ligar, salve a foto com esse nome, rode `python build.py`, faça commit do `dist/` e publique.

Só use fotos de clientes da própria Laryssa.
