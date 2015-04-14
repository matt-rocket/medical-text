__author__ = 'matias'

from irmodels.D2Vmodel import D2Vmodel
from textanalysis.texts import PhraseSentenceStream, RawSentenceStream, ExtractDiseases
from textanalysis.phrasedetection import PmiPhraseDetector
import logging



# setup logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
# phrase detector
phrase_detector = PmiPhraseDetector(RawSentenceStream(fz_docs=False))

extract_disease = ExtractDiseases()

# build model
epochs = 3
m = D2Vmodel(
    PhraseSentenceStream(phrase_detector, extract_func=extract_disease, fz_docs=False, reshuffles=epochs-1),
    name="DISEASE",
    dataset_name="CASEREPORT",
    epochs=epochs)



