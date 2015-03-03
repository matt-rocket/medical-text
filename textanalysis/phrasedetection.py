__author__ = 'matias'

from textanalysis.texts import SentenceStream
from gensim.models.phrases import Phrases, prune_vocab


class PmiPhraseDetector(object):
    """
    Detection using Pointwise Mutual Information (PMI)
    """
    def __init__(self):
        self.sentences = SentenceStream()
        self.phrases = None

    def build(self):
        self.phrases = Phrases(self.sentences, min_count=1, threshold=80.0)
        self.phrases = Phrases(self.phrases[self.sentences], min_count=1, threshold=20.0)

    def prune(self, min_reduce):
        prune_vocab(self.phrases.vocab, min_reduce)

    def detect(self, sentence):
        pass

    def print_phrases(self, threshold=100):
        for word in self.phrases.vocab:
            if "_" in word and self.phrases.vocab[word] > threshold:
                print word, self.phrases.vocab[word]
