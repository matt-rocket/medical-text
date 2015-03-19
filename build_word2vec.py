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

print m.inner_model.most_similar_cosmul(u"testicles".split(), u"woman".split())
print m.inner_model.most_similar_cosmul(u"blood red".split(), u"stool".split())
print m.inner_model.most_similar_cosmul(u"asacol ibd".split(), u"methotrexate".split())

print m.inner_model.most_similar_cosmul(u"asacol".split())
print m.inner_model.most_similar_cosmul(u"colitis".split())
print m.inner_model.most_similar_cosmul(u"lupus".split())
print m.inner_model.most_similar_cosmul(u"neck".split())
print m.inner_model.most_similar_cosmul(u"retina".split())
print m.inner_model.most_similar_cosmul(u"pain".split())
print m.inner_model.most_similar_cosmul(u"glaucoma".split())
print m.inner_model.most_similar_cosmul(u"huntington".split())
print m.inner_model.most_similar_cosmul(u"alzheimer".split())


