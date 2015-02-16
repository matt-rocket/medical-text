__author__ = 'matias'

from entityextractor import CaseReports, DiseaseExtractor
import solr

solr_con = solr.SolrConnection('http://localhost:8983/solr')

d_extractor = DiseaseExtractor()

case_reports = CaseReports()

count = 0
hits = 0
for (title,body,filename) in case_reports:
    count += 1
    if title and d_extractor.extract(title):
        hits += 1
        print hits,"/",count,title
        print d_extractor.extract(title)
