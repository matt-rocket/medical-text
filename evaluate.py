__author__ = 'matias'

from search import StandardSolrEngine
from queryexpansion import AverageW2VExpansion, TermWindowW2VExpansion, TermwiseW2VExpansion
from evaluation.metrics import *
import logging


def evaluate(search_engine, k, verbose=False):
    with open('evaluation/data/findzebra.tsv','r') as infile:
        records = infile.read().split("\n")

        query_results = []

        recalls = []
        precisions = []

        for record in records:
            qid, query, answer, relevant, partly_relevant = record.split("\t")
            correct_answers = [ans for ans in relevant.split(",") + partly_relevant.split(",") if ans is not '']
            response = search_engine.query(query, top_n=k)
            returned_docids = [hit[u'id'] for hit in response.results]
            recalls.append(recall(correct_answers, returned_docids))
            precisions.append(precision(correct_answers, returned_docids))
            if verbose:
                print query
                print "P@%s" % (k,), precision(correct_answers, returned_docids)
                print "R@%s" % (k,), recall(correct_answers, returned_docids)
                print "F@%s" % (k,), f_measure(correct_answers, returned_docids)
                print "Relevant@%s" % (k,), relevant_at_k(correct_answers, returned_docids)
            query_results.append((correct_answers, returned_docids))

        print str(search_engine)
        print "MAP", mean_average_precision(query_results)
        print "MRR", mean_reciprocal_rank(query_results)
        print "Avg. R@k", sum(recalls)/float(len(recalls))
        print "Avg. P@k", sum(precisions)/float(len(precisions))
        print recalls

if __name__ == "__main__":
    # setup logging
    # logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    # retrieval top k ranked
    k = 20
    search_engines = [
        StandardSolrEngine(),
        StandardSolrEngine(query_expansion=AverageW2VExpansion()),
        StandardSolrEngine(query_expansion=TermwiseW2VExpansion()),
        StandardSolrEngine(query_expansion=TermWindowW2VExpansion()),
        ]

    for engine in search_engines:
        evaluate(engine, k, verbose=False)