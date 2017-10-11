from datetime import datetime
import requests
import re
from bs4 import BeautifulSoup


class Plugin():

    # registra o plugin e qual o padrão de url ele deve ser chamado
    # o primeiro parametro é o nome do arquivo
    # o segundo a o padrão em regex da URL
    def register_plugin(self, PluginManager):
        PluginManager.register_plugin('estadao_com_br', r"^https?://(opiniao|politica|economia"
                                                       +r"|brasil|internacional|esportes|cultura"
                                                       +r"|educacao|ciencia|saude|sustentabilidade"
                                                       +r"|sao-paulo).estadao.com.br/noticias/")

    # returna um dicionario contendo três chaves
    # subtitle
    # date_published em formato datetime object
    # content
    # o content é o único obrigatório
    def extract_metadata(self, url):
        self.url = url
        self.page = None
        self.bs = None

        r = requests.get(self.url)
        if r.status_code == 200:
            self.page = r.text
            self.bs = BeautifulSoup(self.page, 'html.parser')

            subtitle = self._get_subtitle()
            date_published = self._get_published_date()

            self._remove_elements()

            content = self._get_content()

            metadata = dict(subtitle=subtitle,
                            date_published=date_published,
                            content=content)
            return metadata
        else:
            return None

    # remove elementos indesejados da pagina, titulos no meio
    # da materia etc... se precisar.
    def _remove_elements(self):
        for div in self.bs.find_all(['style']):
            div.decompose()


    # localiza o subtitulo pelo seletor css
    def _get_subtitle(self):
        subtitle = self.bs.select_one('h2.n--noticia__subtitle')
        return subtitle.get_text()

    # localiza e parsea a data para formato datetime obj
    def _get_published_date(self):
        # Talvez seja feito futuramente...
        pass

    # localiza os paragrafos 
    def _get_content(self):
        paragraphs_list = []
        paragraphs = self.bs.select('.n--noticia__content > p')
        for paragraph in paragraphs:
            if len(paragraph.text) > 20:
                paragraphs_list.append(paragraph.text.strip())
        return ' '.join(paragraphs_list)

    # Isso é irrelevante para o bot, útil para testar standalone =)
def test():
    url = 'http://politica.estadao.com.br/noticias/geral,relatorio-de-bonifacio-de-andrada-pede-rejeicao-de-denuncia-contra-temer,70002037566'
    pl = Plugin()
    metadata = pl.extract_metadata(url)
    print(metadata)

if __name__ == '__main__':
    test()