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

symptoms = []
for line in file("data/misc/symptoms.txt").read().split("\n")[:-1]:
    cui, name = line.split("\t")
    name = name.lower().replace(" ", "_")
    symptoms.append(name)

for symp in symptoms:
    if symp in m.inner_model.vocab:
        print symp, "->", m.inner_model.most_similar_cosmul(symp.split())

"""
for word in m.inner_model.vocab:
    if word in symptoms:
        print word
"""

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

