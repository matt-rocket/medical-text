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

print m.inner_model.most_similar_cosmul(u"lipoma lymphangioma".split(), u"fat".split())
print m.inner_model.most_similar_cosmul(u"osteoma fibroma".split(), u"bone".split())
print m.inner_model.most_similar_cosmul(u"chondroma adenoma".split(), u"cartilage".split())
print m.inner_model.most_similar_cosmul(u"hiv leukemia".split(), u"abacavir".split())


"""
print m.inner_model.most_similar_cosmul(u"asacol".split())
print m.inner_model.most_similar_cosmul(u"colitis".split())
print m.inner_model.most_similar_cosmul(u"lupus".split())
print m.inner_model.most_similar_cosmul(u"neck".split())
print m.inner_model.most_similar_cosmul(u"retina".split())
print m.inner_model.most_similar_cosmul(u"pain".split())
print m.inner_model.most_similar_cosmul(u"glaucoma".split())
print m.inner_model.most_similar_cosmul(u"huntington".split())
print m.inner_model.most_similar_cosmul(u"alzheimer".split())
"""

