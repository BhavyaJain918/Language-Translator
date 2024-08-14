import nltk
from joblib import load
from nltk.corpus import stopwords
import keras._tf_keras.keras as keras
from nltk.stem import WordNetLemmatizer
from keras._tf_keras.keras.layers import ReLU , Softmax
from sklearn.feature_extraction.text import TfidfVectorizer

def bulid_model():
    model = keras.Sequential()

    model.add(keras.layers.Conv1D(filters = 20 , kernel_size = 6 , activation = ReLU() , strides = 2))
    model.add(keras.layers.AveragePooling1D(pool_size = 2))
    model.add(keras.layers.Flatten())
    model.add(keras.layers.Dense(units = 32 , activation = ReLU()))
    model.add(keras.layers.Dense(units = 64 , activation = ReLU()))
    model.add(keras.layers.Dense(units = 10 , activation = Softmax()))

    model.build(input_shape = (1 , 108973 , 1))
    model.load_weights("")     # Path of the weight file (.h5)

    return model


def predict_lang(sent):
    nltk.download('wordnet')
    nltk.download('stopwords')
    vectorizer = TfidfVectorizer()
    lemmatizer = WordNetLemmatizer()

    vectorizer = load("")     # Path of the vectorizer file (.joblib)
    languages = ['Dutch' , 'English' , 'French' , 'Indonesian' , 'Portuguese' , 'Romanian' , 'Russian' , 'Spanish' , 'Swedish' , 'Turkish']

    sent = sent.strip()
    sent = sent.lower()

    words_new = sent.split()
    words_new = [lemmatizer.lemmatize(word) for word in words_new if word not in set(stopwords.words())]
    words_new = " ".join(words_new)

    predict_word = vectorizer.transform([words_new])

    predict_word = predict_word.toarray()

    predict_word = predict_word.reshape((predict_word.shape[0] , predict_word.shape[1] , 1))

    models = bulid_model()
    predicted = models.predict(predict_word)

    class_max = predicted.max()
    index = list(predicted[0]).index(class_max)

    return ((languages)[index])

if __name__ == "__main__":
    print("Predicted Language : " , predict_lang("Hello I have come here to destroy you"))