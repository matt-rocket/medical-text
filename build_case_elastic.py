__author__ = 'matias'

from textanalysis.texts import CaseReportLibrary
import elasticsearch
import json
import os

es = elasticsearch.Elasticsearch()

index_name = "casereports_snowball"

mappings_path = os.path.join("elasticsearch", "mappings.json")
settings_path = os.path.join("elasticsearch", str("settings_%s.json" % (index_name,)))

mappings = json.load(file(mappings_path, 'r'))
settings = json.load(file(settings_path, 'r'))

if es.indices.exists(index_name):
    es.indices.delete(index_name)

es.indices.create(index_name,
                  body={'mappings':mappings, 'settings':settings}
                )

count = 0
for case in CaseReportLibrary():
    title = case.title
    text = case.get_text()
    cui = case.get_id()
    pmcid = case.get_pmcid()
    abstract = case.get_abstract()
    filename = case.filename
    es.index(index_name, doc_type='casereport', id=cui, body={
        'title': title,
        'text': text,
        'filename': filename,
        'cui': cui,
        'pmcid': pmcid,
        'abstract': abstract,
    })
    count += 1
    print count, filename
