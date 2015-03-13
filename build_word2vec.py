__author__ = 'matias'

import logging
from irmodels.W2Vmodel import W2Vmodel
from textanalysis.texts import PhraseSentenceStream, RawSentenceStream
from textanalysis.phrasedetection import PmiPhraseDetector


# setup logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
# phrase detector
phrase_detector = PmiPhraseDetector(RawSentenceStream())
# build model
m = W2Vmodel(PhraseSentenceStream(phrase_detector))


print m.inner_model.most_similar(u"colon_cancer".split())
print m.inner_model.most_similar(u"new_york michigan california".split())
print m.inner_model.most_similar(u"pain back back_pain lumbar".split())
print m.inner_model.most_similar(u"blood".split())
print m.inner_model.most_similar(u"usa germany america france england uk india".split())
print m.inner_model.most_similar(u"symptom symptoms".split())
print m.inner_model.most_similar(u"disease".split())
print m.inner_model.most_similar(u"rare".split())
print m.inner_model.most_similar(u"boy man".split(), u"girl".split())
print m.inner_model.most_similar(u"african caucasian asian hispanic".split())
print m.inner_model.most_similar(u"testicles".split(), u"male".split())
print m.inner_model.most_similar(u"blood".split(), u"red".split())
print m.inner_model.most_similar(u"leg shin femur achilles thigh hip".split())
print m.inner_model.most_similar(u"summer winter spring autumn".split())
print m.inner_model.most_similar(u"bleeding colon burning rectum disease".split())
print m.inner_model.most_similar(u"bacteria".split())
print m.inner_model.most_similar(u"christian muslim".split())
print m.inner_model.most_similar(u"influenza cancer copd asthma colitis blind deaf gout diabetes".split())

