__author__ = 'matias'

from math import log, fabs
from scipy.stats import entropy

def kl_divergence(p, q):
    """
    Compute Kullback-Leibler divergence between 2 probability distributions.
    :param p: a probability distribution
    :param q: another probability distribution
    :return: KL divergence measure
    """
    # FIXME: something wrong here when entry is zero
    # return sum([p[i]*log(p[i]/q[i]) for i in range(len(q))])
    return entropy(p, q)