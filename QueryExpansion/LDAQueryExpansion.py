__author__ = 'matias'


from gensim import corpora, models
import os

data_folder = os.path.join(*[os.path.dirname(__file__), 'data'])

dictionary = corpora.Dictionary.load(os.path.join(data_folder, 'standard.dict'))
corpus = corpora.MmCorpus(os.path.join(data_folder, 'standard.mm'))

lda = models.LdaModel(corpus,num_topics=100,id2word=dictionary)

print lda.print_topic(10)