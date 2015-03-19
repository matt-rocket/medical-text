__author__ = 'matias'

from search import StandardSolrEngine
from queryexpansion import *
from evaluation.metrics import *
import logging


def evaluate(search_engine, k, verbose=False):
    with open('evaluation/data/findzebra.tsv','r') as infile:

        records = infile.read().split("\n")

        query_results = []

        recalls = []
        precisions = []
        ndcgs = []

        for record in records:
            qid, query, answer, relevant, partly_relevant = record.split("\t")
            correct_answers = [ans for ans in relevant.split(",") + partly_relevant.split(",") if ans is not '']
            response = search_engine.query(query, top_n=k)
            returned_docids = [hit[u'id'] for hit in response.results]
            r = recall(correct_answers, returned_docids)
            recalls.append(r)
            p = precision(correct_answers, returned_docids)
            precisions.append(p)
            ndcg_value = ndcg(correct_answers, returned_docids)
            ndcgs.append(ndcg_value)
            if verbose:
                print query
                print "P@%s" % (k,), precision(correct_answers, returned_docids)
                print "R@%s" % (k,), recall(correct_answers, returned_docids)
                print "F@%s" % (k,), f_measure(correct_answers, returned_docids)
                print "Relevant@%s" % (k,), relevant_at_k(correct_answers, returned_docids)
                print "nDCG@%s" % (k,), ndcg(correct_answers, returned_docids)
            query_results.append((correct_answers, returned_docids))

        map_value = mean_average_precision(query_results)
        mrr = mean_reciprocal_rank(query_results)
        avg_ndcg = sum(ndcgs)/float(len(ndcgs))
        avg_r = sum(recalls)/float(len(recalls))
        avg_p = sum(precisions)/float(len(precisions))
        print str(search_engine)
        #print "MAP", map_value
        #print "MRR", mrr
        #print "Avg. nDCG@k", avg_ndcg
        #print "Avg. R@k", avg_r
        #print "Avg. P@k", avg_p
        print map_value, mrr, avg_ndcg, avg_r, avg_p
        #print recalls

if __name__ == "__main__":
    # setup logging
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    # retrieval top k ranked
    k = 20
    search_engines = [
        #StandardSolrEngine(),
        StandardSolrEngine(query_expansion=WeightedW2VExpansion(alpha=5.0)),
        StandardSolrEngine(query_expansion=WeightedW2VExpansion(alpha=6.0)),
        StandardSolrEngine(query_expansion=WeightedW2VExpansion(alpha=7.0)),
        StandardSolrEngine(query_expansion=WeightedW2VExpansion(alpha=8.0)),
        StandardSolrEngine(query_expansion=WeightedW2VExpansion(alpha=9.0)),
        StandardSolrEngine(query_expansion=WeightedW2VExpansion(alpha=10.0)),
        ]

    for engine in search_engines:
        evaluate(engine, k, verbose=False)