__author__ = 'matias'

from nltk import word_tokenize

def tokenize(text):
    # remove MS Word curly quotes
    text = text.replace("\xe2\x80\x99", "'")
    return word_tokenize(text)