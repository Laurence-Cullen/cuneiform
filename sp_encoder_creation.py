import sentencepiece as sp


def main():

    vocab_size = str(5000)

    sp.SentencePieceTrainer.Train(
        '--input=monolingual_corpuses/omni.txt --model_prefix=sp_encodings/omni --vocab_size=' + vocab_size
    )
    # sp.SentencePieceTrainer.Train(
    #     '--input=monolingual_corpuses/sumerian.txt --model_prefix=sp_encodings/sumerian --vocab_size=' + vocab_size
    # )
    # sp.SentencePieceTrainer.Train(
    #     '--input=monolingual_corpuses/akkadian.txt --model_prefix=sp_encodings/akkadian --vocab_size=' + vocab_size
    # )
    # sp.SentencePieceTrainer.Train(
    #     '--input=monolingual_corpuses/hittite.txt --model_prefix=sp_encodings/hittite --vocab_size=' + vocab_size
    # )


if __name__ == '__main__':
    main()
