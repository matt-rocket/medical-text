__author__ = 'matias'

from gensim import corpora
import os
from PubMedParser.entityextractor import CaseReportLibrary
from PubMedParser.pubmed_tokenize import tokenize, stopwords

data_folder = os.path.join(*[os.path.dirname(__file__), 'data'])

pubmed_stopwords = stopwords("pubmed_v3")

def create_corpus():
    docs = []
    count = 1
    max_count = 50000
    for case in CaseReportLibrary():
        # lower case all text (1)
        text = case.get_text().lower()
        tokens = tokenize(text)
        # remove stopwords (2)
        tokens = [token for token in tokens if token not in pubmed_stopwords]
        # TODO: stem tokens (3)

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