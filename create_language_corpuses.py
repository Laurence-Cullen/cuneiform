import math

import pandas as pd


save_folder = 'raw_corpuses/'


def main():
    omni_corpus = pd.read_pickle('transliterations_raw.pickle')

    sumerian_corpus = omni_corpus[omni_corpus['language'].str.contains('Sumerian', na=False)]
    akkadian_corpus = omni_corpus[omni_corpus['language'].str.contains('Akkadian', na=False)]
    hittite_corpus = omni_corpus[omni_corpus['language'].str.contains('Hittite', na=False)]
    corpuses = {
        # 'omni_raw_corpus.txt': omni_corpus,
        'sumerian_raw_corpus.txt': sumerian_corpus,
        'akkadian_raw_corpus.txt': akkadian_corpus,
        'hittite_raw_corpus.txt': hittite_corpus
    }

    for file_name, corpus in corpuses.items():

        with open(save_folder + file_name, mode='w') as file:

            for row in corpus.itertuples():
                file.write(getattr(row, 'translit') + '\n')

    # TODO figure out WTF is going on, why can't I concatenate the files?
    # with open(save_folder + 'proper_omni_corpus.txt', mode='w') as omni_file:
    #     for file_name, _ in corpuses.items():
    #
    #         with open(save_folder + file_name, mode='r') as file:
    #             omni_file.write(file.read())

    # TODO create transliteration, translation pairs

    translation_pairs = {
        # 'omni_raw_corpus.txt': omni_corpus,
        'sumerian': sumerian_corpus,
        'akkadian': akkadian_corpus,
        'hittite': hittite_corpus
    }

    output_dir = 'language_pairs/'

    for language_name, corpus in translation_pairs.items():
        translit_file = open(output_dir + language_name + '.txt', mode='w')
        translated_file = open(output_dir + 'translated_' + language_name + '.txt', mode='w')

        for row in corpus.itertuples():
            if isinstance(getattr(row, 'translation'), str):
                translit_file.write(getattr(row, 'translit') + '\n')
                translated_file.write(str(getattr(row, 'translation')) + '\n')

        translit_file.close()
        translated_file.close()


if __name__ == '__main__':
    main()
