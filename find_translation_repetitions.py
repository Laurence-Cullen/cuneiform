import pandas as pd
from collections import Counter

import matplotlib.pyplot as plt


corpus = pd.read_csv('language_pairs/sumerian.tsv', sep='\t', dtype='str')


a = corpus['translation'].values
letter_counts = Counter(a)

print(letter_counts)

# df = pd.DataFrame.from_dict(letter_counts, orient='index')
# df.plot(kind='bar')
#
# plt.show()
