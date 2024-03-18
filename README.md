Case Details were retrieved from the NLRB website using the search and "Download CSV" feature. 
Searches were batched into time periods containing about 50,000 cases. 
However, some files were unable to be parsed by Pandas immediately so 'Case Numbers' were
extracted using the grep regex 

`'[:digit:]{2}-[:alpha:]{2}-[:digit:]{6}'`

This did lead to a discrepancy in the number of cases the NLRB said they were providing and parsed case numbers.

Example command line usage:

`python scrape_case_pages.py -c case_numbers.csv`

Notes on behavior:
- This script skips cases that already have a file in the `case_htmls` directory.
- This process is still slow taking 3-4 hours per 50,000 cases.
- It doesn't have any command line output and has sparse logging. You can check the `case_htmls` directory to see it's progress `ls -l case_htmls | wc -l`