__author__ = 'matias'

from W2Vmodel import W2Vmodel
from scipy import spatial
import random


class CRPmodel(object):
    def __init__(self, w2v_model):
        self.tables = []
        self.model = w2v_model
        self.N = 0

    def train(self):
        for word in self.model.inner_model.vocab:
            print "The word is..", word
            self._sit_down(word)

    def _sit_down(self, word):
        vec = self.model.inner_model[word]
        # new table probability
        newp = 1.0/(self.N+1)
        rand = random.random()
        if rand <= newp:
            # create new table
            self.tables.append(([word], vec))
        else:
            # place at most similar table
            table_dists = [spatial.distance.cosine(vec, table[1]) for table in self.tables]
            table_no = table_dists.index(max(table_dists))
            words, table_vec = self.tables[table_no]
            self.tables[table_no] = (words + [word], vec+table_vec)
        self.N += 1

    def retrain(self):
        pass

    def show_tables(self):
        for table in self.tables:
            # output only words
            print table[0]


if __name__ == "__main__":
    crp = CRPmodel(W2Vmodel())
    crp.train()
    crp.show_tables()