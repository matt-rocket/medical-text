__author__ = 'matias'


from gensim import corpora, models
import os

data_folder = os.path.join(*[os.path.dirname(__file__), 'data'])

dictionary = corpora.Dictionary.load(os.path.join(data_folder, 'sample.dict'))

corpus = corpora.MmCorpus(os.path.join(data_folder, 'sample.mm'))

lda = models.LdaModel(corpus,num_topics=10,id2word=dictionary)

for i in range(10):
    print lda.print_topic(i, topn=5)
