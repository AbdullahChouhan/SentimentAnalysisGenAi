print("Abdullah Chouhan: Assignment 4\n\nImporting modules...")

try:
    import numpy as np
    import tensorflow as tf
    import keras
    import tensorflow_datasets as tfds

    if not tf.__version__.startswith('2'):
        raise ValueError('This code requires TensorFlow V2.x')
except ModuleNotFoundError as e:
    print(f"Couldn't import modules: {e}")
    exit(1)
print("Modules imported successfully")

# Loading the IMDB dataset
(train_data, test_data), _ = tfds.load(
    'imdb_reviews',
    split=[tfds.Split.TRAIN, tfds.Split.TEST],
    as_supervised=True,
    shuffle_files=True,
    with_info=True
)

# Tokenizing and padding the data
tokenizer = keras.preprocessing.text.Tokenizer(num_words=10000, oov_token='<OOV>')
train_sentences, train_labels = zip(*[(sent.numpy().decode('utf8'), label.numpy()) for sent, label in train_data])
tokenizer.fit_on_texts(train_sentences)
train_sequences = tokenizer.texts_to_sequences(train_sentences)
train_padded = keras.preprocessing.sequence.pad_sequences(train_sequences, maxlen=100, padding='post', truncating='post')

test_sentences, test_labels = zip(*[(sent.numpy().decode('utf8'), label.numpy()) for sent, label in test_data])
test_sequences = tokenizer.texts_to_sequences(test_sentences)
test_padded = keras.preprocessing.sequence.pad_sequences(test_sequences, maxlen=100, padding='post', truncating='post')

train_labels = np.array(train_labels)
test_labels = np.array(test_labels)

print(f"\nTrain data: {train_padded.shape}, {train_labels.shape}\nTest data: {test_padded.shape}, {test_labels.shape}")

# Building a RNN model
print(f"\nBuilding a RNN model...")
model = keras.Sequential([
    keras.layers.Embedding(10000, 32),
    keras.layers.Dropout(0.5),
    keras.layers.SimpleRNN(32, kernel_regularizer=keras.regularizers.l2(0.001)),
    keras.layers.Dense(1, activation='sigmoid')
])

model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])
early_stop = keras.callbacks.EarlyStopping(monitor='val_loss', patience=3)
history = model.fit(train_padded, train_labels, epochs=10, validation_data=(test_padded, test_labels), callbacks=[early_stop])

print(history.history.keys())
print(f"\nTraining accuracy: {history.history['accuracy'][-1]}\nValidation accuracy: {history.history['val_accuracy'][-1]}")
RNNscore = model.evaluate(test_padded, test_labels)
print(f"Score: {RNNscore}")

del model, history

# Buiding a LSTM model

print(f"\nBuilding a LSTM model...")
try:
    from keras.layers import Bidirectional, LSTM
except ModuleNotFoundError as e:
    print(f"Couldn't import modules: {e}")
    exit(1)

model = keras.models.Sequential([
    keras.layers.Embedding(10000, 32),
    Bidirectional(LSTM(32, dropout=0.5, recurrent_dropout=0.5, kernel_regularizer=keras.regularizers.l2(0.001))),
    keras.layers.Dense(1, activation='sigmoid')
])

model.compile(loss="binary_crossentropy", optimizer=keras.optimizers.Adam(learning_rate=0.001), metrics=["accuracy"])
early_stop = keras.callbacks.EarlyStopping(monitor='val_loss', patience=3)
history = model.fit(train_padded, train_labels, epochs=10, validation_data=(test_padded, test_labels), callbacks=[early_stop])

print(history.history.keys())
print(f"\nTraining accuracy: {history.history['accuracy'][-1]}\nValidation accuracy: {history.history['val_accuracy'][-1]}")
LSTMscore = model.evaluate(test_padded, test_labels)
print(f"Score: {LSTMscore}")

del model, history

# Building a CNN model

print("\nBuilding a CNN model...")
try:
    from keras.layers import Conv1D, MaxPooling1D
except ModuleNotFoundError as e:
    print(f"Couldn't import modules: {e}")
    exit(1)

model = keras.Sequential([
    keras.layers.Embedding(10000, 32),
    Conv1D(32, 7, activation='relu'),
    MaxPooling1D(5),
    Bidirectional(LSTM(32, return_sequences=True, dropout=0.5, recurrent_dropout=0.5, kernel_regularizer=keras.regularizers.l2(0.001))),
    Bidirectional(LSTM(32, dropout=0.5, recurrent_dropout=0.5, kernel_regularizer=keras.regularizers.l2(0.001))),
    keras.layers.Dense(1, activation='sigmoid')
])

model.compile(loss="binary_crossentropy", optimizer=keras.optimizers.RMSprop(learning_rate=0.001), metrics=["accuracy"])
early_stop = keras.callbacks.EarlyStopping(monitor='val_loss', patience=3)
checkpoint = keras.callbacks.ModelCheckpoint("best_model.h5", save_best_only=True)
history = model.fit(train_padded, train_labels, epochs=10, validation_data=(test_padded, test_labels), callbacks=[early_stop, checkpoint])

print(history.history.keys())
print(f"\nTraining accuracy: {history.history['accuracy'][-1]}\nValidation accuracy: {history.history['val_accuracy'][-1]}")
CNNscore = model.evaluate(test_padded, test_labels)
print(f"Score: {CNNscore}")

print(f"RNN score: {RNNscore}\nLSTM score: {LSTMscore}\nCNN score: {CNNscore}")