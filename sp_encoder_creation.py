import sentencepiece as sp


def main():

    vocab_size = str(2000)

    sp.SentencePieceTrainer.Train(
        '--input=raw_corpuses/sumerian_raw_corpus.txt --model_prefix=sp_encodings/sumerian --vocab_size=' + vocab_size
    )
    sp.SentencePieceTrainer.Train(
        '--input=raw_corpuses/akkadian_raw_corpus.txt --model_prefix=sp_encodings/akkadian --vocab_size=' + vocab_size
    )
    sp.SentencePieceTrainer.Train(
        '--input=raw_corpuses/hittite_raw_corpus.txt --model_prefix=sp_encodings/hittite --vocab_size=' + vocab_size
    )


if __name__ == '__main__':
    main()
