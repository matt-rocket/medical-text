__author__ = 'matias'

from textanalysis.phrasedetection import PmiPhraseDetector
from textanalysis.texts import RawSentenceStream
import logging

# setup logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

phrase_detector = PmiPhraseDetector(RawSentenceStream())

phrase_detector.print_phrases()

