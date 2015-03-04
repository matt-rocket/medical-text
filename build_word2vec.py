__author__ = 'matias'

import logging
from irmodels.W2Vmodel import W2Vmodel
from textanalysis.texts import PhraseSentenceStream

# setup logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
# build model
m = W2Vmodel(PhraseSentenceStream())


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


