import pickle
import re
import time

import gensim
import nltk
import numpy as np
import tensorflow as tf
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# TEXT CLEANING
TEXT_CLEANING_RE = "@\S+|https?:\S+|http?:\S|[^A-Za-z0-9]+"
SEQUENCE_LENGTH = 300
# EXPORT
KERAS_MODEL = "models/my_model.keras"
WORD2VEC_MODEL = "models/model.w2v"
TOKENIZER_MODEL = "models/tokenizer.pkl"
ENCODER_MODEL = "models/encoder.pkl"

# Load tokenizer from the pickle file
with open(TOKENIZER_MODEL, "rb") as file:
    loaded_tokenizer = pickle.load(file)

# Test loaded tokenizer
text = "Hello"
tokenized_text = loaded_tokenizer.texts_to_sequences(text)
print(tokenized_text)


# Load tokenizer from the pickle file
with open(ENCODER_MODEL, "rb") as file:
    loaded_encoder = pickle.load(file)

# Test loaded tokenizer
example_labels = [k for k in range(len(loaded_encoder.classes_))]
encoded_labels = loaded_encoder.inverse_transform(example_labels)

assert set(loaded_encoder.classes_) == set(encoded_labels)
# print(
#     f"- example_labels = {example_labels}\
#       \n- encoded_classes = {encoded_labels}"
# )

# load Word2Vec model
w2v_model = gensim.models.Word2Vec.load(WORD2VEC_MODEL)
nltk.download("stopwords")
stop_words = stopwords.words("english")
stemmer = SnowballStemmer("english")

# load LSTM classification model
loaded_clf_model = tf.keras.models.load_model(KERAS_MODEL)


def decode_sentiment(score):
    # get the label with 0.5 threshold
    label = 0 if score < 0.5 else 1

    # get the class name from the label
    # print(f"- score={score}, label={label}")
    encoded_labels = loaded_encoder.inverse_transform([label])
    return encoded_labels


def preprocess(text, stem=False):
    # Remove link,user and special characters
    text = re.sub(TEXT_CLEANING_RE, " ", str(text).lower()).strip()
    tokens = []
    for token in text.split():
        if token not in stop_words:
            if stem:
                tokens.append(stemmer.stem(token))
            else:
                tokens.append(token)
    return " ".join(tokens)


def predict_text_sentiment(text, tokenizer, model, verbose=0):
    start_at = time.time()
    # clean and preprocess the input text
    text = (lambda x: preprocess(x))(text)

    # Tokenize text
    x_test = pad_sequences(tokenizer.texts_to_sequences([text]), maxlen=SEQUENCE_LENGTH)
    # Predict
    score = model.predict([x_test])[0]
    score = np.squeeze(score)

    # Decode sentiment
    label = decode_sentiment(score)

    # print the predictions
    prediction_msg = f"{label} (score={100*score:.1f} %)"

    if verbose > 0:
        print(f"\n- processed text : {text}")
        print(f"Predicted sentiment:{prediction_msg}")

    # get results
    result = {
        "label": label,
        "score": float(score),
        "elapsed_time": time.time() - start_at,
    }
    return text, result, prediction_msg


if __name__ == "__main__":
    # run the prediction
    text, prediction = predict_text_sentiment(
        text="I love the latest @RoKy music",
        tokenizer=loaded_tokenizer,
        model=loaded_clf_model,
        verbose=1,
    )

    cprediction = predict_text_sentiment(
        text="I hate the rain",
        tokenizer=loaded_tokenizer,
        model=loaded_clf_model,
        verbose=1,
    )
