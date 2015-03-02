__author__ = 'matias'

import os
from pubmed_tokenize import tokenize
from irdatastructs import TokenTrie


class DiseaseExtractor(object):
    def __init__(self):
        self.trie = TokenTrie(name="disease")
        if self.trie.is_empty():
            diseases_file = open(os.path.join(*[os.path.dirname(__file__), 'data', 'UMLS', 'diseases.txt']))
            disease_names = diseases_file.read().split('\n')
            count = 0
            for disease in disease_names:
                self.trie.add(tokenize(disease))
                print disease
                count += 1
            self.trie.save_to_cache()

    def extract(self, text):
        sequences = self.trie.scan(tokenize(text))
        # assemble sequences into tokens
        return [" ".join(seq) for seq in sequences]


class SymptomExtractor(object):
    def __init__(self):
        self.trie = TokenTrie(name="symptoms")
        if self.trie.is_empty():
            symptoms_file = open(os.path.join(*[os.path.dirname(__file__), 'data', 'UMLS', 'diseases.txt']))
            symptoms = symptoms_file.read().split('\n')
            count = 0
            for symptom in symptoms:
                (code, name) = symptom.split("\t")
                self.trie.add(tokenize(name))
                print name
                count += 1
            self.trie.save_to_cache()

    def extract(self, text):
        sequences = self.trie.scan(tokenize(text))
        # assemble sequences into tokens
        return [" ".join(seq) for seq in sequences]

