__author__ = 'matias'

import xml.etree.ElementTree as ET
from nltk import word_tokenize
from irdatastructs import TokenTrie

class DiseaseExtractor(object):
    def __init__(self):
        self.trie = TokenTrie(name="disease")
        if self.trie.is_empty():
            disease_names = open('../../data/UMLS/diseases.txt').read().split('\n')
            count = 0
            for disease in disease_names:
                self.trie.add(word_tokenize(disease))
                print disease
                count += 1
            self.trie.save_to_cache()

    def extract(self, text):
        return self.trie.scan(word_tokenize(text))

class SymptomExtractor(object):
    def __init__(self):
        self.trie = TokenTrie(name="symptoms")
        if self.trie.is_empty():
            symptoms = open('../../data/UMLS/symptoms.txt').read().split('\n')
            count = 0
            for symptom in symptoms:
                (code,name) = symptom.split("\t")
                self.trie.add(word_tokenize(name))
                print name
                count += 1
            self.trie.save_to_cache()

    def extract(self, text):
        return self.trie.scan(word_tokenize(text))

class CaseReports(object):
    def __init__(self, filename=None):
        sections = ['A-B', 'C-H', 'I-N', 'O-Z']
        self.filenames = []
        for section in sections:
            with open("case_report_list_%s.txt" % section) as infile:
                self.filenames += infile.read().split("\n")
        if filename:
            self.filenames = [filename]

    def __iter__(self):
        for filename in self.filenames:
            tree = ET.parse(filename)
            root = tree.getroot()
            title = root.find('./front/article-meta/title-group/article-title').text
            body_node = root.find('./body')
            if body_node is not None:
                body = ET.tostring(body_node,encoding='utf8',method='text').replace("\n", " ")
                yield body
            else:
                continue

class RareDiseases(set):
    def __init__(self):
        tree = ET.parse("../../data/orphanet/rare_diseases.xml")
        root = tree.getroot()
        names = root.findall('./DisorderList/Disorder/Name')
        for name in names:
            print name.text


