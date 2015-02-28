__author__ = 'matias'

from entityextractor import DiseaseExtractor, SymptomExtractor
from pubmed_tokenize import stopwords, tokenize


class EntityAnalyzer(object):

    def __init__(self):
        self.extractors = [DiseaseExtractor(), SymptomExtractor()]

    def parse(self, text):
        tokens = []
        for extractor in self.extractors:
            tokens += extractor.extract(text)
        return tokens


class StandardAnalyzer(object):

    def __init__(self):
        self.stopwords = stopwords("pubmed_v3")

    def parse(self, text):
        # lowercase query
        text = text.lower()
        tokens = tokenize(text)
        # remove stopwords
        tokens = [token for token in tokens if token not in self.stopwords]
        return tokens


class CombinedAnalyzer(object):

    def __init__(self):
        self.sub_analyzers = [StandardAnalyzer(), EntityAnalyzer()]

    def parse(self, text):
        tokens = []
        for analyzer in self.sub_analyzers:
            tokens += analyzer.parse(text)
        return tokens