__author__ = 'matias'

from gensim.models.phrases import Phrases, prune_vocab
from pubmed_tokenize import stopwords
import os
import logging


class PmiPhraseDetector(object):
    """
    Detection using Pointwise Mutual Information (PMI)
    """
    def __init__(self, sentences, filename=None):

        # model parameters
        self.sentences = sentences
        self.dataset = "CASEREPORT"
        self.tokenizer = "RAW"
        self.prune_stopwords = stopwords("pubmed")
        self.phrases = None
        self.threshold = 250
        self.decay = 2
        self.bigram_iter = 3

        # data file path
        models_folder = os.path.join(*[os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'models'])
        if filename is None:
            filename = "PHRASE_%s_%s_%s_%s" % (self.threshold, self.decay, self.dataset, self.tokenizer, )
        self.filepath = os.path.join(models_folder, filename)

        # does identical model already exists?
        model_exists = os.path.isfile(self.filepath)
        if model_exists:
            logging.info("LOADING - loading phrase data..")
            self.phrases = Phrases.load(self.filepath)
        else:
            logging.info("CREATE - creating phrase data..")
            self.build()

    def build(self):
        self.phrases = Phrases(self.sentences, min_count=1, threshold=self.threshold)
        # run additional merge rounds
        for i in range(2, self.bigram_iter + 1):
            self.phrases = Phrases(self.sentences, min_count=1, threshold=self.threshold*(1.0/self.decay)**(i-1))
        # prune phrases
        self.prune()
        # save model to file
        self.save()

    def save(self):
        self.phrases.save(self.filepath)

    def prune(self, min_reduce=1):
        """
        Remove phrases beginning or ending with a stopword.
        Also removes phrases appearing less frequently than a threshold.
        :param min_reduce: frequency threshold
        """
        multiword_phrases = [phrase for phrase in self.phrases.vocab if "_" in phrase]
        for phrase in multiword_phrases:
            words = phrase.split("_")
            first_word, last_word = words[0], words[-1]
            if first_word in self.prune_stopwords or last_word in self.prune_stopwords:
                del self.phrases.vocab[phrase]

        prune_vocab(self.phrases.vocab, min_reduce)

    def detect(self, sentence):
        return self.phrases[sentence]

    def print_phrases(self, threshold=100):
        for word in self.phrases.vocab:
            if "_" in word and self.phrases.vocab[word] > threshold:
                print word, self.phrases.vocab[word]
