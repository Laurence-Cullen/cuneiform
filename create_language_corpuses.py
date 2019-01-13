import pandas as pd


def main():
    corpus = pd.read_pickle('transliterations_raw.pickle')

    # cat_row = catalogue.loc[catalogue['id'] == getattr(row, 'id')]

    print(corpus['language'].values)

    sumerian_corpus = corpus[corpus['language'].str.contains('Sumerian', na=False)]
    akkadian_corpus = corpus[corpus['language'].str.contains('Akkadian', na=False)]
    hittite_corpus = corpus[corpus['language'].str.contains('Hittite', na=False)]

    # corpuses = [sumerian_corpus, akkadian_corpus, hittite_corpus]

    print(sumerian_corpus)

    with open('raw_corpuses/sumerian_raw_corpus.txt', mode='w') as file:

        for row in sumerian_corpus.itertuples():
            file.write(getattr(row, 'translit') + '\n')

    print(akkadian_corpus)

    with open('raw_corpuses/akkadian_raw_corpus.txt', mode='w') as file:

        for row in akkadian_corpus.itertuples():
            file.write(getattr(row, 'translit') + '\n')

    print(hittite_corpus)

    with open('raw_corpuses/hittite_raw_corpus.txt', mode='w') as file:

        for row in hittite_corpus.itertuples():
            file.write(getattr(row, 'translit') + '\n')


if __name__ == '__main__':
    main()
