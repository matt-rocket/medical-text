__author__ = 'matias'

from gensim import corpora
import os
from textanalysis.texts import CaseReportLibrary
from textanalysis.Analyzers import StandardAnalyzer


def create_corpus():
    data_folder = os.path.join(*[os.path.dirname(__file__), 'data', 'corpora'])

    analyzer = StandardAnalyzer()

    docs = []
    count = 1
    max_count = 50000
    for case in CaseReportLibrary():
        # lower case all text (1)
        text = case.get_text()
        tokens = analyzer.parse(text)
        docs.append(tokens)
        count += 1
        if count % 100 == 0:
            print count,"/",max_count
        if count >= max_count:
            break

    dictionary = corpora.Dictionary(docs)
    corpus = [dictionary.doc2bow(doc) for doc in docs]

    dictionary.save(os.path.join(data_folder, 'standard.dict'))
    corpora.MmCorpus.serialize(os.path.join(data_folder, 'standard.mm'), corpus)


if __name__ == "__main__":
    create_corpus()