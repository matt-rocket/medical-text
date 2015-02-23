__author__ = 'matias'

from gensim import corpora
import os
from PubMedParser.entityextractor import CaseReportLibrary, DiseaseExtractor, SymptomExtractor
from PubMedParser.pubmed_tokenize import stopwords

data_folder = os.path.join(*[os.path.dirname(__file__), 'data'])

entity_stopwords = stopwords("disease").union(stopwords("symptom"))

d_extractor = DiseaseExtractor()
s_extractor = SymptomExtractor()

def create_entity_corpus():
    docs = []
    count = 1
    max_count = 50000
    for case in CaseReportLibrary():
        # get symptom and disease entities
        tokens = case.get_entities(d_extractor) + case.get_entities(s_extractor)
        # remove stopwords (2)
        tokens = [token for token in tokens if token not in entity_stopwords]
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