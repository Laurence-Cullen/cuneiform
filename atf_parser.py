import pandas as pd
import re


def parse_atf(path):
    """
    Parse atf file at provided location into dataframe of transliterated line
    fragments with metadata such as the id of the object it is taken from and
    the language. Includes translations of transliterations if they exist.

    Returns:
        pd.DataFrame
    """

    object_id = ''
    translit_line_regex = r'^([0-9]{1,2}\`?\.[a-z]?[0-9]?[A-Z]?\.? )'
    translation_line_regex = r'^(#tr.[a-zA-Z]*: )'

    line_markers = {
        'id': '&P',
        'translation': '#tr.en: '
    }

    connective_characters = ['~', 'x', '?', '#', '@', '.', 'bx', '|', '(', ')']

    characters_to_strip = ['(', ')', '?', ',', '#', '|']

    counter = 0
    transliterations = []
    translations = []

    with open(path) as file:
        for line in file:
            counter += 1

            if counter % 10000 == 0:
                print("Processing line:", counter)

            # line = line.rstrip('\n')

            # match ID lines and store the most recent object ID found when
            # iterating through lines
            if line.startswith(line_markers['id']):
                fragments = line.split(' = ')
                object_id = fragments[0].lstrip(line_markers['id'])

            # search for transliteration lines, if found strip everything other
            # than the transliteration itself and add the transliteration to
            # data frame
            if re.match(translit_line_regex, line):
                line_start = re.search(translit_line_regex, line).group()
                translit = line.lstrip(line_start)
                translit = translit.rstrip(' \n')
                transliterations.append({'translit': translit, 'id': object_id})

            if re.match(translation_line_regex, line):
                line_start = re.search(translation_line_regex, line).group()
                translate = line.lstrip(line_start)
                translate = translate.rstrip(' \n')
                translations.append({'translation': translate, 'id': object_id})

    return pd.DataFrame(transliterations), pd.DataFrame(translations)


def main():
    # catalogue = pd.read_csv('data/cdli_catalogue.csv', error_bad_lines=False)
    transliterations, translations = parse_atf('data/cdliatf_unblocked.atf')
    print(translations)
    transliterations.to_csv('transliterations_raw.csv', index=False)

    word_count = 0

    all_words = set()

    for string in translations['translation'].values:
        words = string.split(' ')
        word_count += len(words)

        for word in words:
            all_words.add(word.strip(['(', ')', ',', '.']))

    print('number of english translated:', word_count)
    print('unique english words', len(all_words))


if __name__ == '__main__':
    main()
