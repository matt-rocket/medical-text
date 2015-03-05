__author__ = 'matias'

import logging
from irmodels.W2Vmodel import W2Vmodel
from textanalysis.texts import PhraseSentenceStream, SentenceStream
from textanalysis.phrasedetection import PmiPhraseDetector


# setup logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
# phrase detector
phrase_detector = PmiPhraseDetector(SentenceStream())
# build model
m = W2Vmodel(PhraseSentenceStream(phrase_detector))

print m.model.most_similar(u"colon_cancer".split())
print m.model.most_similar(u"new_york michigan california".split())
print m.model.most_similar(u"pain back back_pain lumbar".split())
print m.model.most_similar(u"blood".split())
print m.model.most_similar(u"usa germany america france england uk india".split())
print m.model.most_similar(u"symptom symptoms".split())
print m.model.most_similar(u"disease".split())
print m.model.most_similar(u"rare".split())
print m.model.most_similar(u"boy man".split(), u"girl".split())
print m.model.most_similar(u"african caucasian asian hispanic".split())
print m.model.most_similar(u"testicles".split(), u"male".split())
print m.model.most_similar(u"blood".split(), u"red".split())
print m.model.most_similar(u"leg shin femur achilles thigh hip".split())
print m.model.most_similar(u"summer winter spring autumn".split())
print m.model.most_similar(u"bleeding colon burning rectum disease".split())
print m.model.most_similar(u"bacteria".split())
print m.model.most_similar(u"christian muslim".split())
print m.model.most_similar(u"influenza cancer copd asthma colitis blind deaf gout diabetes".split())


query = u"ulcerative colitis asacol aspirin naproxen penicillin".split()
#query = u"bloody stool abdominal pain frequent stool bloated loose stool".split()

tokens = phrase_detector.detect(query)
print tokens
combined_sim = m.model.most_similar(tokens, topn=50)
token_sims = [m.model.most_similar(token, topn=50) for token in tokens]

print "COMBINED:"
print combined_sim

intersection = set([e[0] for e in combined_sim])

print "TOKENS:"
for sim in token_sims:
    print sim
    intersection = intersection.intersection(set([e[0] for e in sim]))

print list(intersection)