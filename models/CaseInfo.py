import re

from bs4 import BeautifulSoup as bs


class CaseInfo:
    case_number = None
    date_filed = None
    status = None
    num_employees = None
    location = None
    region = None
    description = None

    def __init__(self, html: str):
        soup = bs(html, 'html.parser')

        general_info = soup.find('div', {'class': 'display-flex flex-justify flex-wrap'})

        if general_info is None or soup.text == '':
            raise ValueError('No case data found')

        self.case_number = self.find_field(general_info, 'Case Number')
        self.date_filed = self.find_field(general_info, 'Date Filed')
        self.status = self.find_field(general_info, 'Status')
        self.num_employees = self.find_field(general_info, 'of Employees')
        self.location = self.find_field(general_info, 'Location')
        self.region = self.find_field(general_info, 'Region Assigned')
        self.description = self.find_field(general_info, 'Unit Description')

    def __str__(self):
        return f'Case Info: ' \
               f'{self.case_number} | {self.date_filed} | {self.status} |' \
               f'{self.num_employees} | {self.location} | {self.region} | {self.description[:25]}'

    def find_field(self, soup, key: str):
        try:
            field = soup.find('b', string=re.compile(key)).next_sibling.strip()
        except AttributeError:
            # TODO: Logging?
            field = None

        return field
