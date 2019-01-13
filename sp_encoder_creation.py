import sentencepiece as sp


def main():
    sp.SentencePieceTrainer.Train(
        '--input=raw_corpuses/sumerian_raw_corpus.txt --model_prefix=sentence_piece_encodings/sumerian --vocab_size=1000'
    )
    sp.SentencePieceTrainer.Train(
        '--input=raw_corpuses/akkadian_raw_corpus.txt --model_prefix=sentence_piece_encodings/akkadian --vocab_size=1000'
    )
    sp.SentencePieceTrainer.Train(
        '--input=raw_corpuses/hittite_raw_corpus.txt --model_prefix=sentence_piece_encodings/hittite --vocab_size=1000'
    )


if __name__ == '__main__':
    main()
