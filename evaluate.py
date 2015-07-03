__author__ = 'matias'

from search import StandardSolrEngine, Doc2VecSearchEngine, ElasticSearchEngine, RandomSearchEngine
from queryexpansion import *
from evaluation.metrics import *
import logging


def evaluate(search_engine, k, verbose=False, eval_file='findzebra2.tsv'):
    with open('evaluation/data/%s' % (eval_file,), 'r') as infile:

        records = infile.read().split("\n")

        query_results = []

        recalls = []
        precisions = []
        ndcgs = []

        for record in records:
            print record.split("\t")
            qid, query, answer, relevant, partly_relevant = record.split("\t")
            correct_answers = [ans for ans in relevant.split(",") + partly_relevant.split(",") if ans is not '']
            response = search_engine.query(query, top_n=k)
            returned_docids = [hit[u'id'] for hit in response]
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
    # lda_model = LDAmodel(n_topics=500, n_passes=50, vocabulary='combined', latent_vectors=False)
    k = 20
    search_engines = [
        #RandomSearchEngine(),
        #ElasticSearchEngine(),
        #StandardSolrEngine(),
        #Doc2VecSearchEngine(size=10),
        #Doc2VecSearchEngine(size=15),
        #Doc2VecSearchEngine(size=20),
        #Doc2VecSearchEngine(size=25),
        #Doc2VecSearchEngine(size=30),
        #Doc2VecSearchEngine(size=35),
        #Doc2VecSearchEngine(size=40),
        #Doc2VecSearchEngine(size=45),
        #Doc2VecSearchEngine(size=50),
        #Doc2VecSearchEngine(modelfile="DOC2VEC_CASEREPORT_DOCID_6_40"),
        ElasticSearchEngine(query_expansion=AverageW2VExpansion(p=0.9)),
        ]

    for engine in search_engines:
        evaluate(engine, k, verbose=False, eval_file='casereports_1_2014.tsv')