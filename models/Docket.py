import re

from bs4 import BeautifulSoup as bs


class Docket:
    date = None
    document = None
    issued_by = None
    url = None

    def __init__(self, html: str):
        soup = bs(html, 'html.parser')

        if soup is None or soup.text == '':
            raise ValueError('No docket data found')

        docket = soup.find_all('td')

        self.date = docket[0].text.strip()
        # TODO: grab link as well. Maybe swap has_pdf bool for link
        self.document = docket[1].text.strip()
        self.issued_by = docket[2].text.strip()

        if docket[1].find('a') is not None:
            self.url = docket[1].find('a')['href']

    def __str__(self):
        return f'Docket: {self.date} | {self.document} | {self.issued_by} | Has public doc: {self.url is not None}'

    @staticmethod
    def find_docket_table(html: str):
        """
        Get the Docket table body. If no table is found and no message indicating no data is available raise an exception.
        :param html:
        :return:
        """
        soup = bs(html, 'html.parser')
        table = soup.find('table', {'class': 'docket-activity-table'})
        if table is None:
            no_data_message = soup.find(string=re.compile('Docket Activity data is not available'))
            if no_data_message is None:
                raise Exception('ERROR: No docket activity data or message found.')
        return table

    @staticmethod
    def find_dockets(html: str):
        table = Docket.find_docket_table(html)
        if table is None:
            return None
        table = table.find('tbody')
        return [Docket(str(tr)) for tr in table.find_all('tr')]
