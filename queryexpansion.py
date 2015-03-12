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
        self.k = 10

    def expand(self, query):
        phrases = self.phrase_detector.detect(self.tokenizer.tokenize(query.lower()))
        w2v_phrases = [phrase for phrase in phrases if phrase in self.model]
        translated_queries = [[] for i in range(self.k)]
        for phrase in w2v_phrases:
            similar_phrases = self.model.inner_model.most_similar(phrase,topn=self.k)
            for i in range(self.k):
                translated_queries[i-1].append(similar_phrases[i-1][0])
        query_strings = [" ".join(query) for query in translated_queries]
        combined_query = ".".join(query_strings)
        return combined_query

    def __str__(self):
        return self.__class__.__name__


class TermWindowW2VExpansion(QueryExpansion):

    def __init__(self):
        # phrase detector
        self.phrase_detector = PmiPhraseDetector(RawSentenceStream())
        # number converter
        self.tokenizer = RawTokenizer()
        # build model
        self.model = W2Vmodel(PhraseSentenceStream(self.phrase_detector))
        # parameters
        self.p = 0.8
        self.k = 10

    def expand(self, query):
        phrases = self.phrase_detector.detect(self.tokenizer.tokenize(query.lower()))
        w2v_phrases = [phrase for phrase in phrases if phrase in self.model]
        translated_queries = [[] for i in range(self.k)]
        for idx, phrase in enumerate(w2v_phrases):
            # get adjacent terms
            prev_phrase = w2v_phrases[idx-1] if idx != 0 else u""
            next_phrase = w2v_phrases[idx+1] if idx != len(w2v_phrases)-1 else u""
            window = [e for e in [prev_phrase, phrase, next_phrase] if len(e) > 0]
            similar_phrases = self.model.inner_model.most_similar(window, topn=self.k)
            for i in range(self.k):
                translated_queries[i-1].append(similar_phrases[i-1][0])
        query_strings = [" ".join(query) for query in translated_queries]
        combined_query = ".".join(query_strings)
        return combined_query

    def __str__(self):
        return self.__class__.__name__




if __name__ == "__main__":
    qe = TermWindowW2VExpansion()
    for i in range(8):
        print qe.expand(u"bone cancer, hypertension in shoulders")