__author__ = 'matias'

from gensim import corpora, models
from gensim.matutils import sparse2full
from scoring import kl_divergence
import os
import logging
import pickle


class LDAmodel(object):
    """
    IR models based on Latent Dirichlet Allocation
    """
    def __init__(self, n_topics, n_passes, vocabulary):
        # load data
        models_folder = os.path.join(*[os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'models'])
        corpora_folder = os.path.join(*[os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'corpora'])
        self.n_topics = n_topics
        self.vocabulary = vocabulary
        self.filename = "LDAmodel_%s_%s_%s" % (vocabulary, n_topics, n_passes,)
        self.latent_space_filename = "LATENT_SPACE_LDAmodel_%s_%s_%s" % (vocabulary, n_topics, n_passes,)
        self.dictionary = corpora.Dictionary.load(os.path.join(corpora_folder, "%s.dict" % (vocabulary,)))
        self.corpus = corpora.MmCorpus(os.path.join(corpora_folder, "%s.mm" % (vocabulary,)))

        # does identical model already exists?
        model_exists = os.path.isfile(os.path.join(models_folder, self.filename))
        if model_exists:
            # if model already exists then load it
            logging.info("LOADING LDA model from file")
            self.model = models.LdaModel.load(os.path.join(models_folder, self.filename))
        else:
            # train model with given parameters
            logging.info("STARTING TRAINING - LDA model")
            self.model = self.train(n_topics, n_passes)
            # save model state to file
            logging.info("SAVING LDA model")
            self.model.save(os.path.join(models_folder, self.filename))


        # does identical model already exists?
        latent_docs_path = os.path.join(models_folder, self.latent_space_filename)
        latent_docs_exists = os.path.isfile(latent_docs_path)

        if latent_docs_exists:
            # load latent vectors from file
            logging.info("loading latent space vectors..")
            self.latent_docs = pickle.load(open(latent_docs_path, 'r'))
        else:
            # transform corpus to latent variable vectors
            logging.info("transforming documents to latent space..")
            self.latent_docs = []
            count = 1
            for doc in self.corpus:
                self.latent_docs.append(self.model[doc])
                count += 1
                if count % 1000 == 0:
                    print count, "converted.."
            # save to file
            pickle.dump(self.latent_docs, open(latent_docs_path, 'w'))

    def tokens2latent(self, tokens):
        return self.model[self.dictionary.doc2bow(tokens)]

    def train(self, n_topics, n_passes, update_every=0):
        """
        Train the LDA model
        :param n_topics: number of LDA topics
        :param n_passes: number of training passes
        :param update_every: training batch size
        :return: trained model
        """
        lda_model = models.LdaModel(self.corpus,
                                    num_topics=n_topics,
                                    update_every=update_every,
                                    passes=n_passes,
                                    id2word=self.dictionary)
        return lda_model

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

    model = LDAmodel(n_topics=30, n_passes=10, vocabulary="standard")

    model.model.print_topics()

