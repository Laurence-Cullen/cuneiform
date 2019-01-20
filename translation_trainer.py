import pandas as pd
import numpy as np
import math
import keras.layers as layers
import sentencepiece


def main():
    language = 'sumerian'

    english_sp = sentencepiece.SentencePieceProcessor()
    english_sp.load('sp_encodings/en.wiki.bbe.vs25000.model')

    cuneiform_sp = sentencepiece.SentencePieceProcessor()
    cuneiform_sp.load('sp_encodings/omni.model')



if __name__ == '__main__':
    main()
