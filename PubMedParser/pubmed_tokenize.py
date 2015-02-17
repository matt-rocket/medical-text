__author__ = 'matias'

from nltk import word_tokenize

def tokenize(text):
    if text is None:
        return []
    # TODO: remove MS Word curly quotes
    #text = unicode(text).encode('utf-8').decode('ascii','ignore')
    text = text.replace("\n"," ")
    return word_tokenize(text)