__author__ = 'matias'

from gensim.models.phrases import Phrases, prune_vocab
import os
import logging

class PmiPhraseDetector(object):
    """
    Detection using Pointwise Mutual Information (PMI)
    """
    def __init__(self, sentences):
        # model parameters
        self.sentences = sentences
        self.dataset = "CASEREPORT"
        self.phrases = None
        self.threshold = 80
        self.decay = 0.5
        self.bigram_iter = 2

        # data file path
        models_folder = os.path.join(*[os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'models'])
        filename = "PHRASE_%s_%s" % (self.threshold, self.dataset, )
        self.filepath = os.path.join(models_folder, filename)

        # does identical model already exists?
        model_exists = os.path.isfile(self.filepath)
        if model_exists:
            logging.info("LOADING - loading phrase data")
            self.phrases = Phrases.load(self.filepath)

    def build(self):
        self.phrases = Phrases(self.sentences, min_count=1, threshold=self.threshold)
        # run additional merge rounds
        for i in range(2, self.bigram_iter + 1):
            self.phrases = Phrases(self.sentences, min_count=1, threshold=self.threshold*self.decay**(i-1))
        # save model to file
        self.phrases.save(self.filepath)

    def prune(self, min_reduce):
        prune_vocab(self.phrases.vocab, min_reduce)

    def detect(self, sentence):
        return self.phrases[sentence]

    def print_phrases(self, threshold=100):
        for word in self.phrases.vocab:
            if "_" in word and self.phrases.vocab[word] > threshold:
                print word, self.phrases.vocab[word]
