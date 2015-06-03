__author__ = 'Matias'

from irmodels.D2Vmodel import D2Vmodel, InferredIndex, DocIndex
from textanalysis.texts import CaseReportLibrary, RawSentenceStream, PhraseSentenceStream, extract_docid
from textanalysis.phrasedetection import PmiPhraseDetector
from scipy.spatial.distance import cosine
from heapq import heappush, heappop
import logging


class CSRecommender(object):
    def __init__(self):
        pass

if __name__ == "__main__":
    # setup logging
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    # phrase detector
    phrase_detector = PmiPhraseDetector(RawSentenceStream(fz_docs=False))

    filename = r"C:\Users\matias\Desktop\thesis\data\casereports\Adv_Hematol_2010_Jun_16_2010_601548.nxml"
    filename = r"C:\Users\matias\Desktop\thesis\data\casereports\Ann_Gastroenterol_2014_27(4)_418-420.nxml"
    filename = r"C:\Users\matias\Desktop\thesis\data\casereports\Case_Rep_Ophthalmol_2011_Apr_22_2(1)_129-133.nxml"
    filename = r"C:\Users\matias\Desktop\thesis\data\casereports\Case_Rep_Orthop_2011_Sep_26_2011_492407.nxml"
    # filename = r"C:\Users\matias\Desktop\thesis\data\casereports\Adv_Urol_2010_May_10_2010_276497.nxml"
    # filename = r"C:\Users\matias\Desktop\thesis\data\casereports\Adv_Urol_2008_Oct_28_2008_173694.nxml"

    case_reports = CaseReportLibrary()

    # build model
    epochs = 10
    m = D2Vmodel(
        PhraseSentenceStream(phrase_detector, extract_func=extract_docid, fz_docs=True, reshuffles=epochs-1),
        name="DOCID",
        dataset_name="FINDZEBRA",
        epochs=epochs)

    fz_index = DocIndex(case_reports, "FINDZEBRA")
    cs_index = DocIndex(case_reports, "CASEREPORT")
    infer_index = InferredIndex(case_reports, "CASEREPORT", m, phrase_detector)

    for docid in infer_index:
        print cs_index[docid]
        print "--------------"

        cs_vec = infer_index[docid]

        top_n = 10
        ranking = []

        for word in m.inner_model.vocab:
            if word.startswith("DOCID-FZ"):
                doc_vec = m.inner_model[word]
                distance = cosine(cs_vec, doc_vec)
                heappush(ranking, (distance, fz_index[word]))

        # make top results similar to Solr results
        top_ranked = [heappop(ranking) for i in range(top_n)]
        for entry in top_ranked:
            print entry