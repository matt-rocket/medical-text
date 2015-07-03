import logging
from irmodels.W2Vmodel import W2Vmodel
from textanalysis.texts import PhraseSentenceStream, RawSentenceStream
from textanalysis.phrasedetection import PmiPhraseDetector
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

# setup logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
# phrase detector
phrase_detector = PmiPhraseDetector(RawSentenceStream())
# build model
m = W2Vmodel(PhraseSentenceStream(phrase_detector))


with open("dump.txt", 'r') as infile:
    items = infile.read().lower().split(",")

with open("dumpmedication.txt", 'w') as outfile:
    for e in items:
        if e in m.inner_model.vocab:
            outfile.write("9,%s\n" % (e, ))
