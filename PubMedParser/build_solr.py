__author__ = 'matias'

from entityextractor import CaseReport, CaseReportLibrary, DiseaseExtractor
import solr

solr_con = solr.SolrConnection('http://localhost:8983/solr')

d_extractor = DiseaseExtractor()

case_reports = CaseReportLibrary()

count = 0
hits = 0

for case_report in case_reports:
    count += 1
    print "added",count
    solr_con.add(_commit=False, id=count,
                 title=case_report.title.decode('utf-8'),
                 description=case_report.abstract.decode('utf-8'),
                 text=case_report.body.decode('utf-8'),
                 keywords=",".join(case_report.mesh_terms).decode('utf-8'),
                 resourcename=case_report.filename,
                 )

solr_con.commit()
