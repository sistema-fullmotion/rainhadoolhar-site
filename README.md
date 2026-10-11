# Site Rainha do Olhar

Site estático do Rainha do Olhar (studio de cílios e sobrancelhas no Rio Comprido e Academy).
Servido por nginx no EasyPanel, construído a partir do Dockerfile deste repositório.

- Fatos e preços: `data.py` (única fonte do site)
- Gerar: `python build.py` (exige as fotos obrigatórias em `fotos/`, ver `images.py`) ou `python build.py --sem-fotos`
- Testes: `python -m pytest`
- Conferir se os serviços do site existem e estão liberados no Maapp: `python verificar_precos.py maapp_services.json`
- Publicar: commit do `dist/`, push, e Implantar no EasyPanel (projeto `rainhadoolhar`, app `site`)

## Provador de olhar (topo do studio)

As opções ficam em `data.PROVADOR`. Por padrão cada opção usa uma foto que o site já publica (a mesma da seção Serviços), então nada é baixado duas vezes:
Marcante = `cilios-efeito`, Dramático = `cilios-mega`, Design = `sobrancelha-design`, Henna = `sobrancelha-henna`, Lamination = `sobrancelha-lamination`, Hidratado = `labios-hidragloss`.

Para trocar a foto de uma opção, salve em `fotos/` um arquivo chamado `provador-<grupo>-<opção>` (jpg, jpeg, png ou webp), por exemplo `provador-cilios-marcante`. Esse arquivo vence a foto compartilhada. O Natural dos cílios só tem foto própria (`provador-cilios-natural`); o Natural dos lábios fica sem foto de propósito.
Cada foto do provador deve pesar no máximo 120 KB depois do build (um teste confere).

A opção **Micropigmentado** só aparece quando existir `fotos/provador-labios-micropigmentado.*`. Para ligar, salve a foto com esse nome, rode `python build.py`, faça commit do `dist/` e publique.

Só use fotos de clientes da própria Laryssa.
