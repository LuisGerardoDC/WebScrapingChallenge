import scrapy
from scrapy.http import HtmlResponse as htmlres

class ProductsSpider(scrapy.Spider):
    name = 'products'
    start_urls = [
        'https://www.amazon.com.mx/'
    ]
    custom_settings = {
        'FEED_URI': 'products.json',
        'FEED_FORMAT' :'json',
        'CURRENT_REQUESTS': 24,
        'MEMUSAGE_LIMIT_MB': 2048,
        'MEMUSAGE_NOTIFY_MAIL': ['luisgerarhern@outlook.com'],
        'ROBOTSTXT_OBEY' : True,
        'USER_AGENT': 'LuisHernandez',
        'FEED_EXPORT_ENCODIG' : 'utf-8'
    }

    def parse_search(self, response):
        product_name_xpath = '//h2/a/span/text()'
        product_price_xpath = '//span[@class = "a-price-whole"]/text()'
        all_products_xpath = '//div[@data-component-type="s-search-result"]'
        products_list = response.xpath(all_products_xpath).getall()
        print(f'{"*"*50}\n\n')
        products = []
        for produc_html in products_list:
            product_response = htmlres(url='producto',body=produc_html,encoding='utf-8')
            product_name = product_response.xpath(product_name_xpath).get() 
            product_price = product_response.xpath(product_price_xpath).get()
            print(f'[{product_name}\t-\t{product_price}]')
            products.append({
                'name':product_name,
                'price':product_price
            })
        
        yield {'products':products}

            
    def parse(self, response):
        search = getattr(self, 'search', None)
        if search:
            print(f'{"*"*50}\n\n')
            search = 's?k={}'.format(search.replace(' ','+'))
            yield response.follow(search, callback= self.parse_search)
            
    #facundo 