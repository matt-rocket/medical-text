__author__ = 'matias'


from textanalysis.entityextractor import CaseReportLibrary
from textanalysis.Analyzers import EntityAnalyzer
from irmodels.LDAmodel import LDAmodel


cases = CaseReportLibrary()

model = LDAmodel(n_topics=20, n_passes=100, vocabulary="entity")

analyzer = EntityAnalyzer()


query_str = raw_input("search: ")
while query_str:
    query_tokens = analyzer.parse(query_str)
    print query_tokens
    ranked_docs = model.query(query_tokens)

    print ""
    print "Results:"
    for doc in ranked_docs:
        print cases[doc[0]]

    print "-----"
    query_str = raw_input("search: ")
