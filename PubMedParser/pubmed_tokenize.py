__author__ = 'matias'

from nltk import word_tokenize
import os

def tokenize(text):
    if text is None:
        return []
    text = text.replace("\n", " ")
    return word_tokenize(text)

def stopwords(listname):
    filepath = os.path.join(*[os.path.dirname(__file__), 'data', listname+"_stopwords.txt"])
    stopword_list = open(filepath,'r').read().split("\n")
    return set(stopword_list)

