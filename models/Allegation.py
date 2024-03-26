from bs4 import BeautifulSoup as bs
import re


class Allegation:
    allegation = None

    def __init__(self, html: str):
        li = bs(html, 'html.parser')
        self.allegation = li.text.strip()

    def __str__(self):
        return f'Allegation: {self.allegation}'

    @staticmethod
    def find_allegation_list(html: str):
        """
        Get the Allegations list. If no list is found and no message indicating no data is available raise an exception.
        :param html:
        :return:
        """
        soup = bs(html, 'html.parser')

        no_data_message = soup.find(string=re.compile('Allegations data is not available'))
        if no_data_message is not None:
            return None

        allegations_list = soup.find('h2', text=re.compile('Allegations')).find_next('ul')

        return allegations_list

    @staticmethod
    def find_allegations(html: str):
        allegations_list = Allegation.find_allegation_list(html)
        if allegations_list is None:
            return None
        return [Allegation(str(li)) for li in allegations_list.find_all('li')]
