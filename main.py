import datetime
from concurrent.futures import ThreadPoolExecutor

import logging
import time

from bs4 import BeautifulSoup as bs
import requests
import pandas as pd

logger = logging.getLogger(__name__)
logging.basicConfig(filename=f'logs/nlrb_case_scraper_{datetime.datetime.now().strftime("%Y-%m-%d")}', level=logging.INFO)

url = 'https://www.nlrb.gov/case/'
data_dir = 'case_htmls'


def timing(func):
    """
    Decorator. Time the execution of a function.
    :param func: function to time
    :return:
    """
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f'{func.__name__} took {end - start} seconds')
        logger.info(f'{func.__name__} took {end - start} seconds')
        return result
    return wrapper


def try_again(func):
    """
    Decorator. Retry a function if it fails.
    :param func: function to retry
    :return:
    """
    def wrapper(*args, **kwargs):
        max_attempts = 3
        delay = 3
        for i in range(max_attempts):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                time.sleep(delay)
        logger.error(f'Error executing {func.__name__} with {",".join(*args)} and {", ".join(**kwargs)}: {e}')

    return wrapper


def load_cases():
    cases = pd.read_csv('cases.csv')
    return cases['Case Number'].tolist()


@try_again
def scrape_case(case):
    case_url = url + case
    response = requests.get(case_url)
    if response.status_code != 200:
        logger.warning(f'Error: {response.status_code} for {case_url}')
        raise Exception(f'Error: {response.status_code} for {case_url}')

    case_soup = bs(response.content, 'html.parser').prettify()

    # TODO: do we care about diffs?
    with open(f'{data_dir}/{case}.html', 'w', encoding='utf-8') as f:
        f.write(case_soup)
        logger.debug(f'Downloaded {case}.html at {time.localtime()}')
    return


@timing
def parallel_scrape(cases):
    with ThreadPoolExecutor(max_workers=50) as executor:
        results = executor.map(scrape_case, cases)
    return results


@timing
def main():
    case_numbers = load_cases()
    logger.info(f"Downloading {len(case_numbers)} cases")

    parallel_scrape(case_numbers[:50])
    logger.info(f'Downloaded {len(case_numbers)} at {datetime.datetime.now()}')
    return


if __name__ == '__main__':
    main()
