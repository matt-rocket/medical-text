__author__ = 'matias'

from gensim import corpora, models
from gensim.matutils import sparse2full
from PubMedParser.entityextractor import DiseaseExtractor, SymptomExtractor
from scoring import kl_divergence
import os
import logging


class LDAmodel(object):
    def __init__(self, n_topics, n_passes, vocabulary):
        # load data
        models_folder = os.path.join(*[os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'models'])
        corpora_folder = os.path.join(*[os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'corpora'])
        self.vocabulary = vocabulary
        self.filename = "LDAmodel_%s_%s_%s" % (vocabulary, n_topics, n_passes,)
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
            self.model = self.train(n_topics, n_passes)
            # save model state to file
            print "saving model.."
            self.model.save(os.path.join(models_folder, self.filename))

        # transform corpus to latent variable vectors
        print "transforming documents to latent space.."
        self.latent_docs = [self.model[doc] for doc in self.corpus]

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

    def query(self, query, top_n=10):
        """
        Get the top N ranked document ids.
        :param query: The query string
        :param top_n: the number of top ranked docids returned
        :return: top ranked document ids
        """
        d_extractor = DiseaseExtractor()
        s_extractor = SymptomExtractor()
        doc = list(set(d_extractor.extract(query) + s_extractor.extract(query)))
        # convert query to Bag-Of-Word (BOW) vector
        bow = self.dictionary.doc2bow(doc)
        # transform BOW vector to latent variable space
        latent_vector = self.model[bow]
        ranking = []
        p = sparse2full(latent_vector,10)
        for i in range(len(self.latent_docs)):
            q = sparse2full(self.latent_docs[i],10)
            ranking.append((i, kl_divergence(p, q)))

        ranking.sort(key=lambda x: x[1])

        return ranking[:500]

if __name__ == "__main__":
    # setup logging
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    # model parameters
    model = LDAmodel(n_topics=10, n_passes=100, vocabulary="entity")

    """
    for i in range(10):
        print model.model.print_topic(i, topn=100)
    """
    from PubMedParser.entityextractor import CaseReportLibrary
    cases = CaseReportLibrary()

    ranked_docs = model.query("HIV hiv AIDS aids human immunodeficiency virus acquired immune deficiency syndrome Human immunodeficiency virus infection human immunodeficiency virus infection")
    for doc in ranked_docs:
        print doc[1], cases[doc[0]]