__author__ = 'matias'

from textanalysis.phrasedetection import PmiPhraseDetector
from textanalysis.texts import RawSentenceStream, PhraseSentenceStream
from textanalysis.pubmed_tokenize import RawTokenizer, tokenize
from irmodels.W2Vmodel import W2Vmodel
from irmodels.TFIDFmodel import TFIDFmodel
from irmodels.LDAmodel import LDAmodel


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
            similar_phrases = self.model.inner_model.most_similar_cosmul(phrase,topn=self.k)
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
        query_strings = [" ".join(q) for q in translated_queries]

        combined_query = query + "." + ".".join(query_strings)
        return combined_query

    def __str__(self):
        return self.__class__.__name__


class WeightedW2VExpansion(QueryExpansion):

    def __init__(self):
        # phrase detector
        self.phrase_detector = PmiPhraseDetector(RawSentenceStream())
        # number converter
        self.tokenizer = RawTokenizer()
        # build model
        self.w2v = W2Vmodel(PhraseSentenceStream(self.phrase_detector))
        self.tfidf = TFIDFmodel()
        # parameters
        self.alpha = 6.0
        self.k = 3
        self.p = 0.80

    def expand(self, query):
        phrases = self.phrase_detector.detect(self.tokenizer.tokenize(query.lower()))
        w2v_phrases = [phrase for phrase in phrases if phrase in self.w2v]
        extra_terms = []
        for phrase in w2v_phrases:
            idf = 0.0
            if phrase in self.tfidf.dictionary.token2id:
                idf = self.tfidf.inner_model.idfs[self.tfidf.dictionary.token2id[phrase]]
            expansion = []
            if idf > self.alpha:
                expansion = self.w2v.inner_model.most_similar_cosmul(positive=[phrase], topn=self.k)
            # print phrase, idf, " ".join([e[0] for e in expansion])
            extra_terms += [e[0] for e in expansion]
        new_query = query + " " + " ".join(extra_terms)
        return new_query

    def __str__(self):
        return self.__class__.__name__


class LDAExpansion(QueryExpansion):

    def __init__(self):
        # build model
        self.lda = LDAmodel(n_topics=100, n_passes=10, vocabulary='combined')
        # parameters
        self.k = 10

    def expand(self, query):
        tokens = tokenize(query.lower())
        latent = self.lda.tokens2latent(tokens)
        extra_terms = []
        for topic in latent:
            topn = self.lda.model.show_topic(topicid=topic[0], topn=round(self.k*topic[1]))
            extra_terms += [e[1] for e in topn]
        extra_terms = list(set(extra_terms))
        new_query = query + " " + " ".join(extra_terms)
        return new_query

    def __str__(self):
        return self.__class__.__name__


if __name__ == "__main__":
    qe = LDAExpansion()
    print qe.expand("4 month old, boy, epistaxis, haematemesis, haematochezia, subconjunctival bleeding, petechiae, haematomas, haemangioma, slightly enlarged liver, elevated serum transaminases")