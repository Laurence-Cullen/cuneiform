import sentencepiece as spm


def main():
    sumerian_sp = spm.SentencePieceProcessor()
    sumerian_sp.Load("sp_encodings/sumerian.model")

    akkadian_sp = spm.SentencePieceProcessor()
    akkadian_sp.Load("sp_encodings/akkadian.model")

    hittite_sp = spm.SentencePieceProcessor()
    hittite_sp.Load("sp_encodings/hittite.model")


    test_sentence = "(N36) 1(N45) , SZE~a EN~a SANGA~a HI# AN# NUN~a UB GIR3@g~b UB APIN~a UD5~a"

    sumerian_encoded = sumerian_sp.EncodeAsPieces(test_sentence)
    akkadian_encoded = akkadian_sp.EncodeAsPieces(test_sentence)
    hittite_encoded = hittite_sp.EncodeAsPieces(test_sentence)

    print('Sumerian:', sumerian_encoded)
    print('Akkadian:', akkadian_encoded)
    print('Hittite: ', hittite_encoded)


if __name__ == '__main__':
    main()
