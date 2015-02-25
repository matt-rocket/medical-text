__author__ = 'matias'


from textanalysis.entityextractor import CaseReportLibrary
from irmodels.LDAmodel import LDAmodel

cases = CaseReportLibrary()

model = LDAmodel(n_topics=10, n_passes=10, vocabulary="standard")

ranked_docs = model.query(["poison poisoned poisonous poisons antidote antidotes"])
for doc in ranked_docs:
    print doc[1], cases[doc[0]]
