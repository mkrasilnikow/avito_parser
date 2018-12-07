import logging
import requests
from parsers.html_parser import HtmlParser
from vpn.simple_vpn import Vpn
from time import sleep
from random import uniform

logger = logging.getLogger(__name__)


class Scrapper(object):
    def __init__(self, skip_objects=None):
        self.skip_objects = skip_objects

    def scrap_process(self, storage, url, vpn):

        html_parser = HtmlParser()

        if vpn:
            vpn = Vpn()
            proxy = vpn.get_proxy()
            user_agent = vpn.get_user_agent()
        else:
            proxy = None
            user_agent = None

        response = requests.get(url, headers=user_agent, proxies=proxy)
        logger.info('Now we use: user-agent=' + str(user_agent) + '   proxy=' + str(proxy))
        total_pages = html_parser.get_pages(response.text)
        logger.info("total pages is " + str(total_pages))
        storage.write_data([])
        for i in range(1, total_pages + 1):
            generated_url = url + '?p=' + str(i)
            logger.info("Get url " + generated_url)
            sleep(10)
            try:
                html = html_parser.get_html(generated_url, user_agent, proxy)
                storage.append_data(html_parser.get_page_data(html))
            except:
                logger.error("Can't get page data from page " + str(i))
                continue

