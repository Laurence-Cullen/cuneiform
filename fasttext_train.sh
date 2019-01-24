#!/usr/bin/env bash

LANGUAGE=akkadian

../../fastText-0.2.0/fasttext skipgram \
 -input tokenised_corpuses/${LANGUAGE}.txt \
  -output embeddings/fasttext_${LANGUAGE} \
  -minCount 0 \
  -minn 2 \
  -wordNgrams 6 \
  -epoch 30000 \
  -dim 100 \
  -lr 0.2 \
  -neg 5