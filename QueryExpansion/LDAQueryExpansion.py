__author__ = 'matias'

from gensim import corpora, models
import os


def train_lda(n_topics, n_passes, update_every=0):
    lda_model = models.LdaModel(corpus, num_topics=n_topics, update_every=update_every, passes=n_passes, id2word=dictionary)
    return lda_model


if __name__ == "__main__":
    # model parameters
    vocabulary = ""
    topics = 30
    passes = 10

    # load data
    data_folder = os.path.join(*[os.path.dirname(__file__), 'data'])
    filename = "LDAmodel%s_%s_%s" % (topics, passes,)
    dictionary = corpora.Dictionary.load(os.path.join(data_folder, 'standard.dict'))
    corpus = corpora.MmCorpus(os.path.join(data_folder, 'standard.mm'))

    # does identical model already exists?
    model_exists = os.path.isfile(os.path.join(data_folder, filename))
    if model_exists:
        # if model already exists then load it
        print "loading model.."
        lda = models.LdaModel.load(os.path.join(data_folder, filename))
    else:
        print "training model.."
        lda = train_lda(topics, passes)
        print "saving model.."
        lda.save(os.path.join(data_folder, filename))

    for i in range(topics):
        print lda.print_topic(i, topn=30)

