__author__ = 'matias'

from gensim.models.tfidfmodel import TfidfModel
from gensim import corpora
import logging
import os


class TFIDFmodel(object):
    def __init__(self):
        self.inner_model = None

        # load dictionary and corpus
        vocabulary = "raw"
        corpora_folder = os.path.join(*[os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'corpora'])
        self.dictionary = corpora.Dictionary.load(os.path.join(corpora_folder, "%s.dict" % (vocabulary,)))
        self.corpus = corpora.MmCorpus(os.path.join(corpora_folder, "%s.mm" % (vocabulary,)))

        # parameters
        self.dataset = "CASEREPORT"

        # data file path
        models_folder = os.path.join(*[os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'models'])
        filename = "TFIDF_%s" % (self.dataset, )
        self.filepath = os.path.join(models_folder, filename)
        model_exists = os.path.isfile(self.filepath)

        if model_exists:
            logging.info("found data file %s" % (self.filepath, ))
            self.inner_model = TfidfModel.load(self.filepath)
        else:
            self.inner_model = TfidfModel(corpus=self.corpus)
            self.inner_model.save(self.filepath)

    def __contains__(self, item):
        return item in self.inner_model


if __name__ == "__main__":
    # setup logging
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    # build model
    tfidf = TFIDFmodel()
    print tfidf.dictionary.token2id['and']