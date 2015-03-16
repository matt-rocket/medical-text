__author__ = 'matias'

from gensim.models.word2vec import Word2Vec
import logging
import os


class W2Vmodel(object):
    def __init__(self, sentences=[]):
        self.inner_model = None

        # parameters
        self.dataset = "CASEREPORT"
        self.sentences = sentences

        # data file path
        models_folder = os.path.join(*[os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'models'])
        filename = "WORD2VEC_%s" % (self.dataset, )
        self.filepath = os.path.join(models_folder, filename)
        model_exists = os.path.isfile(self.filepath)

        if model_exists:
            logging.info("found data file %s" % (self.filepath, ))
            self.inner_model = Word2Vec.load(self.filepath)
        else:
            self.inner_model = Word2Vec(sentences=self.sentences)
            self.inner_model.save(self.filepath)

    def __contains__(self, item):
        return item in self.inner_model
