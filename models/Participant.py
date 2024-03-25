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
    def find_participant_table(html: str):
        '''
        Get the Participant table body. If no table is found and no message indicating no data is available raise an exception.
        :param html:
        :return:
        '''
        soup = bs(html, 'html.parser')
        table = soup.find('table', {'class': 'Participants'})
        if table is None:
            no_data_message = soup.find(string=re.compile('Participants data is not available'))
            if no_data_message is None:
                raise Exception('ERROR: No participant data or message found.')
        return table

    @staticmethod
    def find_participants(html: str):
        table = Participant.find_participant_table(html)
        if table is None:
            return None

        table = table.find('tbody')

        return [Participant(str(row)) for row in table.find_all('tr') if not row.find('td', {'colspan': '3'})]
