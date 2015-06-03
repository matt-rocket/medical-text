__author__ = 'matias'

from irmodels.D2Vmodel import D2Vmodel, DocIndex
from textanalysis.texts import PhraseSentenceStream, RawSentenceStream, extract_docid, extract_mesh_terms
from textanalysis.phrasedetection import PmiPhraseDetector
import logging
from scipy.spatial.distance import cosine
from textanalysis.texts import FZArticleLibrary, CaseReportLibrary
from heapq import heappush, heappop
import numpy as np

# setup logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
# phrase detector
pmi_level = 90
phrase_detector = PmiPhraseDetector(RawSentenceStream(fz_docs=False),
                                    filename=str("PHRASE_%s_2_CASEREPORT_RAW" % (pmi_level, )))

# build model
epochs = 2
m = D2Vmodel(
    PhraseSentenceStream(phrase_detector, extract_func=extract_docid, fz_docs=False, reshuffles=epochs-1),
    name="DOCID",
    dataset_name="CASEREPORT+PMI"+str(pmi_level),
    epochs=epochs,
    dimension=30)

doc_index = DocIndex(CaseReportLibrary(), "CASEREPORT")



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
"""

vec_query1 = m.infer_doc_vector("bleeding from colon, bloody stool, abdominal pain, diarrhea", steps=50)
vec_query2 = m.infer_doc_vector("memory loss, cognitive and functional difficulties, mild cognitive impairment.", steps=50)
vec_query3 = m.infer_doc_vector("tender warm swollen joints, morning stiffness", steps=50)
vec_query4 = m.infer_doc_vector("fever, sore throat, muscular pain, and headaches, vomiting, diarrhea and rash, decreased liver function, external and internal bleeding",steps=50)

"""
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


for word in m.inner_model.vocab:
    if word.startswith("MESH-"):
        print word


def normalize(array):
    np.linalg.norm(array)*1.0/array

case_id = 'DOCID-CS3471415'
case_vec = m.inner_model[case_id]

"""
filename = r"C:\Users\matias\Desktop\thesis\data\casereports\Case_Rep_Oncol_2013_Jan_9_6(1)_25-30.nxml"
for article in CaseReportLibrary(filename=filename):
    text = article.get_text()
    print article.get_abstract()
    case_vec = m.inner_model.infer_vector(text, steps=50)
    print case_vec
"""

ranking = []

for word in m.inner_model.vocab:
    if word.startswith("DOCID-CS"):
        doc_vec = m.inner_model[word]
        distance = cosine(case_vec, doc_vec)
        heappush(ranking, (distance, word))
        #print "added", doc_index[word]

for i in range(10):
    dist, doc_id = heappop(ranking)
    print doc_id
    print i, "\t", dist, doc_index[doc_id]