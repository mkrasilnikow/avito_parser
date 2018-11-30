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
        data = []
        ads = soup.find('div', class_='catalog-list').find_all('div', class_='item_table-description')
        for ad in ads:
            # type of flat, square, price, floor, total floors, distance to subway
            title = ad.find('a', class_='item-description-title-link').find('span').text.split(',')
            type_of_flat = title[0]
            area = re.search(r'(.+) м²', title[1])[0]
            floors = re.findall(r'\d+', title[2])
            floor = floors[0]
            total_floors = floors[1]
            price = ad.find('span', class_='price').text.strip()
            full_address = ad.find('p', class_='address').text.strip()
            try:
                distance_to_subway = ad.find('p', class_='address').find('span', class_="c-2").string.strip()
                subway = re.match(r'\D+', full_address).group(0).strip()
            except:
                distance_to_subway = ''
                subway = ''
            # print(type_of_flat + '= ' + area[0] + '= ' + floor + '= ' +
            #       total_floors + ' pr= ' + price + " " + subway + " " + distance_to_subway)
            data.append({'type_of_flat': type_of_flat,
                         'area': area,
                         'floor': floor,
                         'total_floors': total_floors,
                         'subway': subway,
                         'distance_to_subway': distance_to_subway,
                         'price': price, })
        return data

    def scrap_process(self, storage, query):

        base_url = 'https://www.avito.ru/sankt-peterburg/kvartiry/prodam/'
        page_url = '?p='
        static_url = base_url + query + page_url + '1'

        response = requests.get(static_url)
        total_pages = self.get_pages(response.text)

        for i in range(total_pages):
            generated_url = base_url + query + page_url + str(i)
            html = self.get_html(generated_url)

            storage.write_data(self.get_page_data(html))
