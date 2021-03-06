# Neural Machine Translation of Cuneiform

Progress! Managed to get a 12.38 BLEU score translating from Sumerian transliterations to English! This was trained from 13,000 unique sentence pairs on the Google AutoML Translation platform.

Inspired by the Ashurbanipal exhibition at the British Museum and a [book](https://www.amazon.co.uk/Cuneiform-Irving-Finkel/dp/0714111880) on [cuneiform](https://en.wikipedia.org/wiki/Cuneiform) writing from my excellent friend [Ellie Winter](https://eleanorwinter.com). I found that pretty much all the Cuneiform ever transliterated and translated is stored in a single digital library initiative. Some ~80,000 lines of cuneiform have been translated leaving almost 1.7 million lines for which no english translations have been generated. 

This repository is a store of my efforts towards neural machine translation of languages written in cuneiform including Sumerian, Akkadian, Hittite and others. It appears that a group of several researchers have been funded to work on machine translation of these language but so far no papers have been puplished other than [the one announcing](http://www.aclweb.org/anthology/W17-2202) the funding of the project and a high level description the NLP pipeline they plan to build. However it appears they planned to use more classical and hardcoded NLP techniques based on large quantities of human knowledge and dissection of the transliterated text. I saw the oppurtunity to use more flexible and modern techniques such as unsupervised word tokenisation and word embeddings in addition to transfer learning and attention based sequence models to attack the problem in a knowledge agnostic fashion.

I am looking to build a powerful NMT system to shine a light on the vast piles of untranslated cuneiform text using the latest research in low resource translation systems. 80,000 line might sound like a lot but typical production systems use tens of million of sentences!


## Work completed so far:
* Wrote script to grab the most recently updated cuneiform data dump from [CDLI](https://cdli.ucla.edu/?)
* Explored object catalogue statistics with the awesome [pandas-profiling](https://github.com/pandas-profiling/pandas-profiling)
* Parsed ATF file of object transliteration and translation
* Married transliterations and translation with catalogue metadata (language, provenence, genre, etc)
* Built single language plain text corpuses of [Akkadian](https://en.wikipedia.org/wiki/Akkadian_language), [Sumerian](https://en.wikipedia.org/wiki/Sumerian_language) and [Hittite](https://en.wikipedia.org/wiki/Hittite_language) transliterations
* Used [Sentence Piece](https://github.com/google/sentencepiece) by Google for unsupervised text tokenising of different languages
* Explored [Open-NMT](http://opennmt.net/) and trained a demo English to German translation model
* Found out what was happening to the ~30,000 lines of translated text that disapears when only lines following transliterations are saved, need to sift through translations in multiple languages to pull out english ones
* Created matched transliteration, translation file pairs
* Hit 12.38 BLEU for Sumerian -> English translation, woop woop!
* Researched [word embeddings for use in machine translation](http://www.aclweb.org/anthology/N18-2084), looks to have promise, especially for low resource languages. Loads of good ideas about using multilingual embeddings and encoders to squeze the most out of the limited datasets
* Found tools for [aligning word embeddings across languages](https://github.com/Babylonpartners/fastText_multilingual)
* Built multilingual corpus and split out undetermined language corpus
* Built sentence piece encodings from the entire Cuneiform transliterated dataset of 1.6 million lines
* Tokenised monolingual Sumerian corpus with learnt sentence piece model
* Built [GloVe embeddings](https://nlp.stanford.edu/projects/glove/) of tokenised Sumerian
* Added distance.py script for exploring word embeddings, enter a word and the 100 words with the highest cosine similarity will be displayed
* Built high performance FastText embeddings for Sumerian after some experimentation with training hyper parameters
* Started work on seq2seq model, built infrastructure to convert language pair corpuses to tokenised arrays
* Currently debugging sequence model architecture

