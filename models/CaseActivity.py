import re

from bs4 import BeautifulSoup as bs


class CaseActivity:
    def __init__(self, html: str):
        soup = bs(html, 'html.parser')
        soup = soup.find('div', {'id': 'case_docket_activity_data'})
        has_docs = soup.find(string=re.compile("Related Documents data is not available"))
        if has_docs is not None:
            raise NotImplementedError('Related Documents hasnt been implemented.')
1