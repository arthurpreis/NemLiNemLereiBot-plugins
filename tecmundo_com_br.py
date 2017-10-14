from datetime import datetime
import requests
import re
from bs4 import BeautifulSoup


class Plugin():

    # registra o plugin e qual o padrão de url ele deve ser chamado
    # o primeiro parametro é o nome do arquivo
    # o segundo a o padrão em regex da URL
    def register_plugin(self, PluginManager):
        PluginManager.register_plugin('tecmundo_com_br', r"^https?://tecmundo.com.br/""(internet|mercado)")

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


    def _remove_elements(self):
        for el in self.bs.find_all(['b'] ,text=re.compile(r'^(Confira|Leia também|Promoção|Desconto):')):
            try:
                el.parent.decompose()
            except AttributeError:
                pass
        #TODO: remover "Cupons de Desconto" do corpo do texto


    # localiza o subtitulo pelo seletor css
    def _get_subtitle(self):
        subtitle = self.bs.select_one('h1.article-title')
        return subtitle.get_text()

    # localiza e parsea a data para formato datetime obj
    def _get_published_date(self):
        months = {'janeiro': '01', 'fevereiro': '02', 'março': '03', 'abril': '04',
                    'maio': '05', 'junho': '06', 'julho': '07', 'agosto': '08',
                    'setembro': '09', 'outubro': '10', 'novembro': '11', 'dezembro': '12',
                    'jan': '01', 'fev': '02', 'mar': '03', 'abr': '04',
                    'mai': '05', 'jun': '06', 'jul': '07', 'ago': '08',
                    'set': '09', 'out': '10', 'nov': '11', 'dez': '12'}
        state = str(self.bs.select('.article-header'))
        date = re.search(r'([0-9])+( )+\w+ ([0-9])+', state).group(0).split(' ')
        date[1] = months[date[1].lower()]
        date_str = date[0] + '/' + date[1] + '/' + date[2]
        date_published = datetime.strptime(date_str, "%d/%m/%Y").date()
        return date_published


    # localiza os paragrafos
    def _get_content(self):
        paragraphs_list = []
        paragraphs = self.bs.select('div.article-text > p')
        for paragraph in paragraphs:
            if len(paragraph.text) > 20:
                paragraphs_list.append(paragraph.text.strip())
        return ' '.join(paragraphs_list)

    # Isso é irrelevante para o bot, útil para testar standalone =)
def test():
    url = 'https://www.tecmundo.com.br/mercado/123043-treta-qualcomm-que-banir-completamente-iphone-china.htm'
    pl = Plugin()
    metadata = pl.extract_metadata(url)
    print(metadata)

if __name__ == '__main__':
    test()
