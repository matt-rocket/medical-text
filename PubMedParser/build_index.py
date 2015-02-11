__author__ = 'matias'

from entityextractor import CaseReports, DiseaseExtractor, SymptomExtractor
from irdatastructs import InvertedIndex

index = InvertedIndex("disease")

cases = CaseReports()
d_extractor = DiseaseExtractor()
s_extractor = SymptomExtractor()

count = 0
for body in cases:
    count += 1
    diseases = [" ".join(words) for words in d_extractor.extract(body)]
    index.add(diseases,count)
    print "added", count

index.save()
