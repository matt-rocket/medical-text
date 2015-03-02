__author__ = 'matias'

from textanalysis.texts import SentenceStream
import logging
from gensim.models.phrases import Phrases


# setup logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

sentences = SentenceStream()

bigram = Phrases.learn_vocab(sentences,max_vocab_size=4000000)



for word in bigram[1]:
    print word
