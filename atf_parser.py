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

    line_markers = {
        'id': '&P',
        'translation': '#tr.en: '
    }


    counter = 0

    transliterations = []

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

                # transliterations.append({'translit': translit, 'id': object_id}, ignore_index=True)

    return pd.DataFrame(transliterations)


def main():
    # catalogue = pd.read_csv('data/cdli_catalogue.csv', error_bad_lines=False)
    transliterations = parse_atf('data/cdliatf_unblocked.atf')
    print(transliterations)


if __name__ == '__main__':
    main()

