__author__ = 'matias'

from irmodels.W2Vmodel import W2Vmodel
from sklearn import svm
from sklearn.metrics.pairwise import cosine_similarity


class DomainInformationExtractor(object):
    def __init__(self):
        self.w2v = W2Vmodel()
        xs = []
        ys = []
        with open('data/misc/domain_classify.txt', 'r') as infile:
            lines = infile.read().split("\n")
            for line in lines:
                word, y = line.split(',')
                word_vec = self.w2v.inner_model[word]
                xs.append(word_vec)
                ys.append(y)

        self.clf = svm.SVC()
        self.clf.fit(xs, ys)

    def classify(self, word):
        word_vec = self.w2v.inner_model[word]
        return self.clf.predict(word_vec)

if __name__ == "__main__":
    ex = DomainInformationExtractor()
    ex.classify("head")
