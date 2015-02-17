__author__ = 'matias'

from gensim import models, corpora, similarities

from PubMedParser.entityextractor import CaseReportLibrary

texts = []
count = 1
max_count = 3000
print "reading case reports.."
for case in CaseReportLibrary():
    texts.append(case.mesh_terms)
    count += 1
    if count % 100 == 0:
        print count,"/",max_count
    if count >= max_count:
        break

dictionary = corpora.Dictionary(texts)

for text in texts:
    print dictionary.doc2bow(text)
