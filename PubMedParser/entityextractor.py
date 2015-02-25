__author__ = 'matias'

import os
import xml.etree.ElementTree as ET
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


class CaseReportLibrary(object):
    def __init__(self, filename=None):
        sections = ['A-B', 'C-H', 'I-N', 'O-Z']
        self.filenames = []
        for section in sections:
            section_filepath = os.path.join(*[os.path.dirname(__file__), "data", "casereportlists",  "case_report_list_%s.txt"]) % section
            with open(section_filepath) as infile:
                self.filenames += infile.read().split("\n")
        if filename:
            self.filenames = [filename]

    def __getitem__(self, item):
        tree = ET.parse(self.filenames[item])
        root = tree.getroot()
        title = root.find('./front/article-meta/title-group/article-title')
        title = ET.tostring(title, encoding='utf8', method='text')
        return title

    def __iter__(self):
        for filename in self.filenames:
            tree = ET.parse(filename)
            root = tree.getroot()
            title = root.find('./front/article-meta/title-group/article-title')
            keywords = root.findall('./front/article-meta/kwd-group/kwd')
            abstract = root.find('./front/article-meta/abstract')
            if title is not None:
                title = ET.tostring(title, encoding='utf8', method='text')
            if abstract is not None:
                abstract = ET.tostring(abstract, encoding='utf8', method='text')
            if keywords is not None:
                keywords = [ET.tostring(kwd, encoding='utf8', method='text') for kwd in keywords]
            body_node = root.find('./body')
            if body_node is not None:
                body = ET.tostring(body_node, encoding='utf8', method='text').replace("\n", " ")
                yield CaseReport(title, body, filename, keywords, abstract)
            else:
                continue


class CaseReport(object):
    def __init__(self, title, body, filename, mesh_terms, abstract):
        self.title = title if title is not None else ""
        self.body = body if body is not None else ""
        self.abstract = abstract if abstract is not None else ""
        self.filename = filename if filename is not None else ""
        self.mesh_terms = mesh_terms if mesh_terms is not None else []

    def get_entities(self, extractor):
        """
        :param extractor: the entity extractor
        :return: list of strings
        """
        if self.title or self.body or self.abstract:
            sequences = extractor.extract(self.body) + extractor.extract(self.title) + extractor.extract(self.abstract)
            for term in self.mesh_terms:
                sequences += extractor.extract(term)
            entities = list(set([" ".join(seq) for seq in sequences]))
            return entities
        else:
            return []

    def get_text(self):
        """
        :return: string containing all text in case report
        """
        return " ".join([self.title, " ".join(self.mesh_terms), self.abstract, self.body])


class RareDiseases(set):
    def __init__(self):
        tree = ET.parse("../../data/orphanet/rare_diseases.xml")
        root = tree.getroot()
        names = root.findall('./DisorderList/Disorder/Name')
        for name in names:
            print name.text
