import datetime
import time
from concurrent.futures import ThreadPoolExecutor

from bs4 import BeautifulSoup as bs
import requests
import pandas as pd

url = 'https://www.nlrb.gov/case/'
data_dir = 'case_htmls'


def timing(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f'{func.__name__} took {end - start} seconds')
        return result
    return wrapper


def load_cases():
    cases = pd.read_csv('cases.csv')
    return cases['Case Number'].tolist()


def scrape_case(case):
    case_url = url + case
    response = requests.get(case_url)
    if response.status_code != 200:
        print(f'Error: {response.status_code} for {case_url}')
        return
    case_soup = bs(response.content, 'html.parser').prettify()

    # TODO: do we care about diffs?
    with open(f'{data_dir}/{case}.html', 'w', encoding='utf-8') as f:
        f.write(case_soup)
        print(f'Downloaded {case}.html at {time.localtime()}')
    return


@timing
def parallel_scrape(cases):
    with ThreadPoolExecutor(max_workers=20) as executor:
        results = executor.map(scrape_case, cases)
    return results


@timing
def main():
    case_numbers = load_cases()
    print(f"Downloading {len(case_numbers)} cases")

    parallel_scrape(case_numbers)
    print(f'Downloaded {len(case_numbers)} at {datetime.datetime.now()}')
    return


if __name__ == '__main__':
    main()
