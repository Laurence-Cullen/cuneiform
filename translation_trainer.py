import keras
import numpy as np
import pandas as pd
import sentencepiece
from keras.layers import Input, Embedding, Dense, LSTM


def sentences_to_indices(sentence_array, sp_encoder, max_len, add_start_frag=False):
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

    start_index = 1
    end_index = 2

    # Initialize encoded_sentences as a numpy matrix of zeros and the correct shape (≈ 1 line)
    encoded_sentences = np.ones((m, max_len), dtype=int) * end_index

    for i in range(m):  # loop over training examples
        word_ids = None

        try:
            # Convert sentence into a list of IDs corresponding to character fragments
            word_ids = sp_encoder.EncodeAsIds(sentence_array[i])
        except TypeError:
            ValueError('failed to encode transliteration at line', i + 1)

        # Initialize j to 0
        j = 0

        if add_start_frag:
            word_ids = [start_index] + word_ids

        # Loop over the words of sentence_words
        for word_id in word_ids:

            # Set the (i,j)th entry of encoded_sentences to the index of the correct word.
            encoded_sentences[i, j] = int(word_id)

            # Increment j to j + 1
            j += 1

    return encoded_sentences


def load_embedding_index(embedding_path):
    embeddings_index = {}

    with open(embedding_path, mode='r') as file:
        for line in file:
            values = line.split()
            word = values[0]
            coefs = np.asarray(values[1:], dtype='float32')
            embeddings_index[word] = coefs

    print('Found %s word vectors.' % len(embeddings_index))

    return embeddings_index


def build_word_index(vocab):
    word_index = {}

    for row in vocab.itertuples():
        print(row)
        word_index[getattr(row, '_1')] = getattr(row, 'Index')

    return word_index


def build_embedding_matrix(embeddings_index, dimensions, word_index):
    embedding_matrix = np.zeros((len(word_index), dimensions))
    for word, i in word_index.items():
        embedding_vector = embeddings_index.get(word)
        if embedding_vector is not None:
            # words not found in embedding index will be all-zeros.
            embedding_matrix[i] = embedding_vector

    return embedding_matrix


def main():
    language = 'sumerian'

    english_sp = sentencepiece.SentencePieceProcessor()
    english_sp.load('sp_encodings/en.wiki.bpe.vs5000.model')
    english_vocab_size = len(pd.read_csv(
        'sp_encodings/en.wiki.bpe.vs5000.vocab',
        sep='\t',
        header=None,
        engine='python',
        quoting=3
    ))

    cuneiform_sp = sentencepiece.SentencePieceProcessor()
    cuneiform_sp.load('sp_encodings/omni.model')
    cuneiform_vocab = pd.read_csv('sp_encodings/omni.vocab', sep='\t', header=None)
    cuneiform_word_index = build_word_index(cuneiform_vocab)
    print(cuneiform_vocab)

    cuneiform_vocab_size = len(cuneiform_vocab)

    cuneiform_embeddings_index = load_embedding_index('embeddings/0.11_loss_sumerian.vec')
    cuneiform_embedding_dims = len(cuneiform_embeddings_index['a'])

    cuneiform_embedding_matrix = build_embedding_matrix(
        embeddings_index=cuneiform_embeddings_index,
        dimensions=cuneiform_embedding_dims,
        word_index=cuneiform_word_index
    )

    sentence_pairs = pd.read_csv('language_pairs/' + language + '.tsv', sep='\t')

    number_sentence_pairs = len(sentence_pairs)
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
        max_len=max_engish_sentence_length,
        add_start_frag=True
    )

    decoder_target_data = np.zeros_like(decoder_input_data, dtype=float)

    for t in range(max_engish_sentence_length - 1):
        decoder_target_data[:, t] = decoder_input_data[:, t + 1]

    # TODO add </s> fragment ID at end of decoder_target_data sentences

    print(decoder_target_data.shape)
    decoder_target_data = decoder_target_data.reshape((number_sentence_pairs, max_engish_sentence_length, 1))
    print(decoder_target_data.shape)

    # Define an input sequence and process it.
    encoder_inputs = Input(shape=(None,))
    x = Embedding(
        cuneiform_vocab_size,
        cuneiform_embedding_dims,
        weights=[cuneiform_embedding_matrix],
        trainable=False
    )(encoder_inputs)

    x, state_h, state_c = LSTM(lstm_units, return_state=True)(x)
    encoder_states = [state_h, state_c]

    # Set up the decoder, using `encoder_states` as initial state.
    decoder_inputs = Input(shape=(None,))
    x = Embedding(english_vocab_size, english_embedding_dims)(decoder_inputs)
    decoder_lstm = LSTM(
        lstm_units,
        input_shape=(None, max_engish_sentence_length),
        return_sequences=True
    )(x, initial_state=encoder_states)

    decoder_dense = Dense(english_vocab_size, activation='softmax')

    decoder_outputs = decoder_dense(decoder_lstm)

    # Define the model that will turn
    # `encoder_input_data` & `decoder_input_data` into `decoder_target_data`
    model = keras.Model([encoder_inputs, decoder_inputs], decoder_outputs)

    # Compile & run training
    model.compile(optimizer='rmsprop', loss='sparse_categorical_crossentropy')

    print(model.summary())

    # Note that `decoder_target_data` needs to be one-hot encoded,
    # rather than sequences of integers like `decoder_input_data`!
    model.fit(
        [encoder_input_data, decoder_input_data],
        decoder_target_data,
        batch_size=batch_size,
        epochs=epochs,
        validation_split=0.2
    )

    model.save('first_model.model')

    # Performing inference

    encoder_model = keras.Model(encoder_inputs, encoder_states)

    decoder_state_input_h = Input(shape=(lstm_units,))
    decoder_state_input_c = Input(shape=(lstm_units,))

    decoder_states_inputs = [decoder_state_input_h, decoder_state_input_c]

    decoder_outputs, state_h, state_c = decoder_lstm(
        decoder_inputs,
        initial_state=decoder_states_inputs
    )

    decoder_states = [state_h, state_c]
    decoder_outputs = decoder_dense(decoder_outputs)

    decoder_model = keras.Model(
        [decoder_inputs] + decoder_states_inputs,
        [decoder_outputs] + decoder_states
    )

    def decode_sequence(input_seq):
        # TODO preprocess input into set length array of word fragment IDs

        # Encode the input as state vectors.
        states_value = encoder_model.predict(input_seq)

        # Generate empty target sequence of length 1.
        target_seq = np.zeros((1, 1))
        # Populate the first fragment of target sequence with the start character.
        target_seq[0, 0] = cuneiform_sp.EncodeAsIds('<s>')[0]

        # Sampling loop for a batch of sequences
        # (to simplify, here we assume a batch of size 1).
        stop_condition = False
        decoded_sentence = ''
        while not stop_condition:
            output_tokens, h, c = decoder_model.predict(
                [target_seq] + states_value)

            # Sample a token
            sampled_token_index = np.argmax(output_tokens[0, -1, :])
            sampled_fragment = english_sp.DecodeIds([sampled_token_index])
            decoded_sentence += sampled_fragment

            # Exit condition: either hit max length
            # or find stop character.
            if (sampled_fragment == '</s>' or
                    len(decoded_sentence) > max_engish_sentence_length):

                stop_condition = True

            # Update the target sequence (of length 1).
            target_seq = np.zeros((1, 1))
            target_seq[0, 0] = sampled_token_index

            # Update states
            states_value = [h, c]

        return decoded_sentence

    while True:
        sumerian_sentence = input('Enter Sumerian string to translate:')
        english_sentence = decode_sequence(sumerian_sentence)
        print(english_sentence)


if __name__ == '__main__':
    main()
