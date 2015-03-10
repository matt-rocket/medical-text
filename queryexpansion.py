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
        # phrase detector
        self.phrase_detector = PmiPhraseDetector(RawSentenceStream())
        # number converter
        self.tokenizer = RawTokenizer()
        # build model
        self.model = W2Vmodel(PhraseSentenceStream(self.phrase_detector))
        # parameters
        self.p = 0.7
        self.n = 10

    def expand(self, query):
        phrases = self.phrase_detector.detect(self.tokenizer.tokenize(query.lower()))
        w2v_phrases = [phrase for phrase in phrases if phrase in self.model]
        similar_phrases = self.model.inner_model.most_similar(w2v_phrases, [], topn=self.n)
        extra_terms = " ".join([phrase[0].replace('_', ' ') for phrase in similar_phrases if phrase[1] > self.p])
        return "%s %s" % (query, extra_terms, )

    def __str__(self):
        return self.__class__.__name__


class TermwiseW2VExpansion(QueryExpansion):

    def __init__(self):
        # phrase detector
        self.phrase_detector = PmiPhraseDetector(RawSentenceStream())
        # number converter
        self.tokenizer = RawTokenizer()
        # build model
        self.model = W2Vmodel(PhraseSentenceStream(self.phrase_detector))
        # parameters
        self.p = 0.7
        self.n = 10

    def expand(self, query):
        phrases = self.phrase_detector.detect(self.tokenizer.tokenize(query.lower()))
        w2v_phrases = [phrase for phrase in phrases if phrase in self.model]
        translated_phrases = []
        for term in w2v_phrases:
            closest_term = self.model.inner_model.most_similar([term], [], topn=self.n)[0][0]
            translated_phrases.append(closest_term)
        extra_terms = " ".join(translated_phrases)
        return "%s %s" % (query, extra_terms, )

    def __str__(self):
        return self.__class__.__name__