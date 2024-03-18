import argparse
import datetime
import os
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
        error = None
        for i in range(max_attempts):
            try:
                return func(*args, **kwargs)
            # On any failure, catch, warn, sleep in case of rate limiting, and try again
            except Exception as e:
                logger.warning(f'Error executing {func.__name__} with {",".join(*args)} and {", ".join(**kwargs)}: {e}')
                time.sleep(delay)
                error = e
        # If we've gotten here 3 requests have failed. Log error and return None
        logger.error(f'Error executing {func.__name__} with {",".join(*args)} and {", ".join(**kwargs)}: {error}')

    return wrapper


def load_cases(filename):
    """
    Load case numbers from a csv file.
    :param filename:
    :return:
    """
    filename = filename if filename else 'cases.csv'
    cases = pd.read_csv(filename)
    return cases['Case Number'].tolist()


@try_again
def scrape_case(case):
    """
    Get the html for a case by case number. Write the html to a file.
    Skip case # if file already exists.
    :param case:
    :return:
    """
    case_file = f'{data_dir}/{case}.html'
    if os.path.exists(case_file):
        logger.debug(f'{case_file} already exists. Skipping download')
        return

    # Get the page for case #
    case_url = url + case
    response = requests.get(case_url)
    if response.status_code != 200:
        logger.warning(f'Error: {response.status_code} for {case_url}')
        raise Exception(f'Error: {response.status_code} for {case_url}')

    case_soup = bs(response.content, 'html.parser').prettify()

    # Write the page to a file
    with open(case_file, 'w', encoding='utf-8') as f:
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
    parse = argparse.ArgumentParser(description='Scrape NLRB case data')
    parse.add_argument('-c', '--cases', type=str, help='Path to case numbers')

    args = parse.parse_args()

    case_numbers = load_cases(args.cases)
    logger.info(f"Downloading {len(case_numbers)} cases")

    parallel_scrape(case_numbers)
    logger.info(f'Downloaded {len(case_numbers)} at {datetime.datetime.now()}')
    return


if __name__ == '__main__':
    main()
