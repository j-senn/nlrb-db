import re

from bs4 import BeautifulSoup as bs


class Participant:
    legal_role = None
    description = None
    names = None
    address = None
    phone = None

    def __init__(self, html: str):
        soup = bs(html, 'html.parser')
        columns = soup.find_all('td')
        self.split_participant(columns[0])
        self.address = self.clean_address(columns[1].text)
        self.phone = columns[2].text.strip()

    def __str__(self):
        return f'Participant: {self.legal_role} | {self.description} | {",".join(self.names)}' \
               f' | {self.address} | {self.phone}'

    def clean_address(self, address: str):
        a = re.sub(r'\n\s*\n', '\n', address).strip()
        return a

    def split_participant(self, soup):
        participant_details = [detail.strip() for detail in soup.strings if detail.strip()]
        self.legal_role = participant_details[0]
        self.description = participant_details[1]
        self.names = [name for name in participant_details[2:]]

    @staticmethod
    def find_participants(html: str):
        soup = bs(html, 'html.parser')
        soup = soup.find('table', {'class': 'Participants'}).find('tbody')
        # rows_with_data = [row.parent.parent for row in soup.find_all('br')]
        participants = [Participant(str(row)) for row in soup.find_all('tr') if not row.find('td', {'colspan': '3'})]
        return participants