__author__ = 'matias'

from gensim import corpora, models
from gensim.matutils import sparse2full
from scoring import kl_divergence
import os
import logging


class HDPmodel(object):
    def __init__(self, vocabulary):
        # load data
        models_folder = os.path.join(*[os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'models'])
        corpora_folder = os.path.join(*[os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'corpora'])
        self.vocabulary = vocabulary
        self.filename = "HDPmodel_%s" % (vocabulary, )
        self.dictionary = corpora.Dictionary.load(os.path.join(corpora_folder, "%s.dict" % (vocabulary,)))
        self.corpus = corpora.MmCorpus(os.path.join(corpora_folder, "%s.mm" % (vocabulary,)))

        # does identical model already exists?
        model_exists = os.path.isfile(os.path.join(models_folder, self.filename))
        if model_exists:
            # if model already exists then load it
            print "loading model.."
            self.model = models.LdaModel.load(os.path.join(models_folder, self.filename))
        else:
            # train model with given parameters
            print "training model.."
            self.model = self.train()
            # save model state to file
            print "saving model.."
            self.model.save(os.path.join(models_folder, self.filename))

        # transform corpus to latent variable vectors
        print "transforming documents to latent space.."
        self.latent_docs = []
        count = 1
        for doc in self.corpus:
            self.latent_docs.append(self.model[doc])
            count += 1
            if count % 1000 == 0:
                print count, "converted.."


    def train(self):
        """
        Train the HDP model
        :param n_passes: number of training passes
        :param update_every: training batch size
        :return: trained model
        """
        hdp_model = models.HdpModel(self.corpus,
                                    id2word=self.dictionary)
        return hdp_model

    def query(self, query_tokens, top_n=10):
        """
        Get the top N ranked document ids.
        :param query_tokens: List of query token strings
        :param top_n: the number of top ranked docids returned
        :return: top ranked document ids
        """
        # convert query tokens to Bag-Of-Word (BOW) vector
        bow = self.dictionary.doc2bow(query_tokens)
        # transform BOW vector to latent variable space
        latent_vector = self.model[bow]
        # rank document by Kullback-Leibler divergence
        ranking = []
        p = sparse2full(latent_vector, self.n_topics)
        print p
        for i in range(len(self.latent_docs)):
            q = sparse2full(self.latent_docs[i], self.n_topics)
            score = kl_divergence(p, q)
            ranking.append((i, score))

        ranking.sort(key=lambda x: x[1])

        return ranking[:top_n]

if __name__ == "__main__":
    # setup logging
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    # model parameters
    model = HDPmodel(vocabulary="combined")
