import numpy as np
import pickle
import random

from tensorflow.keras.models import load_model
from nltk.stem import WordNetLemmatizer
import nltk 

from .settings import BASE_DIR

# On utilise le lemmatiseur pour reduire les mots à leur base
lemmatizer = WordNetLemmatizer()

# On charge les mots et les classes qui ont été enregistrés précédemment
words = pickle.load(open(f"{BASE_DIR}/words.pkl", "rb"))
classes = pickle.load(open(f"{BASE_DIR}/classes.pkl", "rb"))
model = load_model(f"{BASE_DIR}/chatbot_model.h5")


def clean_up_sentence(sentence):
    """
    Cette fonction permet de nettoyer une phrase en la divisant en mots
    et en les réduisant à leur base (lemmatisation).
    """
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words


def bow(sentence, words, show_details=True):
    """
    Cette fonction permet de créer un sac de mots (bag of words) à partir
    d'une phrase. Le sac de mots est une liste de 0 et de 1 où chaque élément
    correspond à un mot de la liste des mots connus. Si le mot est présent dans
    la phrase, la valeur est à 1, sinon elle est à 0.
    """
    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
    return(np.array(bag))


def predict_class(sentence, model):
    """
    Cette fonction permet de prédire la classe d'une phrase en utilisant
    le modèle de classification entraîné précédemment. La fonction renvoie
    une liste de dictionnaires où chaque dictionnaire contient l'intention
    et la probabilité associée.
    """
    p = bow(sentence, words, show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list


def get_response(ints, intents_json):
    """
    Cette fonction permet de récupérer une réponse aléatoire correspondant
    à l'intention trouvée par la fonction predict_class.
    """
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result
