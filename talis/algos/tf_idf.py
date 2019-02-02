import nltk
import numpy as np
import random
import string

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class TFIDF(object):

    def __init__(self):
        nltk.download('punkt')
        nltk.download('wordnet')
        self.raw_data = ""
        self.sent_tokens = []
        self.word_tokens = []
        self.lemmer = nltk.stem.WordNetLemmatizer()
        self.remove_punct_dict = dict(
            (ord(punct), None) for punct in string.punctuation
        )
        self.ai_response = None

    def set_data(self, raw_data):
        self.raw_data = raw_data.replace("\n", " ").lower()
        # do better parsing of data
        self.sent_tokens = nltk.sent_tokenize(self.raw_data)
        self.word_tokens = nltk.word_tokenize(self.raw_data)

    def LemTokens(self, tokens):
        return [self.lemmer.lemmatize(token) for token in tokens]

    def LemNormalize(self, text):
        return self.LemTokens(
            nltk.word_tokenize(text.translate(self.remove_punct_dict))
        )

    def answer(self, input_text):
        self.sent_tokens.append(input_text.lower())
        TfidfVec = TfidfVectorizer(
            tokenizer=self.LemNormalize,
            stop_words='english'
        )
        tfidf = TfidfVec.fit_transform(self.sent_tokens)
        vals = cosine_similarity(tfidf[-1], tfidf)
        idx = vals.argsort()[0][-2]
        flat = vals.flatten()
        flat.sort()
        req_tfidf = flat[-2]
        if(req_tfidf == 0):
            self.ai_response = "I'm sorry, I don't know the answer."
        else:
            self.ai_response = self.sent_tokens[idx]
        self.sent_tokens.remove(input_text.lower())
        return self.ai_response