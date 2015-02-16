__author__ = 'matias'

from nltk import word_tokenize

def tokenize(text):
    # remove MS Word curly quotes
    text.replace("’","'")
    return word_tokenize(text)