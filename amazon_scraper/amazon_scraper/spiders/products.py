import scrapy

class ProductsSpider(scrapy.Spider):
    name = 'products'
    start_urls = [
        'https://www.amazon.com.mx/'
    ]
    custom_settings = {
        'FEED_URI': 'products.csv',
        'FEED_FORMAT' :'csv',
        'CURRENT_REQUESTS': 24,
        'MEMUSAGE_LIMIT_MB': 2048,
        'MEMUSAGE_NOTIFY_MAIL': ['luisgerarhern@outlook.com'],
        'ROBOTSTXT_OBEY' : True,
        'USER_AGENT': 'LuisHernandez',
        'FEED_EXPORT_ENCODIG' : 'utf-8'
    }
    def parse_product(self, response, **kwargs):
        if kwargs:
            products = kwargs['products']
        product_name_xpath = '//span[@id="productTitle"]/text()'
        product_price_xpath =  '//span[@id="priceblock_ourprice"]/text()'
        product_name = response.xpath(product_name_xpath).get()
        product_price = response.xpath(product_price_xpath).get()
        yield{product_name,product_price}

    def parse(self, response):
        search = getattr(self, 'search', None)
        if search:
            print(f'{"*"*50}\n\n')
            search = 's?k={}'.format(search.replace(' ','+'))
            yield response.follow(search, callback= self.parse)
            next_page_xpath = '//li[@class="a-last"]/a/@href'
            links_xpath = '//div[@class="a-section aok-relative s-image-square-aspect"]/../@href'
            next_page_button = response.xpath(next_page_xpath).get()
            
            for i in range(3):
                product_list = response.xpath(links_xpath).getall()
                for product in product_list:
                    yield response.follow(product, callback = self.parse_product)
                yield response.follow(next_page_button, callback = self.parse)
            
                        

            