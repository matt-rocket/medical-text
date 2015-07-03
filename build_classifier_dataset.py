__author__ = 'Matias'

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from textanalysis.texts import CaseReportLibrary
from irmodels.D2Vmodel import D2Vmodel
import numpy as np
import logging
import json

class LabeledCases(object):
    def __init__(self, return_object=False):
        self.cases = CaseReportLibrary()
        self.labels = {}
        self.return_object = return_object
        with open("classification/data/class.txt", 'r') as infile:
            lines = infile.read().split("\n")[:-1]
            count = 0
            for line in lines:
                pmcid, cls = line.split(" ")
                self.labels[pmcid] = cls

    def __iter__(self):
        i = 1
        for case in self.cases:
            pmcid = case.get_pmcid()
            if pmcid not in self.labels:
                continue
            elif i >= len(self.labels):
                break
            else:
                i += 1
                item = case.get_text() if not self.return_object else (pmcid, self.labels[pmcid], case.get_text())
                yield item
                if i % 50 == 0:
                    msg = str("Streamed %s labeled case reports" % (i, ))
                    logging.info(msg)
            if i > 500:
                break

    def __len__(self):
        return len(self.cases)

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    corpus = LabeledCases()
    vectorizer = CountVectorizer(min_df=1, max_features=5000).fit(corpus)
    tfidf_vectorizer = TfidfVectorizer(min_df=1, max_features=5000).fit(corpus)
    ngram_vectorizer = TfidfVectorizer(min_df=1, ngram_range=(1, 2), max_features=15000).fit(corpus)
    ids = []
    docs = []
    labels = []

    for case in LabeledCases(return_object=True):
        pmcid, cls, text = case
        ids.append(pmcid)
        docs.append(text)
        labels.append(cls)

    docvecs_counts = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
    superdocvecs_counts = [40]

    bow = vectorizer.fit_transform(docs).toarray()
    tfidf = tfidf_vectorizer.fit_transform(docs).toarray()
    ngram = ngram_vectorizer.fit_transform(docs).toarray()

    with open('classification/data/labels_500.json', 'w') as outfile:
        json.dump({'ids': ids, 'labels': labels}, outfile)

    with open('classification/data/bow_500.txt', 'w') as outfile:
        np.savetxt(outfile, bow)

    with open('classification/data/tfidf_500.txt', 'w') as outfile:
        np.savetxt(outfile, tfidf)

    with open('classification/data/ngram_500.txt', 'w') as outfile:
        np.savetxt(outfile, ngram)


    for docvecs_count in docvecs_counts:

        d2v = D2Vmodel(
            None,
            name="DOCID",
            dataset_name="CASEREPORT",
            epochs=2,
            dimension=docvecs_count)

        docvecs = np.zeros(shape=(len(ids), docvecs_count))

        for idx, pmcid in enumerate(ids):
            docvecs[idx, :] = d2v.inner_model['DOCID-CS'+str(pmcid)]


        docvecs_filepath = str("classification/data/docvecs%s_500.txt" % (docvecs_count,))
        with open(docvecs_filepath, 'w') as outfile:
            np.savetxt(outfile, docvecs)

    for superdocvecs_count in superdocvecs_counts:

        d2v = D2Vmodel(
            None,
            name="DOCID",
            dataset_name="CASEREPORT",
            epochs=6,
            dimension=superdocvecs_count)

        superdocvecs = np.zeros(shape=(len(ids), superdocvecs_count))

        for idx, pmcid in enumerate(ids):
            superdocvecs[idx, :] = d2v.inner_model['DOCID-CS'+str(pmcid)]


        superdocvecs_filepath = str("classification/data/superdocvecs%s_500.txt" % (superdocvecs_count,))
        with open(superdocvecs_filepath, 'w') as outfile:
            np.savetxt(outfile, superdocvecs)
