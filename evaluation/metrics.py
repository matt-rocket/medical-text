__author__ = 'matias'


def precision(correct_answers, results):
    relevant_and_retrieved = [doc for doc in results if doc in correct_answers]
    return len(relevant_and_retrieved) / float(len(results))


def recall(correct_answers, results):
    relevant_and_retrieved = [doc for doc in results if doc in correct_answers]
    return len(relevant_and_retrieved) / float(len(correct_answers))


def f_measure(correct_answers, results):
    r = recall(correct_answers, results)
    p = precision(correct_answers, results)
    return 2 * float(p*r)/(p+r)
