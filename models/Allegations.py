from bs4 import BeautifulSoup as bs
import re


class Allegations:
    allegation = None

    def __init__(self, html: str):
        li = bs(html, 'html.parser')
        self.allegation = li.text.strip()

    def __str__(self):
        return f'Allegation: {self.allegation}'

    @staticmethod
    def find_allegation_list(html: str):
        """
        Get the Allegation table body. If no table is found and no message indicating no data is available raise an exception.
        :param html:
        :return:
        """
        soup = bs(html, 'html.parser')
        allegations_list = soup.find('h2', text=re.compile('Allegations')).find_next('ul')

        if allegations_list is None:
            no_data_message = soup.find(string=re.compile('Allegations data is not available'))
            if no_data_message is None:
                raise Exception('ERROR: No allegations data or message found.')

        return allegations_list

    @staticmethod
    def find_allegations(html: str):
        allegations_list = Allegations.find_allegation_list(html)
        if allegations_list is None:
            return None
        return [Allegations(str(li)) for li in allegations_list.find_all('li')]
