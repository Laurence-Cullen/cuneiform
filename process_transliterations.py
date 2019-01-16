# import re

import pandas as pd

import atf_parser
strip_non_alphanum_regex = r'[^a-zA-Z0-9\ ]'


def main():
    catalogue = pd.read_csv('data/cdli_catalogue.csv', error_bad_lines=False)
    transliterations, translations = atf_parser.parse_atf_file('data/cdliatf_unblocked.atf')

    transliterations = atf_parser.annotate_with_catalogue_data(catalogue, transliterations)

    transliterations.to_pickle('transliterations_raw.pickle')
    # transliterations.to_csv('transliterations_raw.csv')

    # print(transliterations)
    #
    # word_count = 0
    #
    # all_words = set()
    #
    # for string in translations['translation'].values:
    #     clean_string = re.sub(pattern=strip_non_alphanum_regex, repl='', string=string)
    #
    #     words = clean_string.split(' ')
    #     word_count += len(words)
    #
    #     for word in words:
    #         all_words.add(word)

    # print('number of english translated:', word_count)
    # print('unique english words', len(all_words))


if __name__ == '__main__':
    main()
