__author__ = 'matias'

from textanalysis.phrasedetection import PmiPhraseDetector
from textanalysis.texts import RawSentenceStream, PhraseSentenceStream
from textanalysis.pubmed_tokenize import RawTokenizer
from irmodels.W2Vmodel import W2Vmodel


class QueryExpansion(object):
    def expand(self, query):
        raise NotImplementedError()

    def __str__(self):
        raise NotImplementedError()


class AverageW2VExpansion(QueryExpansion):

    def __init__(self):
        self.name = "W2V Query Expansion"
        # phrase detector
        self.phrase_detector = PmiPhraseDetector(RawSentenceStream())
        # number converter
        self.tokenizer = RawTokenizer()
        # build model
        self.model = W2Vmodel(PhraseSentenceStream(self.phrase_detector))

    def expand(self, query):
        # parameters
        threshold = 0.7
        n = 10
        phrases = self.phrase_detector.detect(self.tokenizer.tokenize(query.lower()))
        w2v_phrases = [phrase for phrase in phrases if phrase in self.model]
        similar_phrases = self.model.inner_model.most_similar(w2v_phrases, [], topn=n)
        extra_terms = " ".join([phrase[0].replace('_', ' ') for phrase in similar_phrases if phrase[1] > threshold])
        return "%s %s" % (query, extra_terms, )

    def __str__(self):
        return self.__class__.__name__