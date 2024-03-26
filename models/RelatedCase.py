from bs4 import BeautifulSoup as bs
import re


class RelatedCase:
    case_number = None
    case_name = None
    status = None

    def __init__(self, html: str):
        soup = bs(html, 'html.parser')
        columns = soup.find_all('td')
        self.case_number = columns[0].text.strip()
        self.case_name = columns[1].text.strip()
        self.status = columns[2].text.strip()

    def __str__(self):
        return f'Related Case: {self.case_number} | {self.case_name} | {self.status}'

    @staticmethod
    def find_case_table(html: str):
        """
        Get the Related cases table body. If no table is found and no message indicating no data is available raise an exception.
        :param html:
        :return:
        """
        soup = bs(html, 'html.parser')
        table = soup.find('table', {'class': 'related-case'})
        if table is None:
            no_data_message = soup.find(string=re.compile('Related Cases data is not available'))
            if no_data_message is None:
                raise Exception('ERROR: No related case data or message found.')
        return table

    @staticmethod
    def find_related_cases(html: str):
        table = RelatedCase.find_case_table(html)
        if table is None:
            return None
        table = table.find('tbody')
        return [RelatedCase(str(tr)) for tr in table.find_all('tr')
]