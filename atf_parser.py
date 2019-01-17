import contextlib
import re

import pandas as pd

translit_line_regex = r'^([0-9]{1,2}\`?\.[a-z]?[0-9]?[A-Z]?\.? )'
translation_line_regex = r'^(#tr.[a-zA-Z]*: )'
strip_non_alphanum_regex = r'[^a-zA-Z0-9\ ]'


def parse_atf_file(path):
    """
    Parse atf file at provided location into dataframe of transliterated line
    fragments with metadata such as the id of the object it is taken from and
    the language. Includes translations of transliterations if they exist.

    Returns:
        pd.DataFrame
    """

    object_id = ''

    line_markers = {
        'id': '&P',
        'translation': '#tr.en: '
    }

    counter = 0
    transliterations = []
    translations = []

    with open(path) as file:
        lines = []

        for line in file:
            lines.append(line)

        for i in range(len(lines)):
            line = lines[i]

            counter += 1

            if counter % 10000 == 0:
                print("Processing line:", counter)

            # line = line.rstrip('\n')

            # match ID lines and store the most recent object ID found when
            # iterating through lines
            if line.startswith(line_markers['id']):
                fragments = line.split(' = ')

                with contextlib.suppress(ValueError):
                    object_id = int(fragments[0].lstrip(line_markers['id']))

            # search for transliteration lines, if found strip everything other
            # than the transliteration itself and add the transliteration to
            # respective data frame
            if re.match(translit_line_regex, line):
                line_start = re.search(translit_line_regex, line).group()
                translit = line.lstrip(line_start)
                translit = translit.rstrip(' \n')

                # default state is no translation being found
                translation = None

                for look_ahead in range(1, 20):

                    next_line = lines[i + look_ahead]

                    # Look ahead from transliteration to see if an english translation for it exists
                    if re.match(translation_line_regex, next_line):

                        line_start = re.search(translation_line_regex, next_line).group()

                        if line_start == '#tr.en: ':
                            translation = next_line.lstrip(line_start)
                            translation = translation.rstrip(' \n')
                            translations.append({'translation': translation, 'id': object_id})

                            transliterations.append({'translit': translit, 'id': object_id, 'translation': translation})

                            break

                if translation is None:
                    transliterations.append({'translit': translit, 'id': object_id})

    return pd.DataFrame(transliterations), pd.DataFrame(translations)


def annotate_with_catalogue_data(catalogue, transliterations):

    annotated_transliterations = []
    object_id = 1

    cat_row = catalogue.loc[catalogue['id'] == object_id]

    for row in transliterations.itertuples():

        row_object_id = getattr(row, 'id')

        if object_id != row_object_id:

            print(object_id)

            object_id = row_object_id

            try:
                cat_row = catalogue.loc[catalogue['id'] == getattr(row, 'id')].iloc[0]
            # catching what appears to be a missing id problem
            except IndexError:
                continue

        translation = getattr(row, 'translation')
        translit = getattr(row, 'translit')

        with contextlib.suppress(AttributeError):
            translation = translation.lower()

        with contextlib.suppress(AttributeError):
            translit = translit.lower()

        annotated_transliterations.append({
            'id': row_object_id,
            'translation': translation,
            'translit': translit,
            'language': cat_row['language'],
            # 'collection': cat_row['collection'],
            # 'genre': cat_row['genre'],
            # 'subgenre': cat_row['subgenre'],
            # 'height': cat_row['height'],
            # 'thickness': cat_row['thickness'],
            # 'width': cat_row['width'],
            # 'material': cat_row['material'],
            # 'object_type': cat_row['object_type'],
            # 'period': cat_row['period'],
            # 'provenience': cat_row['provenience']
        })

    print('finished annotating with catalogue data')

    return pd.DataFrame(annotated_transliterations)
