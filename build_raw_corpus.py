__author__ = 'matias'

from gensim import corpora
import os
from textanalysis.texts import CaseReportLibrary
from textanalysis.pubmed_tokenize import tokenize


def create_corpus():
    data_folder = os.path.join(*[os.path.dirname(__file__), 'data', 'corpora'])

    docs = []
    count = 1
    max_count = 50000
    for case in CaseReportLibrary():
        # lower case all text (1)
        text = case.get_text()
        tokens = tokenize(text)
        docs.append(tokens)
        count += 1
        if count % 100 == 0:
            print count,"/",max_count
        if count >= max_count:
            break

    dictionary = corpora.Dictionary(docs)
    corpus = [dictionary.doc2bow(doc) for doc in docs]

    dictionary.save(os.path.join(data_folder, 'raw.dict'))
    corpora.MmCorpus.serialize(os.path.join(data_folder, 'raw.mm'), corpus)


if __name__ == "__main__":
    create_corpus()