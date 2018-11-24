import requests
from bs4 import BeautifulSoup



class HtmlParser:

    def parse(self, data):
        """
        Parses html text and extracts field values
        :param data: html text (page)
        :return: a dictionary where key is one
        of defined fields and value is this field's value
        """
        soup = BeautifulSoup(data)

        # Your code here: find an appropriate html element

        # Your code here
        return [dict()]

    def get_html(self):
        return None
