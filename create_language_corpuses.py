import pandas as pd

monolingual_folder = 'monolingual_corpuses/'
language_pairs_folder = 'language_pairs/'


def save_monolingual_corpuses(corpuses, sep='\n'):
    for file_name, corpus in corpuses.items():

        transliterations = []

        for row in corpus.itertuples():
            transliterations.append(getattr(row, 'translit'))

        file_content = sep.join(transliterations)

        file = open(monolingual_folder + file_name, mode='w')
        print(file_content, flush=True, file=file)
        file.close()


def save_language_pairs(translation_pairs):
    for language_name, corpus in translation_pairs.items():
        translit_file = open(language_pairs_folder + language_name + '.txt', mode='w')
        translated_file = open(language_pairs_folder + 'translated_' + language_name + '.txt', mode='w')
        tsv_file = open(language_pairs_folder + language_name + '.tsv', mode='w')

        tsv_file.write('translit\ttranslation\n')

        dead_translations = ['basket-of-tablets:', 'xxx', '(subscript)', ';', '']
        dead_transliterations = ['']

        pair_set = set()

        for row in corpus.itertuples():
            if isinstance(getattr(row, 'translation'), str):
                translation = str(getattr(row, 'translation')).replace('\t', '')
                transliteration = str(getattr(row, 'translit')).replace('\t', '')

                pair = (transliteration, translation)

                if translation in dead_translations or transliteration in dead_transliterations or pair in pair_set:
                    continue

                pair_set.add(pair)

                translit_file.write(transliteration + '\n')
                translated_file.write(translation + '\n')

                tsv_file.write(transliteration + '\t' + translation + '\n')

        translit_file.close()
        translated_file.close()


def main():
    omni_corpus = pd.read_pickle('transliterations_raw.pickle')

    sumerian_corpus = omni_corpus[omni_corpus['language'].str.contains('Sumerian', na=False)]
    akkadian_corpus = omni_corpus[omni_corpus['language'].str.contains('Akkadian', na=False)]
    hittite_corpus = omni_corpus[omni_corpus['language'].str.contains('Hittite', na=False)]
    undetermined_corpus = omni_corpus[omni_corpus['language'].isnull()]

    newline_separated_corpuses = {
        'omni.txt': omni_corpus,
        'sumerian.txt': sumerian_corpus,
        'akkadian.txt': akkadian_corpus,
        'hittite.txt': hittite_corpus,
        'undetermined.txt': undetermined_corpus
    }

    save_monolingual_corpuses(newline_separated_corpuses)

    translation_pairs = {
        'sumerian': sumerian_corpus,
        'akkadian': akkadian_corpus,
        'hittite': hittite_corpus
    }

    save_language_pairs(translation_pairs)


if __name__ == '__main__':
    main()
