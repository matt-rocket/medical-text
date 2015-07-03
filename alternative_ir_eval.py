__author__ = 'Matias'


from textanalysis.texts import CaseReportLibrary, RawSentenceStream, PhraseSentenceStream
from textanalysis.texts import extract_docid
from textanalysis.phrasedetection import PmiPhraseDetector
from irmodels.D2Vmodel import D2Vmodel, DocIndex
from scipy.spatial.distance import cosine
import logging
import random

# setup logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
# phrase detector

pmis = [50, 100, 150, 200]

for pmi in pmis:

    phrase_detector = PmiPhraseDetector(RawSentenceStream(fz_docs=False),
                                        filename=str("PHRASE_%s_2_CASEREPORT_RAW") % (pmi, ))

    dims = [20]#, 25, 30, 35, 40, 45, 50]

    for dim in dims:
        # build model
        epochs = 2
        m = D2Vmodel(
            PhraseSentenceStream(phrase_detector, extract_func=extract_docid, fz_docs=False, reshuffles=epochs-1),
            name="DOCID",
            dataset_name="CASEREPORT",
            epochs=epochs,
            modelfile=str("DOC2VEC_CASEREPORT-PMI%s_DOCID_2" % (pmi, )),
            dimension=dim)

        doc_index = DocIndex(CaseReportLibrary(), "CASEREPORT")

        count = 0
        docid2vec = {}
        for case in CaseReportLibrary():
            docid = case.get_id()
            if docid in m.inner_model.vocab:
                vec = m.inner_model[docid]
                docid2vec[docid] = vec
            count += 1
            #print count, docid
            if count >= 20000:
                break


        count = 0
        false_count = 0
        for case in CaseReportLibrary():
            docid = case.get_id()
            if docid not in docid2vec:
                continue
            abstract = case.get_abstract()
            try:
                abstract_vec = m.infer_doc_vector(abstract, steps=10, phrase_detector=phrase_detector)
            except UnicodeDecodeError:
                continue

            true_vec = docid2vec[docid]
            true_distance = cosine(abstract_vec, true_vec)

            # get random non case vector

            wrong_docids = [random.choice(docid2vec.keys()) for i in range(5)]
            wrong_vecs = [docid2vec[docid] for docid in wrong_docids]
            wrong_distances = [cosine(abstract_vec, vec) for vec in wrong_vecs]

            correct = all([true_distance < dist for dist in wrong_distances])

            count += 1
            if not correct:
                false_count += 1
            if count > 1000:
                break
        print "Error rate:", float(false_count)/count, dim