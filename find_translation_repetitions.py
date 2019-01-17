from collections import Counter

import pandas as pd

corpus = pd.read_csv('language_pairs/sumerian.tsv', sep='\t', dtype='str')

a = corpus['translation'].values
letter_counts = Counter(a)

print(letter_counts)
