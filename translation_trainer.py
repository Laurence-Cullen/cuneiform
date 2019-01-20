import keras
import numpy as np
import pandas as pd
import sentencepiece
from keras.layers import Input, Embedding, Dense, LSTM, Flatten
import tensorflow


def sentences_to_indices(sentence_array, sp_encoder, max_len):
    """
    Converts an array of sentences (strings) into an array of indices corresponding to words in the sentences.
    The output shape should be such that it can be given to `Embedding()` (described in Figure 4).

    Arguments:
    sentence_array -- array of sentences (strings), of shape (m, 1)
    word_to_index -- a dictionary containing the each word mapped to its index
    max_len -- maximum number of words in a sentence. You can assume every sentence in X is no longer than this.

    Returns:
    encoded_sentences -- array of indices corresponding to words in the sentences from X, of shape (m, max_len)
    """

    m = sentence_array.shape[0]  # number of training examples

    # Initialize encoded_sentences as a numpy matrix of zeros and the correct shape (≈ 1 line)
    encoded_sentences = np.zeros((m, max_len), dtype=int)

    for i in range(m):  # loop over training examples
        word_ids = None

        try:
            # Convert sentence into a list of IDs corresponding to character fragments
            word_ids = sp_encoder.EncodeAsIds(sentence_array[i])
        except TypeError:
            ValueError('failed to encode transliteration at line', i + 1)

        # Initialize j to 0
        j = 0

        # Loop over the words of sentence_words
        for word_id in word_ids:
            # if len(word_id) == 0:
            #     continue

            # Set the (i,j)th entry of encoded_sentences to the index of the correct word.
            encoded_sentences[i, j] = int(word_id)

            # Increment j to j + 1
            j += 1

    return encoded_sentences


def load_embeddings(embedding_path):
    embeddings_index = {}

    with open(embedding_path, mode='r') as file:
        for line in file:
            values = line.split()
            word = values[0]
            coefs = np.asarray(values[1:], dtype='float32')
            embeddings_index[word] = coefs

    print('Found %s word vectors.' % len(embeddings_index))

    return embeddings_index


def main():
    language = 'sumerian'

    english_sp = sentencepiece.SentencePieceProcessor()
    english_sp.load('sp_encodings/en.wiki.bpe.vs25000.model')
    english_vocab_size = len(pd.read_csv(
        'sp_encodings/en.wiki.bpe.vs25000.vocab',
        sep='\t',
        header=None,
        engine='python',
        quoting=3
    ))

    cuneiform_sp = sentencepiece.SentencePieceProcessor()
    cuneiform_sp.load('sp_encodings/omni.model')
    cuneiform_vocab_size = len(pd.read_csv('sp_encodings/omni.vocab', sep='\t', header=None))

    cuneiform_embeddings = load_embeddings('embeddings/0.11_loss_sumerian.vec')

    sentence_pairs = pd.read_csv('language_pairs/' + language + '.tsv', sep='\t')

    cuneiform_embedding_dims = len(cuneiform_embeddings['a'])
    english_embedding_dims = 100
    max_cuneiform_sentence_length = 200
    max_engish_sentence_length = 200
    lstm_units = 128
    batch_size = 64
    epochs = 10

    encoder_input_data = sentences_to_indices(
        sentence_array=sentence_pairs['translit'].values,
        sp_encoder=cuneiform_sp,
        max_len=max_cuneiform_sentence_length
    )

    decoder_input_data = sentences_to_indices(
        sentence_array=sentence_pairs['translation'].values,
        sp_encoder=english_sp,
        max_len=max_engish_sentence_length
    )

    decoder_target_data = np.zeros_like(decoder_input_data, dtype=int)

    for t in range(max_engish_sentence_length - 1):
        decoder_target_data[:, t] = decoder_input_data[:, t + 1]

    print(len(cuneiform_embeddings['a']))

    # Define an input sequence and process it.
    encoder_inputs = Input(shape=(None,))
    x = Embedding(cuneiform_vocab_size, cuneiform_embedding_dims)(encoder_inputs)
    x, state_h, state_c = LSTM(lstm_units, return_state=True)(x)
    encoder_states = [state_h, state_c]

    # Set up the decoder, using `encoder_states` as initial state.
    decoder_inputs = Input(shape=(None,))
    x = Embedding(english_vocab_size, english_embedding_dims)(decoder_inputs)
    x, _, _ = LSTM(lstm_units, return_sequences=True)(x, initial_state=encoder_states)
    decoder_outputs = Dense(english_vocab_size, activation='softmax')(x)

    # Define the model that will turn
    # `encoder_input_data` & `decoder_input_data` into `decoder_target_data`
    model = keras.Model([encoder_inputs, decoder_inputs], decoder_outputs)

    # Compile & run training
    model.compile(optimizer='rmsprop', loss='categorical_crossentropy')

    print(model.output_shape)

    # Note that `decoder_target_data` needs to be one-hot encoded,
    # rather than sequences of integers like `decoder_input_data`!
    model.fit([encoder_input_data, decoder_input_data], decoder_target_data,
              batch_size=batch_size,
              epochs=epochs,
              validation_split=0.2)


if __name__ == '__main__':
    main()
