__author__ = 'matias'

from gensim import corpora
import os
from textanalysis.texts import CaseReportLibrary
from textanalysis.Analyzers import EntityAnalyzer


def create_entity_corpus():
    data_folder = os.path.join(*[os.path.dirname(__file__), 'data', 'corpora'])

    analyzer = EntityAnalyzer()

    docs = []
    count = 1
    max_count = 50000
    for case in CaseReportLibrary():
        text = case.get_text()
        # get symptom and disease entities
        tokens = analyzer.parse(text)

        docs.append(tokens)
        count += 1
        if count % 100 == 0:
            print count,"/",max_count
        if count >= max_count:
            break

    dictionary = corpora.Dictionary(docs)
    corpus = [dictionary.doc2bow(doc) for doc in docs]

    dictionary.save(os.path.join(data_folder, 'entity.dict'))
    corpora.MmCorpus.serialize(os.path.join(data_folder, 'entity.mm'), corpus)


if __name__ == "__main__":
    create_entity_corpus()