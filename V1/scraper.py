import argparse
import logging
import re
import csv
from requests.exceptions import HTTPError,ContentDecodingError
from urllib3.exceptions import MaxRetryError

logging.basicConfig(level=logging.INFO)
import amazon_objects as products

from common import config
is_well_formed_link = re.compile(r'^https?://.+/.+$')
is_root_path = re.compile(r'(/)(.+)$')
logger = logging.getLogger(__name__)

def _news_scraper(product):
    host = config()['amazon']['url']
    product = 's?k={}'.format(product.replace(' ','+'))
    logging.info(f'Beginning scraper for {host}{product}')
    try:
        homepage = products.HomePage(host+product)
        for link in homepage.product_links:
            builded_link = _build_link(host,link)
            try:
                _fetch_article(builded_link)
            except ValueError as ve:
                print(f'product page: {ve}')


    except ValueError as ve:
        print(f'Home page: {ve}')

def _fetch_article(link):
    logger.info(f'Start fetching article at {link}')
    try:
        article = products.ArticlePage(link)
        print(article.name)
        print(article.price)
    except (HTTPError, MaxRetryError,ContentDecodingError) as e:
        logger.warning(f'Error while fetching the article {e}')


def _build_link(host, link):
    if is_well_formed_link.match(link):
        return link
    elif is_root_path.match(link):
        return f'{host}{is_root_path.split(link)[2]}'
    else:
        return f'{host}/{link}'

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('product',
        help= 'proudcts',
        type= str,
    )
    args = parser.parse_args()
    _news_scraper(args.product)
