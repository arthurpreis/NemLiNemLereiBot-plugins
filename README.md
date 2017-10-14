# NemLiNemLereiBot-plugins

O [NemLiNemLereiBot](https://github.com/CaioWzy/NemLiNemLereiBot) utiliza os plugins para extrair o metadata das not�cias e de acordo com as idiossincrasias de cada site sem poluir o c�digo do bot.

## Portais de not�cias postados no r/brasil

- [x] http://estadao.com.br
- [x] http://www1.folha.uol.com.br/ *paywall*
- [x] http://www.gazetadopovo.com.br/
- [x] https://g1.globo.com
- [ ] https://www.cartacapital.com.br
-- [x] t�tulo
-- [x] data
-- [ ]conte�do
- [x] http://www.correiobraziliense.com.br/
- [x] http://www.correio24horas.com.br/
- [ ] ~~http://www.dw.com/~~ *n�o � br* 
- [ ] http://www.jb.com.br/
-- [x] t�tulo
-- [x] data
-- [ ]conte�do
- [x] http://www.jornaldebrasilia.com.br/
- [ ] https://www.tecmundo.com.br/
-- [x] t�tulo
-- [x] data
-- [x]conte�do
-- [ ] remover propagandas (cupons de desconto) do corpo do texto
- [ ] ~~https://www.theintercept.com/~~ *n�o � br*

## TODO:
1. Ir implementando (g1 � o mais utilizado);
2. ~~Quantificar quais s�o os portais mais postados no sub;~~ vide stats_ (mesmo assim tem mta noticia postada com outras flairs.... � poss�vel que eu repasse o script)
3. Possivelmente refatorar parsers que sejam parecidos em mais de um site;
4. Estat�sticas de uso e qualidade de cada plugin (?);
5. Manter;
6. ~~Adicionar automaticamente a lista de plugins a ser implementados conforme posts novos com a flair 'not�cia'.~~ vide site_rank.py






