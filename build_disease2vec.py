__author__ = 'matias'

from irmodels.D2Vmodel import D2Vmodel
from textanalysis.texts import PhraseSentenceStream, RawSentenceStream, ExtractDiseases
from textanalysis.phrasedetection import PmiPhraseDetector
from scipy.spatial.distance import cosine
from heapq import heappush, heappop
import numpy as np
import logging



# setup logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
# phrase detector
phrase_detector = PmiPhraseDetector(RawSentenceStream(fz_docs=False))

extract_disease = ExtractDiseases()

# build model
epochs = 3
m = D2Vmodel(
    PhraseSentenceStream(phrase_detector, extract_func=extract_disease, fz_docs=False, reshuffles=epochs-1),
    name="DISEASE",
    dataset_name="CASEREPORT",
    epochs=epochs)

vec_lupus = m.inner_model["man"]
print np.all(np.isnan(vec_lupus))

disease_count = len([word for word in m.inner_model.vocab if word.startswith("DISEASE-")])
not_nans = [word for word in m.inner_model.vocab if not np.all(np.isnan(m.inner_model[word]))]
print not_nans
print "non-nan count", len(not_nans)
print "count", disease_count
print "total word count", len(m.inner_model.vocab)

"""
ranking = []

for word in m.inner_model.vocab:
    if word.startswith("DISEASE-"):
        vec_disease = m.inner_model[word]
        print vec_disease
        #distance = cosine(vec_lupus, vec_disease)
        #heappush(ranking, (distance, word))
        print "added", word

for i in range(20):
    dist, disease = heappop(ranking)
    print i, "\t", dist, disease
"""