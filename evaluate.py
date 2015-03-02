__author__ = 'matias'


from textanalysis.texts import CaseReportLibrary
from textanalysis.Analyzers import EntityAnalyzer
from irmodels.LDAmodel import LDAmodel


cases = CaseReportLibrary()

model = LDAmodel(n_topics=500, n_passes=200, vocabulary="entity")

analyzer = EntityAnalyzer()

for i in range(100):
    print model.model.print_topic(i)

"""
query_str = raw_input("search: ")
while query_str:
    query_tokens = analyzer.parse(query_str)
    print query_tokens
    ranked_docs = model.query(query_tokens)

    print ""
    print "Results:"
    for doc in ranked_docs:
        print doc[0], doc[1], cases[doc[0]]

    print "-----"
    query_str = raw_input("search: ")
"""