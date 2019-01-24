# import re

import pandas as pd

import atf_parser
strip_non_alphanum_regex = r'[^a-zA-Z0-9\ ]'


def main():
    catalogue = pd.read_csv('CDLI_data/cdli_catalogue.csv', error_bad_lines=False)
    transliterations, translations = atf_parser.parse_atf_file('CDLI_data/cdliatf_unblocked.atf')

    transliterations = atf_parser.annotate_with_catalogue_data(catalogue, transliterations)

    transliterations.to_pickle('transliterations_raw.pickle')


if __name__ == '__main__':
    main()
