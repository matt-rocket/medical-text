__author__ = 'matias'

import solr
from textanalysis.texts import RawSentenceStream, PhraseSentenceStream, FZArticleLibrary, extract_docid
from textanalysis.phrasedetection import PmiPhraseDetector
from irmodels.D2Vmodel import D2Vmodel, DocIndex
from nltk.tokenize import sent_tokenize, word_tokenize
from scipy.spatial.distance import cosine
from heapq import heappush



class SearchEngine(object):
    def __str__(self):
        raise NotImplementedError()

    def query(self, query_str, top_n=20):
        raise NotImplementedError()


class StandardSolrEngine(SearchEngine):
    def __init__(self, query_expansion=None):
        self.solr_con = solr.SolrConnection('http://localhost:8983/solr')
        self.name = "Standard Solr Engine"
        self.query_expansion = query_expansion

    def __str__(self):
        if self.query_expansion is not None:
            string = "%s with %s" % (self.name, self.query_expansion,)
        else:
            string = self.name
        return string

    def query(self, query_str, top_n=20):
        # expand query
        if self.query_expansion is not None:
            query_str = self.query_expansion.expand(query_str)
        # remove special Solr query chars
        query_str = query_str.replace(":", "")
        return self.solr_con.query(query_str, rows=top_n)


class TwoPhaseSearchEngine(SearchEngine):

    def __init__(self, inner_engine, top_ranker):
        self.inner_engine = inner_engine
        self.top_ranker = top_ranker

    def __str__(self):
        return "2-phase Search Engine"

    def query(self, query_str, top_n=20):
        pass


class Doc2VecSearchEngine(SearchEngine):

    def __init__(self):
        self.phrase_detector = PmiPhraseDetector(RawSentenceStream(fz_docs=False))
        # build model
        epochs = 10
        self.model = D2Vmodel(
            PhraseSentenceStream(self.phrase_detector, extract_func=extract_docid, fz_docs=True, reshuffles=epochs-1),
            name="DOCID",
            dataset_name="FINDZEBRA",
            epochs=epochs)
        self.doc_index = DocIndex(FZArticleLibrary(), "FINDZEBRA")

    def __str__(self):
        return "Doc2Vec Search Engine"

    def query(self, query_str, top_n=20):
        text = query_str.lower()
        tokens = []
        for sent in sent_tokenize(text):
            tokens += word_tokenize(sent)
        phrases = self.phrase_detector.detect(tokens)
        query_vec = self.model.inner_model.infer_vector(phrases, steps=100)

        ranking = []

        for word in self.model.inner_model.vocab:
            if word.startswith("DOCID-FZ"):
                doc_vec = self.model.inner_model[word]
                distance = cosine(query_vec, doc_vec)
                heappush(ranking, (distance, word))

        return ranking[:top_n]




if __name__ == "__main__":
    engine = StandardSolrEngine()
    engine.solr_con
    query_input = raw_input("search for:")
    while query_input is not "":
        hits = engine.query(query_input, 50).results
        relevant = []
        partly_relevant = []
        print "--------- RESULTS ---------"
        for hit in hits:
            relevance_input = ""
            while not relevance_input.isdigit():
                relevance_input = raw_input(
                    str(hit[u'id']) + " " + str(hit[u'title']) +
                    " (0=not relevant, 1=partly relevant, 2=relevant) Rating:")
            if relevance_input == "1":
                partly_relevant.append(hit[u'id'])
            elif relevance_input == "2":
                relevant.append(hit[u'id'])
        print "---------------------------"
        print "Relevant:  ", ",".join(relevant)
        print "Partly Relevant:  ", ",".join(partly_relevant)
        print ""
        query_input = raw_input("search for:")
