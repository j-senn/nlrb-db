from bs4 import BeautifulSoup as bs


class Docket:
    date = None
    document = None
    issued_by = None
    has_pdf = False

    def __init__(self, html: str):
        soup = bs(html, 'html.parser')

        if soup is None or soup.text == '':
            raise ValueError('No docket data found')

        docket = soup.find_all('td')

        self.date = docket[0].text.strip()
        # TODO: grab link as well. Maybe swap has_pdf bool for link
        self.document = docket[1].text.strip()
        self.issued_by = docket[2].text.strip()
        self.has_pdf = '*' not in self.document  # '*' indicates a pdf is not present

    def __str__(self):
        return f'Docket: {self.date} | {self.document} | {self.issued_by} | {self.has_pdf}'

    @staticmethod
    def find_dockets(html: str):
        soup = bs(html, 'html.parser')
        soup = soup.find('div', {'id': 'case_docket_activity_data'}).find('table').find('tbody')
        return [Docket(str(tr)) for tr in soup.find_all('tr')]
