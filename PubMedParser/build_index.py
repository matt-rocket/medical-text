__author__ = 'matias'

from entityextractor import CaseReports, DiseaseExtractor, SymptomExtractor
from irdatastructs import InvertedIndex

d_index = InvertedIndex("disease")
s_index = InvertedIndex("symptom")

cases = CaseReports()
d_extractor = DiseaseExtractor()
s_extractor = SymptomExtractor()


count = 0
max_count = 1
for (title, body, filename) in cases:
    count += 1
    symptoms = [" ".join(words) for words in s_extractor.extract(body)]
    diseases = [" ".join(words) for words in d_extractor.extract(body)]
    s_index.add(symptoms,count)
    d_index.add(diseases,count)
    if count >= max_count:
        break

s_index.save()
d_index.save()