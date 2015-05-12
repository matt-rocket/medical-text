__author__ = 'matias'

import xml.etree.ElementTree as ET
import logging
from nltk.tokenize import sent_tokenize
from pubmed_tokenize import SimpleTokenizer, RawTokenizer
from gensim.models.doc2vec import LabeledSentence
import os
from os.path import isfile, join
import json
from random import shuffle
from entityextractor import DiseaseExtractor


class SentenceStream(object):
    def __init__(self):
        self.docs = CaseReportLibrary()
        self.tokenizer = SimpleTokenizer()

    def __iter__(self):
        doc_count = len(self.docs)
        count = 0
        for doc in self.docs:
            for sentence in sent_tokenize(doc.get_text().lower()):
                tokens = self.tokenizer.tokenize(sentence)
                yield tokens
            count += 1
            logging.info(msg="%s/%s documents streamed" % (count, doc_count, ))


class RawSentenceStream(object):
    def __init__(self, extract_func=None, fz_docs=False, reshuffles=0):
        self.docs = FZArticleLibrary(reshuffles=reshuffles) if fz_docs else CaseReportLibrary(reshuffles=reshuffles)
        self.tokenizer = RawTokenizer()
        self.extract_func = extract_func

    def __iter__(self):
        doc_count = len(self.docs)
        count = 0
        for doc in self.docs:
            for sentence in sent_tokenize(doc.get_text().lower()):
                tokens = self.tokenizer.tokenize(sentence)
                if self.extract_func is not None:
                    labeled_tokens = LabeledSentence(words=tokens, labels=self.extract_func(doc))
                    yield labeled_tokens
                else:
                    yield tokens
            count += 1
            logging.info(msg="%s/%s documents streamed" % (count, doc_count, ))


class PhraseSentenceStream(object):
    def __init__(self, phrase_detector, extract_func=None, fz_docs=False, reshuffles=0):
        self.stream = RawSentenceStream(extract_func=extract_func, fz_docs=fz_docs, reshuffles=reshuffles)
        self.detector = phrase_detector
        self.is_labeled = extract_func is not None

    def __iter__(self):
        for sentence in self.stream:
            # detect phrases in sentence/labeled sentence
            if self.is_labeled:
                sentence.words = self.detector.detect(sentence.words)
            else:
                sentence = self.detector.detect(sentence)
            yield sentence


class Document(object):

    def get_text(self):
        raise NotImplementedError()

    def get_id(self):
        raise NotImplementedError()


class CaseReportLibrary(object):
    def __init__(self, filename=None, cs_path=r"C:\Users\matias\Desktop\thesis\data\casereports", reshuffles=0):
        if filename is not None:
            self.filenames = [filename]
        else:
            docs = [join(cs_path, f) for f in os.listdir(cs_path) if isfile(join(cs_path, f))]
            self.filenames = docs[:]
            for i in range(reshuffles):
                reordered_docs = docs[:]
                shuffle(reordered_docs)
                self.filenames += reordered_docs

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
            _id = root.find('./front/article-meta/article-id[@pub-id-type="pmid"]')
            pmcid = root.find('./front/article-meta/article-id[@pub-id-type="pmc"]')
            keywords = root.findall('./front/article-meta/kwd-group/kwd')
            abstract = root.find('./front/article-meta/abstract')
            if _id is not None:
                _id = ET.tostring(_id, encoding='utf8', method='text')
            if pmcid is not None:
                pmcid = ET.tostring(pmcid, encoding='utf8', method='text')
            if title is not None:
                title = ET.tostring(title, encoding='utf8', method='text')
            if abstract is not None:
                abstract = ET.tostring(abstract, encoding='utf8', method='text')
            if keywords is not None:
                keywords = [ET.tostring(kwd, encoding='utf8', method='text') for kwd in keywords]
            body_node = root.find('./body')
            if body_node is not None and _id is not None:
                body = ET.tostring(body_node, encoding='utf8', method='text').replace("\n", " ")
                yield CaseReport(_id, pmcid, title, body, filename, keywords, abstract)
            else:
                continue

    def __len__(self):
        return len(self.filenames)


class CaseReport(Document):
    def __init__(self, _id, pmcid, title, body, filename, mesh_terms, abstract):
        self.id = _id
        self.pmcid = pmcid
        self.id_prefix = "DOCID-CS"
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
            try:
                sequences = extractor.extract(self.body) + extractor.extract(self.title) + extractor.extract(self.abstract)
                for term in self.mesh_terms:
                    sequences += extractor.extract(term)
                entities = [term for term in set(sequences) if term is not "1"]
                return entities
            except UnicodeDecodeError:
                return []
        else:
            return []

    def get_text(self):
        """
        :return: string containing all text in case report
        """
        return " ".join([self.title, " ".join(self.mesh_terms), self.abstract, self.body]).decode('utf-8')

    def get_id(self):
        return self.id_prefix + self.id

    def get_pmcid(self):
        return self.pmcid

    def get_abstract(self):
        return self.abstract if self.abstract is not None else ""


class FZArticleLibrary(object):
    def __init__(self, filename=None, cs_path=r"C:\Users\matias\Desktop\thesis\medical-text\data\articles\findzebra", reshuffles=0):
        if filename is not None:
            self.filenames = [filename]
        else:
            docs = [join(cs_path, f) for f in os.listdir(cs_path) if isfile(join(cs_path, f))]
            self.filenames = docs[:]
            for i in range(reshuffles):
                reordered_docs = docs[:]
                shuffle(reordered_docs)
                self.filenames += reordered_docs

    def __getitem__(self, item):
        return self.filenames[item]

    def __iter__(self):
        for filename in self.filenames:
            obj = json.load(open(filename, 'r'))
            title = obj['title']
            content = obj['content']
            _id = obj['id']
            yield FZArticle(title=title, content=content, _id=_id)

    def __len__(self):
        return len(self.filenames)


class FZArticle(Document):
    def __init__(self, title, content, _id):
        self.id_prefix = "DOCID-FZ"
        self.body = content
        self.title = title
        self.id = _id

    def get_text(self):
        """
        :return: string containing all text in case report
        """
        return ". ".join([self.title, self.body])

    def get_id(self):
        return self.id_prefix + self.id

    def get_entities(self, extractor):
        return []

class RareDiseases(set):
    def __init__(self):
        tree = ET.parse("../../data/orphanet/rare_diseases.xml")
        root = tree.getroot()
        names = root.findall('./DisorderList/Disorder/Name')
        for name in names:
            print name.text


def extract_docid(doc):
    return [doc.get_id()]


def extract_mesh_terms(doc):
    return ["MESH-"+str(term) for term in doc.mesh_terms]

class ExtractDiseases(object):

    def __init__(self):
        self.disease_extractor = DiseaseExtractor()
        self.cached_doc = None
        self.cache = None

    def __call__(self, *args, **kwargs):
        doc = args[0]
        doc_id = doc.get_id()
        if doc_id == self.cached_doc:
            return self.cache
        else:
            entities = doc.get_entities(extractor=self.disease_extractor)
            entities = ["DISEASE-"+entity for entity in entities]
            self.cache = entities
            self.cached_doc = doc_id
            return entities