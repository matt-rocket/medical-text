__author__ = 'matias'


from textanalysis.texts import CaseReportLibrary, RawSentenceStream, PhraseSentenceStream
from textanalysis.texts import extract_mesh_terms
from textanalysis.pubmed_tokenize import tokenize
from textanalysis.entityextractor import DiseaseExtractor, SymptomExtractor


symptom_extractor = SymptomExtractor()
disease_extractor = DiseaseExtractor()

doc_lengths = []
diseases = []
symptoms = []


count = 0
has_mesh = 0
for case in CaseReportLibrary():
    text = case.get_text()
    doc_lengths.append(len(tokenize(text)))
    diseases += disease_extractor.extract(text)
    symptoms += symptom_extractor.extract(text)
    mesh_terms = extract_mesh_terms(case)
    count += 1
    if mesh_terms:
        has_mesh += 1
    print count


diseases = set(diseases)
symptoms = set(symptoms)

print "Avg doc length:", sum(doc_lengths)/float(count)
print "Diseases:", len(diseases)
print "Symptoms:", len(symptoms)
print "Has MeSH terms:", 100 * float(has_mesh)/count, "%"
