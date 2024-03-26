import os
from os import path

from bs4 import BeautifulSoup as bs

from models.Allegation import Allegation
from models.CaseInfo import CaseInfo
from models.Docket import Docket
from models.RelatedDocument import RelatedDocument
from models.RelatedCase import RelatedCase
from models.Participant import Participant


class Case:

    # TODO: Swich to passing around soup? rather than html strings?
    def __init__(self, html: str):
        soup = bs(html, 'html.parser')
        main_html = str(soup.find('div', {'id': 'block-mainpagecontent'}))

        self.info = CaseInfo(main_html)
        self.docket = Docket.find_dockets(main_html)
        self.related_documents = RelatedDocument(main_html)
        self.allegations = Allegation.find_allegations(main_html)
        self.participants = Participant.find_participants(main_html)
        self.related_cases = RelatedCase.find_related_cases(main_html)
        return


def parse_all(data_dir):
    # Ignore .gitignore
    htmls = [html for html in os.listdir(data_dir) if html.endswith('.html')]

    for case_html in htmls:
        with open(path.join(data_dir, case_html), 'r', encoding='utf-8') as f:
            html = f.read()
        try:
            case = Case(html)
        except Exception as e:
            print(case_html)
            print(e)
            raise e

def parse_one(data_dir, case_html):
    with open(path.join(data_dir, case_html), 'r', encoding='utf-8') as f:
        html = f.read()
    try:
        case = Case(html)
    except Exception as e:
        print(case_html)
        print(e)
        raise e

def main():
    data_dir = path.join(os.getcwd() + '/case_htmls')
    file = path.join(data_dir, '08-RD-002121.html')

    parse_one(data_dir, '08-RD-002121.html')

if __name__ == '__main__':
    main()
