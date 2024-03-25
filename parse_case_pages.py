import os
import re
from os import path

from bs4 import BeautifulSoup as bs

from models import CaseInfo, CaseActivity, Docket, Participant


class Allegations:
    def __init__(self, html: str):
        soup = bs(html, 'html.parser')
        soup = soup.find('div', {'id': 'case_docket_activity_data'})
        has_docs = soup.find(string=re.compile("Allegations data is not available"))
        if has_docs is not None:
            raise NotImplementedError('Allegations data hasnt been implemented.')


class RelatedCases:
    def __init__(self, html: str):
        soup = bs(html, 'html.parser')
        soup = soup.find('div', {'id': 'case_docket_activity_data'})
        has_docs = soup.find(string=re.compile("Related Cases data is not available"))
        if has_docs is not None:
            raise NotImplementedError('Related Cases data hasnt been implemented.')


class CaseHtml:

    # TODO: Swich to passing around soup? rather than html strings?
    def __init__(self, html: str):
        soup = bs(html, 'html.parser')
        soup = soup.find('div', {'id': 'block-mainpagecontent'})
        self.html = soup.prettify()
        self.info = CaseInfo(self.html)
        # TODO: Handle no dockets
        self.docket = Docket.find_dockets(self.html)
        self.case_activity = self.load_case_activity(self.html)
        self.allegations = self.load_allegations(self.html)
        self.participants = self.load_participants(self.html)
        self.related_cases = RelatedCases(self.html)

        return

    def load_case_activity(self, html: str):
        try:
            return CaseActivity(html)
        except NotImplementedError as e:
            print(self.info.case_number + "HAS CASE ACTIVITY USE FOR IMPLEMENTATION")
            print(e)
            return None

    def load_allegations(self, html: str):
        try:
            return Allegations(html)
        except NotImplementedError as e:
            print(self.info.case_number + "HAS ALLEGATIONS USE FOR IMPLEMENTATION")
            print(e)
            return None

    def load_participants(self, html: str):
        participants = Participant.find_participants(html)
        return participants

def main():
    data_dir = path.join(os.getcwd() + '/case_htmls')
    file = path.join(data_dir, '32-RC-337328.html')

    with open(file, 'r', encoding='utf-8') as f:
        html = f.read()

    case = CaseHtml(html)
    print(case.info)
    print("\n".join(str(docket) for docket in case.docket))
    for participant in case.participants:
        print(participant)


if __name__ == '__main__':
    main()