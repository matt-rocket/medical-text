__author__ = 'matias'

from nltk import word_tokenize
import os


def tokenize(text):
    if text is None:
        return []
    text = text.replace("\n", " ").replace("."," ")
    return word_tokenize(text)


def stopwords(listname):
    filepath = os.path.join(*[os.path.dirname(__file__), 'data', 'stopwordlists', listname+"_stopwords.txt"])
    stopword_list = open(filepath,'r').read().split("\n")
    return set(stopword_list)


class Num2TokenConverter(object):
    def __init__(self):
        self.number_words = stopwords("numbers")

    def convert(self,tokens):
        converted_tokens = []
        for token in tokens:
            if token.isdigit() or token in self.number_words:
                converted_tokens.append("[number]")
            else:
                converted_tokens.append(token)
        return converted_tokens
