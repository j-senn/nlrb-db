import re

from bs4 import BeautifulSoup as bs


class RelatedDocument:
    case_number = None
    name = None
    url = None

    def __init__(self, case_number: str, html: str):
        soup = bs(html, 'html.parser')
        a = soup.find('a')
        self.case_number = case_number
        self.name = a.text.strip()
        self.url = a['href']

    @staticmethod
    def find_allegation_list( html: str):
        """
        Get the Related document list. If no list is found and no message indicating no data is available raise an exception.
        :param html:
        :return:
        """
        soup = bs(html, 'html.parser')

        no_data_message = soup.find(string=re.compile('Related Documents data is not available'))
        if no_data_message is not None:
            return None

        documents_list = soup.find('h2', text=re.compile('Related Documents')).find_next('ul')

        return documents_list

    @staticmethod
    def find_related_documents(case_number: str, html: str):
        documents_list = RelatedDocument.find_allegation_list(html)
        if documents_list is None:
            return None
        return [RelatedDocument(case_number, str(li))
                for li in documents_list.find_all('li')]