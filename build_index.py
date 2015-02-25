__author__ = 'matias'

from entityextractor import CaseReportLibrary, DiseaseExtractor, SymptomExtractor
from irdatastructs import InvertedIndex

d_index = InvertedIndex("disease")
s_index = InvertedIndex("symptom")

cases = CaseReportLibrary()
d_extractor = DiseaseExtractor()
s_extractor = SymptomExtractor()

count = 0
max_count = 50000
for case in cases:
    text = case.get_text()
    count += 1
    symptoms = list(set(s_extractor.extract(text)))
    diseases = list(set(d_extractor.extract(text)))
    s_index.add(symptoms,count)
    d_index.add(diseases,count)
    if count >= max_count:
        break
    print count,"/",max_count
    print symptoms + diseases

s_index.save()
d_index.save()