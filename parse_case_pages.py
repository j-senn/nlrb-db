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
        self.case_number = self.info.case_number
        self.docket = Docket.find_dockets(main_html)
        self.related_documents = RelatedDocument.find_related_documents(self.case_number, main_html)
        self.allegations = Allegation.find_allegations(main_html)
        self.participants = Participant.find_participants(main_html)
        self.related_cases = RelatedCase.find_related_cases(self.case_number, main_html)
        return


def related_cases_to_csv(case, data_dir):
    file = path.join(data_dir, 'related_cases.tsv')

    if case.related_cases is None:
        return

    if not path.exists(file):
        with open(file, 'w', encoding='utf-8') as f:
            f.write('Pare_Case_Number\tCase_Number\tName\tStatus\n')

    with open(file, 'a+', encoding='utf-8') as f:
        for related in case.related_cases:
            f.write(f'{related.parent_case_number}\t{related.case_number}\t{related.case_name}\t{related.status}\n')


def related_docs_to_csv(case, data_dir):
    file = path.join(data_dir, 'related_docs.tsv')

    if case.related_documents is None:
        return

    if not path.exists(file):
        with open(file, 'w', encoding='utf-8') as f:
            f.write('Case_Number\tName\tURL\n')

    with open(file, 'a+', encoding='utf-8') as f:
        for doc in case.related_documents:
            f.write(f'{case.case_number}\t{doc.name}\t{doc.url}\n')


def parse_all(data_dir, output_dir):
    # Ignore .gitignore
    htmls = [html for html in os.listdir(data_dir) if html.endswith('.html')]

    for case_html in htmls:
        with open(path.join(data_dir, case_html), 'r', encoding='utf-8') as f:
            html = f.read()
        try:
            case = Case(html)
            related_docs_to_csv(case, output_dir)
            related_cases_to_csv(case, output_dir)
        except Exception as e:
            print(case_html)
            print(e)
            raise e


def parse_one(case_html):
    with open(case_html, 'r', encoding='utf-8') as f:
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
    output_dir = path.join(os.getcwd() + '/tsvs')
    # parse_one(file)
    parse_all(data_dir, output_dir)


if __name__ == '__main__':
    main()
