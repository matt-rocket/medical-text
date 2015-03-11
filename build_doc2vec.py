__author__ = 'matias'

import logging
from irmodels.D2Vmodel import D2Vmodel
from textanalysis.texts import PhraseSentenceStream, RawSentenceStream, extract_docid
from textanalysis.phrasedetection import PmiPhraseDetector


# setup logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
# phrase detector
phrase_detector = PmiPhraseDetector(RawSentenceStream())
# build model
m = D2Vmodel(PhraseSentenceStream(phrase_detector, extract_func=extract_docid))
