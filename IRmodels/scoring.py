__author__ = 'matias'

from scipy.stats import entropy

def kl_divergence(p, q):
    """
    Compute Symmetric Kullback-Leibler divergence between 2 probability distributions
    Also known as the Shannon-Jensen divergence.
    :param p: a probability distribution
    :param q: another probability distribution
    :return: KL divergence measure
    """
    return 0.5*(entropy(p, q) + entropy(q, p))