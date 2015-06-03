__author__ = 'matias'

from gensim.models.doc2vec import Doc2Vec
import logging
import os
import pickle
from nltk.tokenize import word_tokenize, sent_tokenize

class D2Vmodel(object):
    def __init__(self, sentences, name, dataset_name, epochs=1, dimension=50, modelfile=None):
        self.inner_model = None

        # parameters
        self.dataset = dataset_name
        self.sentences = sentences
        self.name = name
        self.epochs = epochs
        self.dimension = dimension

        # data file path
        models_folder = os.path.join(*[os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'models'])
        if modelfile is not None:
            filename = modelfile
        else:
            filename = "DOC2VEC_%s_%s_%s_%s" % (self.dataset, self.name, self.epochs, self.dimension)
        self.filepath = os.path.join(models_folder, filename)
        model_exists = os.path.isfile(self.filepath)

        # train initial model
        if model_exists:
            logging.info("found data file %s" % (self.filepath, ))
            self.inner_model = Doc2Vec.load(self.filepath)
        else:
            self.inner_model = Doc2Vec(sentences, size=self.dimension)
            print self.inner_model.vocab.keys()
            self.inner_model.save(fname=self.filepath)

    def __contains__(self, item):
        return item in self.inner_model

    def infer_doc_vector(self, text, steps=50, phrase_detector=None):
        text = text.lower()
        tokens = []
        for sent in sent_tokenize(text):
            tokens += word_tokenize(sent)
        if phrase_detector is not None:
            tokens = phrase_detector.detect(tokens)
        return self.inner_model.infer_vector(document=tokens, steps=steps)


class DocIndex(object):
    def __init__(self, doc_library, name):
        self.docs = doc_library
        self.name = name
        self.docid2name = {}

        models_folder = os.path.join(*[os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'models'])
        filename = "DOCINDEX_%s" % (self.name, )
        self.filepath = os.path.join(models_folder, filename)
        model_exists = os.path.isfile(self.filepath)

        if model_exists:
            # load data
            self.docid2name = pickle.load(open(self.filepath, 'r'))
        else:
            count = 1
            for doc in self.docs:
                self.docid2name[doc.get_id()] = doc.title
                print count, doc.title
                count += 1
            # save data
            pickle.dump(self.docid2name, open(self.filepath, 'w'))

    def __getitem__(self, item):
        return self.docid2name[item]


class InferredIndex(object):
    def __init__(self, doc_library, name, doc2vec, phrase_detector=None):
        self.doc_index = DocIndex(doc_library=doc_library, name=name)
        self.docid2vec = {}
        self.docs = doc_library

        models_folder = os.path.join(*[os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'models'])
        filename = "INFERINDEX_%s" % (name, )
        self.filepath = os.path.join(models_folder, filename)
        model_exists = os.path.isfile(self.filepath)

        if model_exists:
            # load data
            self.docid2vec = pickle.load(open(self.filepath, 'r'))
        else:
            count = 1
            for doc in self.docs:
                self.docid2vec[doc.get_id()] = doc2vec.infer_doc_vector(
                    doc.get_text(),
                    steps=50,
                    phrase_detector=phrase_detector)
                print count, doc.title
                count += 1
            # save data
            pickle.dump(self.docid2vec, open(self.filepath, 'w'))

    def __getitem__(self, item):
        return self.docid2vec[item]

    def __iter__(self):
        for docid in self.docid2vec:
            yield docid


if __name__ == "__main__":
    from textanalysis.texts import CaseReportLibrary, FZArticleLibrary
    index = DocIndex(FZArticleLibrary(), "FINDZEBRA")
