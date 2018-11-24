import logging
import requests
import re

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

class Scrapper(object):
    def __init__(self, skip_objects=None):
        self.skip_objects = skip_objects

    def get_html(self, url):
        response = requests.get(url)
        if not response.ok:
            logger.error(response.text)
        else:
            return response.text

    def get_pages(self, html):
        soup = BeautifulSoup(html, 'lxml')
        pages = soup.find('div', class_='pagination-pages').find_all('a', class_='pagination-page')[-1].get('href')
        return int(re.findall(r'p=(\d+)', pages)[0])

    def get_page_data(self, html):
        soup = BeautifulSoup(html, 'lxml')
        ads = soup.find('div', class_='catalog-list').find_all('div', class_='item_table-description')
        for ad in ads:
            #type of flat, square, price, floor, total floors, distance to subway
            title = ad.find('div', class_='item_table-header')\
                .find('a', class_='item-description-title-link').find('span').text
            print(title)
            '''try:
                type
            except:
            '''



    def scrap_process(self, storage):

        base_url = 'https://www.avito.ru/sankt-peterburg/kvartiry/prodam/'
        page_url = '?p='
        #TODO: Вынести в константы и параметры командной строки
        query = 'studii'
        static_url = base_url+query+page_url+'1'

        response = requests.get(static_url)
        total_pages = self.get_pages(response.text)

        for i in range(1):
            generated_url = base_url+query+page_url+str(i)
            html = self.get_html(generated_url)
            self.get_page_data(html)


            # storage.write_data(str(data))

