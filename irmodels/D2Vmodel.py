__author__ = 'matias'

from gensim.models.doc2vec import Doc2Vec
import logging
import os
import pickle

class D2Vmodel(object):
    def __init__(self, sentences, name, dataset_name, epochs=1):
        self.inner_model = None

        # parameters
        self.dataset = dataset_name
        self.sentences = sentences
        self.name = name
        self.epochs = epochs

        # data file path
        models_folder = os.path.join(*[os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'models'])
        filename = "DOC2VEC_%s_%s_%s" % (self.dataset, self.name, self.epochs)
        self.filepath = os.path.join(models_folder, filename)
        model_exists = os.path.isfile(self.filepath)

        # train initial model
        if model_exists:
            logging.info("found data file %s" % (self.filepath, ))
            self.inner_model = Doc2Vec.load(self.filepath)
        else:
            self.inner_model = Doc2Vec(sentences)
            print self.inner_model.vocab.keys()
            self.inner_model.save(fname=self.filepath)

    def __contains__(self, item):
        return item in self.inner_model

    def infer_doc_vector(self, tokens):
        self.inner_model.infer_vector(document=tokens, steps=50)


class DocIndex(object):
    def __init__(self, doc_library, name):
        self.docs = doc_library
        self.name = name
        self.docid2filename = {}

        models_folder = os.path.join(*[os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'models'])
        filename = "DOCINDEX_%s" % (self.name, )
        self.filepath = os.path.join(models_folder, filename)
        model_exists = os.path.isfile(self.filepath)

        if model_exists:
            # load data
            self.docid2filename = pickle.load(open(self.filepath, 'r'))
        else:
            count = 1
            for doc in self.docs:
                self.docid2filename[doc.get_id()] = doc.title
                print count, doc.title
                count += 1
            # save data
            pickle.dump(self.docid2filename, open(self.filepath, 'w'))

    def __getitem__(self, item):
        return self.docid2filename[item]


if __name__ == "__main__":
    from textanalysis.texts import CaseReportLibrary, FZArticleLibrary
    index = DocIndex(FZArticleLibrary(), "FINDZEBRA")
