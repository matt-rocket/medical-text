__author__ = 'matias'

from scipy.stats import entropy
from math import log

def kl_divergence(p, q):
    """
    Compute Kullback-Leibler divergence between 2 probability distributions
    :param p: a probability distribution
    :param q: another probability distribution
    :return: KL divergence measure
    """
    measure = 0
    for i in range(len(p)):
        if p[i] != 0 and q[i] != 0:
            measure += p[i]*log(p[i]/float(q[i]))
    return measure

def sj_divergence(p, q):
    """
    Compute the Shannon-Jensen divergence, a symmetric KL-divergence.
    :param p: a probability distribution
    :param q: another probability distribution
    :return: SJ divergence measure
    """
    return 0.5*(entropy(p, q) + entropy(q, p))