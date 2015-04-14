__author__ = 'matias'

from irmodels.D2Vmodel import D2Vmodel, DocIndex
from textanalysis.texts import PhraseSentenceStream, RawSentenceStream, extract_docid, extract_mesh_terms
from textanalysis.phrasedetection import PmiPhraseDetector
import logging
from scipy.spatial.distance import cdist, cosine
import numpy as np
from textanalysis.texts import FZArticleLibrary
from heapq import heappush, heappop



# setup logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
# phrase detector
phrase_detector = PmiPhraseDetector(RawSentenceStream(fz_docs=False))

# build model
epochs = 10
m = D2Vmodel(
    PhraseSentenceStream(phrase_detector, extract_func=extract_docid, fz_docs=True, reshuffles=epochs-1),
    name="DOCID",
    dataset_name="FINDZEBRA",
    epochs=epochs)

doc_index = DocIndex(FZArticleLibrary(), "FINDZEBRA")



"""
sims = m.inner_model.most_similar(['DOCID-FZ4870'],topn=20)

vec_lung_cancer = m.inner_model['DOCID-FZ4870']
vec_colitis = m.inner_model['DOCID-FZ1397']
vec_crohn1 = m.inner_model['DOCID-FZ20248']
vec_crohn2 = m.inner_model['DOCID-FZ18205']
vec_colorectal_cancer = m.inner_model['DOCID-FZ9693']
vec_diabetes = m.inner_model['DOCID-FZ14622']
vec_huntington = m.inner_model['DOCID-FZ142']
vec_alzheimers = m.inner_model['DOCID-FZ3951']
vec_early_alzheimers = m.inner_model['DOCID-FZ3953']

vec_query1 = m.inner_model.infer_vector("bleeding from colon, bloody stool, abdominal pain, diarrhea".split(),steps=50000)
vec_query2 = m.inner_model.infer_vector("memory loss, cognitive and functional difficulties, mild cognitive impairment.".split(),steps=50000)

print "lung cancer", 1-cosine(vec_lung_cancer, vec_query1), 1-cosine(vec_lung_cancer, vec_query2)
print "colitis", 1-cosine(vec_colitis, vec_query1), 1-cosine(vec_colitis, vec_query2)
print "crohn1", 1-cosine(vec_crohn1, vec_query1), 1-cosine(vec_crohn1, vec_query2)
print "crohn2", 1-cosine(vec_crohn2, vec_query1), 1-cosine(vec_crohn2, vec_query2)
print "colorectal cancer", 1-cosine(vec_colorectal_cancer, vec_query1), 1-cosine(vec_colorectal_cancer, vec_query2)
print "diabetes", 1-cosine(vec_diabetes, vec_query1), 1-cosine(vec_diabetes, vec_query2)
print "alzheimer's", 1-cosine(vec_alzheimers, vec_query1), 1-cosine(vec_alzheimers, vec_query2)
print "early onset alzheimer's", 1-cosine(vec_early_alzheimers, vec_query1), 1-cosine(vec_early_alzheimers, vec_query2)
"""
#print doc_index.docid2filename
#for sim in sims:
#    print doc_index[sim[0]], sim

#for word in m.inner_model.vocab:
#    if word.startswith("DOCID-FZ") and "Alzheimer's" in doc_index[word]:
#        print word, doc_index[word]

from nltk.tokenize import sent_tokenize, word_tokenize

colitis_id = 'DOCID-FZ1397'
filename = r"C:\Users\matias\Desktop\thesis\medical-text\data\articles\findzebra\colitis.json"
for article in FZArticleLibrary(filename=filename):
    text = article.get_text().lower()
    tokens = []
    for sent in sent_tokenize(text):
        tokens += word_tokenize(sent)
    phrases = phrase_detector.detect(tokens)
    colitis_vec = m.inner_model.infer_vector(phrases, steps=100)


ranking = []

for word in m.inner_model.vocab:
    if word.startswith("DOCID-FZ"):
        doc_vec = m.inner_model[word]
        distance = cosine(colitis_vec, doc_vec)
        heappush(ranking, (distance, word))
        print "added", doc_index[word]

for i in range(100):
    dist, doc_id = heappop(ranking)
    print i, "\t", dist, doc_index[doc_id]
