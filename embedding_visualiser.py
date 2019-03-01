import os

import numpy
import pandas as pd
import tensorflow as tf

from translation_trainer import load_embedding_index, build_word_index

cuneiform_vocab = pd.read_csv('sp_encodings/omni.vocab', sep='\t', header=None)
cuneiform_word_index = build_word_index(cuneiform_vocab)

cuneiform_embeddings_index = load_embedding_index('embeddings/0.11_loss_sumerian.vec')

cuneiform_embedding_matrix = numpy.zeros(shape=(len(cuneiform_embeddings_index), 100), dtype=float)
cuneiform_words = []
i = 0
for word, vector in cuneiform_embeddings_index.items():
    if word.strip('▁').isalpha():
        cuneiform_embedding_matrix[i][:] = vector
        cuneiform_words.append(word)

    i += 1

# filtered_embedding_matrix = numpy.zeros(shape=(len(cuneiform_words), 100), dtype=float)

filtered_embedding_matrix = cuneiform_embedding_matrix[0:len(cuneiform_words)][:]

# print(cuneiform_embedding_matrix)
# print(numpy.array(cuneiform_embedding_matrix))

# Create some variables.
emb = tf.Variable(numpy.array(filtered_embedding_matrix), name='word_embeddings')

# Add an op to initialize the variable.
init_op = tf.global_variables_initializer()

# Add ops to save and restore all the variables.
saver = tf.train.Saver()

# Later, launch the model, initialize the variables and save the
# variables to disk.
with tf.Session() as sess:
    sess.run(init_op)

    # Save the variables to disk.
    save_path = saver.save(sess, "embedding_vis/model.ckpt")
    print("Model saved in path: %s" % save_path)

words = '\n'.join(cuneiform_words)

with open(os.path.join('embedding_vis', 'embedding_labels.tsv'), 'w') as f:
    f.write(words)

# .tsv file written in embedding_vis/embedding_labels.tsv
