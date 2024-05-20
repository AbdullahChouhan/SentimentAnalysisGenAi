try:    
    import numpy as np
    import tensorflow as tf
    from tensorflow import keras
    import tensorflow_datasets as tfds
    from keras.layers import Bidirectional, LSTM, Conv1D, MaxPooling1D
except ModuleNotFoundError as e:
    print(f"Couldn't import modules: {e}")
    exit(1)

if not tf.__version__.startswith('2'):
    raise ValueError('This code requires TensorFlow V2.x')

class AI:
    """
    The AI class is responsible for loading and processing the IMDb dataset
    and building various neural network models for text classification using TensorFlow and Keras.
    """
    def __init__(self):
        """
        Initializes the object by calling the `load_imdb_data` method.

        This method is called when an instance of the class is created. It loads the IMDB dataset for sentiment analysis.
        """
        self.model = None
        self.load_imdb_data()

    def load_imdb_data(self):
        """
        Loads the IMDB dataset for sentiment analysis.

        This function loads the IMDB dataset, which contains reviews of movies
        labeled as positive or negative. The dataset is split into training and
        testing sets. The function then tokenizes and pads the training and
        testing data.
        """
        (train_data, test_data), _ = tfds.load(
            'imdb_reviews',
            split=[tfds.Split.TRAIN, tfds.Split.TEST],
            as_supervised=True,
            shuffle_files=True,
            with_info=True
        )

        self._tokenize_and_pad_data(train_data, test_data)

    def _tokenize_and_pad_data(self, train_data, test_data):
        """
        Tokenizes and pads the training and testing data.

        Parameters:
        - train_data (list): A list of tuples containing the training sentences and labels.
        - test_data (list): A list of tuples containing the testing sentences and labels.
        
        Uses Tokenizer from Keras to fit on the training sentences.
        Converts sentences to sequences and pads them to a maximum length of 100.
        Stores the padded sequences and labels as instance variables (self.train_padded, self.test_padded, self.train_labels, self.test_labels).
        """
        self.tokenizer = keras.preprocessing.text.Tokenizer(num_words=10000, oov_token='<OOV>')
        train_sentences, train_labels = zip(*[(sent.numpy().decode('utf8'), label.numpy()) for sent, label in train_data])
        self.tokenizer.fit_on_texts(train_sentences)
        train_sequences = self.tokenizer.texts_to_sequences(train_sentences)
        self.train_padded = keras.preprocessing.sequence.pad_sequences(train_sequences, maxlen=100, padding='post', truncating='post')

        test_sentences, test_labels = zip(*[(sent.numpy().decode('utf8'), label.numpy()) for sent, label in test_data])
        test_sequences = self.tokenizer.texts_to_sequences(test_sentences)
        self.test_padded = keras.preprocessing.sequence.pad_sequences(test_sequences, maxlen=100, padding='post', truncating='post')

        self.train_labels = np.array(train_labels)
        self.test_labels = np.array(test_labels)

    def buildRNN_model(self):
        """
        Builds a simple RNN model for binary classification.

        Returns:
        - model (keras.Sequential): The compiled RNN model.

        The function creates a sequential model with the following layers:
        - Embedding layer: Maps the input sequences to dense vectors of size 32.
        - Dropout layer: Applies dropout regularization to prevent overfitting.
        - SimpleRNN layer: Applies a simple RNN with 32 units and L2 regularization.
        - Dense layer: Applies a dense layer with a single unit and sigmoid activation function.

        The model is compiled with binary cross-entropy loss, Adam optimizer, and accuracy metric.
        The model is trained for 10 epochs with early stopping based on the validation loss.
        The trained model is returned.
        """
        model = keras.Sequential([
            keras.layers.Embedding(10000, 32),
            keras.layers.Dropout(0.5),
            keras.layers.SimpleRNN(32, kernel_regularizer=keras.regularizers.l2(0.001)),
            keras.layers.Dense(1, activation='sigmoid')
        ])

        model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])
        early_stop = keras.callbacks.EarlyStopping(monitor='val_loss', patience=3)
        model.fit(self.train_padded, self.train_labels, epochs=10, validation_data=(self.test_padded, self.test_labels), callbacks=[early_stop])
        self.model = model

    def buildLSTM_model(self):
        """
        Builds an LSTM model for binary classification.

        Returns:
        - model (keras.Sequential): The compiled LSTM model.

        The function creates a sequential model with the following layers:
        - Embedding layer: Maps the input sequences to dense vectors of size 32.
        - Bidirectional LSTM layer: Applies a bidirectional LSTM with 32 units and dropout regularization.
        - Dense layer: Applies a dense layer with a single unit and sigmoid activation function.

        The model is compiled with binary cross-entropy loss, Adam optimizer, and accuracy metric.
        The model is trained for 10 epochs with early stopping based on the validation loss.
        The trained model is returned.
        """
        model = keras.models.Sequential([
            keras.layers.Embedding(10000, 32),
            Bidirectional(LSTM(32, dropout=0.5, recurrent_dropout=0.5, kernel_regularizer=keras.regularizers.l2(0.001))),
            keras.layers.Dense(1, activation='sigmoid')
        ])

        model.compile(loss="binary_crossentropy", optimizer=keras.optimizers.Adam(learning_rate=0.001), metrics=["accuracy"])
        early_stop = keras.callbacks.EarlyStopping(monitor='val_loss', patience=3)
        model.fit(self.train_padded, self.train_labels, epochs=10, validation_data=(self.test_padded, self.test_labels), callbacks=[early_stop])
        self.model = model

    def buildCNN_model(self):
        """
        Builds a CNN model for binary classification.

        Returns:
        - model (keras.Sequential): The compiled CNN model.

        The function creates a sequential model with the following layers:
        - Embedding layer: Maps the input sequences to dense vectors of size 32.
        - Conv1D layer: Applies a 1D convolution with 32 filters and a kernel size of 7, with ReLU activation.
        - MaxPooling1D layer: Applies max pooling with a pool size of 5.
        - Bidirectional LSTM layer: Applies a bidirectional LSTM with 32 units and dropout regularization.
        - Bidirectional LSTM layer: Applies another bidirectional LSTM with 32 units and dropout regularization.
        - Dense layer: Applies a dense layer with a single unit and sigmoid activation function.

        The model is compiled with binary cross-entropy loss, RMSprop optimizer, and accuracy metric.
        The model is trained for 10 epochs with early stopping based on the validation loss.
        The trained model is saved to "best_model.h5" if it achieves the best validation loss.
        The trained model is returned.
        """
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
        model.fit(self.train_padded, self.train_labels, epochs=10, validation_data=(self.test_padded, self.test_labels), callbacks=[early_stop, checkpoint])
        self.model = model
        
    def analyze(self, text):
        """
        Analyzes the input text and returns the predicted sentiment.

        Parameters:
        - text (str): The input text to analyze.

        Returns:
        - sentiment (str): The predicted sentiment of the input text.

        The function uses the trained model to predict the sentiment of the input text.
        The predicted sentiment is returned as a string.
        """
        if not self.tokenizer:
            raise Exception("Tokenizer not initialized. Please call _tokenize_and_pad_data() first.")
        sequences = self.tokenizer.texts_to_sequences([text])
        padded = keras.preprocessing.sequence.pad_sequences(sequences, maxlen=100, padding='post', truncating='post')
        if not self.model:
            raise Exception("Model not initialized. Please call build() or buildCNN_model() first.")
        sentiment = "Positive" if self.model.predict(padded)[0][0] > 0.5 else "Negative"
        return sentiment