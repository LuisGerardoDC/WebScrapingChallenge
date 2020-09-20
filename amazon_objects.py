import requests
import lxml.html as lxhtml

from common import config

class Page:
    def __init__(self,url):
        self._config = config()['amazon']
        self._queries = self._config['products']
        self._html = None
        self._visit(url)
        self.url = url
    

    def _select(self, query_string):
        return self._html.xpath(query_string)


    def _visit(self, url):
        response = requests.get(url)
        home = response.content.decode('utf-8')
        self._html = lxhtml.fromstring(home)
    

class HomePage(Page):
    def __init__(self,url):
        super().__init__(url)

    @property
    def product_links(self):
        return self._select(self._queries['product_links'])

class ArticlePage(Page):

    def __init__(self,url):
        super().__init__(url)

    @property
    def name(self):
        result = self._select(self._queries['product_name'])
        return result

    @property
    def price(self):
        result = self._select(self._queries['product_price'])
        return result
