__author__ = 'matias'

from math import log

def precision(correct_answers, results):
    relevant_and_retrieved = [doc for doc in results if doc in correct_answers]
    return len(relevant_and_retrieved) / float(len(results))


def recall(correct_answers, results):
    relevant_and_retrieved = [doc for doc in results if doc in correct_answers]
    if len(correct_answers) > 0:
        return len(relevant_and_retrieved) / float(len(correct_answers))
    else:
        return 0.0


def f_measure(correct_answers, results):
    r = recall(correct_answers, results)
    p = precision(correct_answers, results)
    if (p+r) > 0:
        return 2 * float(p*r)/(p+r)
    else:
        return 0.0


def average_precision(correct_answers, results):
    relevance = map(lambda x: 1 if x in correct_answers else 0, results)
    numerator = sum([relevance[k-1]*precision(correct_answers, results[:k]) for k in range(1,len(results)+1)])
    denominator = len(correct_answers)
    return numerator/denominator if denominator > 0 else 0.0


def mean_average_precision(query_results):
    numerator = sum([average_precision(correct, results) for correct, results in query_results])
    denominator = len(query_results)
    return numerator/denominator


def mean_reciprocal_rank(query_results):
    reciprocal_ranks = []
    for correct, results in query_results:
        relevance = map(lambda x: 1 if x in correct else 0, results)
        if 1 in relevance:
            reciprocal_ranks.append(1.0/(relevance.index(1)+1.0))
        else:
            reciprocal_ranks.append(0.0)
    return sum(reciprocal_ranks)/len(query_results)


def ndcg(correct, results):
    relevance = map(lambda x: 1 if x in correct else 0, results)
    ordered_relevance = sorted(relevance,reverse=True)
    dcg = sum([(2.0**relevance[i] - 1)/log(i+2) for i in range(len(relevance))])
    idcg = sum([(2.0**ordered_relevance[i] - 1)/log(i+2) for i in range(len(ordered_relevance))])
    result = dcg/idcg if idcg > 0 else 0.0
    return result


def relevant_at_k(correct, results):
    relevance = map(lambda x: 1 if x in correct else 0, results)
    if 1 in relevance:
        return relevance.index(1)+1
    else:
        return None
