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

# SENTIMENT MAP
decode_map = {0: "NEGATIVE", 2: "NEUTRAL", 4: "POSITIVE"}

# TEXT CLENAING
TEXT_CLEANING_RE = "@\S+|https?:\S+|http?:\S|[^A-Za-z0-9]+"
SEQUENCE_LENGTH = 300
# EXPORT
KERAS_MODEL = "models/model.keras"
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
list_classes = ["NEGATIVE", "POSITIVE"]
encoded_labels = loaded_encoder.transform(list_classes)
print(
    f"- list_classes = {list_classes}\
      \n- encoded_labels = {encoded_labels}"
)

# load Word2Vec model
w2v_model = gensim.models.Word2Vec.load(WORD2VEC_MODEL)
nltk.download("stopwords")
stop_words = stopwords.words("english")
stemmer = SnowballStemmer("english")

# load LSTM classification model
loaded_clf_model = tf.keras.models.load_model(KERAS_MODEL)


def decode_sentiment(label):
    return decode_map[int(label)]


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


def predict(text, tokenizer, model, include_neutral=True):
    start_at = time.time()
    # clean and preprocess the input text
    text = (lambda x: preprocess(x))(text)

    # Tokenize text
    x_test = pad_sequences(tokenizer.texts_to_sequences([text]), maxlen=SEQUENCE_LENGTH)
    # Predict
    score = model.predict([x_test])[0]
    score = np.squeeze(score)
    # Decode sentiment
    label = decode_sentiment(score, include_neutral=include_neutral)

    # print the predictions
    print(f"\n- processed text : {text}")
    print(f"\n- predicted sentiment : {label} (score={100*score:.1f} %)")

    # get results
    result = {
        "label": label,
        "score": float(score),
        "elapsed_time": time.time() - start_at,
    }
    return result
