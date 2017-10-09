from datetime import datetime
import requests
import re
from bs4 import BeautifulSoup


class Plugin():

    # registra o plugin e qual o padrão de url ele deve ser chamado
    # o primeiro parametro é o nome do arquivo
    # o segundo a o padrão em regex da URL
    def register_plugin(self, PluginManager):
        PluginManager.register_plugin(
            'g1_globo_com', r"^https?://g1.globo.com((?!/google/amp/))"
                            "(.*)/noticia/(.*).ghtml$")

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
        pass


    # localiza o subtitulo pelo seletor css
    def _get_subtitle(self):
        subtitle = self.bs.select_one('.content-head__subtitle')
        return subtitle.get_text()

    # localiza e parsea a data para formato datetime obj
    def _get_published_date(self):
        date = self.bs.select_one('time[itemprop="datePublished"]').get_text()
        if date:
            match_date = re.search(r'(\d{2})/(\d{2})/(\d{4})', date).group(0)
            date_published = datetime.strptime(match_date, "%d/%m/%Y").date()
            return date_published
        else:
            return None

    # localiza os paragrafos 
    def _get_content(self):
        paragraphs_list = []
        paragraphs = self.bs.find_all(
            "p", re.compile(r"content-text__container(.*)"))
        for paragraph in paragraphs:
            if len(paragraph.text) > 20:
                paragraphs_list.append(paragraph.text.strip())
        return ' '.join(paragraphs_list)

    # Isso é irrelevante para o bot, útil para testar standalone =)
def test():
    url = 'https://g1.globo.com/politica/noticia/relator-da-denuncia-contra-temer-diz-que-entregara-parecer-na-tarde-desta-terca.ghtml'
    pl = Plugin()
    metadata = pl.extract_metadata(url)
    print(metadata)

if __name__ == '__main__':
    test()