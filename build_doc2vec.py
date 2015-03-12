__author__ = 'matias'

import logging
from irmodels.D2Vmodel import D2Vmodel
from textanalysis.texts import PhraseSentenceStream, RawSentenceStream, extract_mesh_terms
from textanalysis.phrasedetection import PmiPhraseDetector


# setup logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
# phrase detector
phrase_detector = PmiPhraseDetector(RawSentenceStream())
# build model
m = D2Vmodel(PhraseSentenceStream(phrase_detector, extract_func=extract_mesh_terms), name="DOCID")


pos = phrase_detector.detect(u"swelling tongue".split())
neg = phrase_detector.detect(u"".split())
print m.inner_model.most_similar(pos)