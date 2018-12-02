import logging
import requests
from parsers.html_parser import HtmlParser

logger = logging.getLogger(__name__)


class Scrapper(object):
    def __init__(self, skip_objects=None):
        self.skip_objects = skip_objects

    def scrap_process(self, storage, query):

        html_parser = HtmlParser()
        base_url = 'https://www.avito.ru/sankt-peterburg/kvartiry/prodam/'
        page_url = '?p='
        static_url = base_url + query + page_url + '1'
        response = requests.get(static_url)
        total_pages = html_parser.get_pages(response.text)
        logger.info("total pages is " + str(total_pages))
        storage.write_data([])
        for i in range(total_pages):
            generated_url = base_url + query + page_url + str(i)
            logger.info("Get url " + generated_url)
            html = html_parser.get_html(generated_url)
            logger.info("Get page data from page " + str(i))
            storage.append_data(html_parser.get_page_data(html))
