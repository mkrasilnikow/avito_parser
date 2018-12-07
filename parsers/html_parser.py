import requests
from bs4 import BeautifulSoup
import logging
import re
from converters import distance_converter

logger = logging.getLogger(__name__)


class HtmlParser(object):
    def __init__(self, skip_objects=None):
        self.skip_objects = skip_objects

    def get_html(self, url, user_agent=None, proxy=None):
        response = requests.get(url, headers=user_agent, proxies=proxy)
        logger.info('Now we use: user-agent=' + str(user_agent) + '   proxy=' + str(proxy))
        if not response.ok:
            logger.error(response.text)
        else:
            return response.text

    def get_pages(self, html):
        soup = BeautifulSoup(html, 'lxml')
        try:
            pages = soup.find('div', class_='pagination-pages').find_all('a', class_='pagination-page')[-1].get('href')
        except:
            logger.error("Can't get number of pages")
            return 0
        return int(re.findall(r'p=(\d+)', pages)[0])

    def get_page_data(self, html):
        soup = BeautifulSoup(html, 'lxml')
        data = []
        try:
            ads = soup.find('div', class_='catalog-list').find_all('div', class_='item_table-description')
        except:
            logger.error("Can't parse catalog-list")
        for ad in ads:
            # type of flat, square, price, floor, total floors, distance to subway
            try:
                title = ad.find('a', class_='item-description-title-link').find('span').text.split(',')
            except AttributeError:
                logger.error("Can't parse title")
            type_of_flat = title[0]
            area = re.search(r'(.+) м²', title[1])[0]
            floors = re.findall(r'\d+', title[2])
            floor = floors[0]
            total_floors = floors[1]
            try:
                price = ad.find('span', class_='price').text.strip()
                full_address = ad.find('p', class_='address').text.strip()
            except AttributeError:
                logger.error("Can't parse price and full_address")
            try:
                distance_to_subway = ad.find('p', class_='address').find('span', class_="c-2").string.strip()
                distance_to_subway = distance_converter.convert(re.search(r'\d+.\d+', distance_to_subway).group(0))
                subway = re.match(r'\D+', full_address).group(0).strip()
            except AttributeError:
                logger.warning("Distance to subway or subway station is not defined!")
                distance_to_subway = ''
                subway = ''
            data.append({'type_of_flat': type_of_flat,
                         'area': area,
                         'floor': floor,
                         'total_floors': total_floors,
                         'subway': subway,
                         'distance_to_subway': distance_to_subway,
                         'price': price, })
        return data
