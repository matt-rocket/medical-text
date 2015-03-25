__author__ = 'matias'

import xml.etree.ElementTree as ET
import logging
from nltk.tokenize import sent_tokenize
from pubmed_tokenize import SimpleTokenizer, RawTokenizer
from gensim.models.doc2vec import LabeledSentence
import os
from os.path import isfile, join
import json


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
    def __init__(self, extract_func=None):
        self.docs = CaseReportLibrary()
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
    def __init__(self, phrase_detector, extract_func=None):
        self.stream = RawSentenceStream(extract_func=extract_func)
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


class CaseReportLibrary(object):
    def __init__(self, filename=None, cs_path=r"C:\Users\matias\Desktop\thesis\data\casereports"):
        if filename is not None:
            self.filenames = [filename]
        else:
            self.filenames = [join(cs_path, f) for f in os.listdir(cs_path) if isfile(join(cs_path, f))]


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

    def __len__(self):
        return len(self.filenames)


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


class FZArticleLibrary(object):
    def __init__(self, filename=None, cs_path=r"C:\Users\matias\Desktop\thesis\medical-text\data\articles\findzebra"):
        if filename is not None:
            self.filenames = [filename]
        else:
            self.filenames = [join(cs_path, f) for f in os.listdir(cs_path) if isfile(join(cs_path, f))]

    def __getitem__(self, item):
        return self.filenames[item]

    def __iter__(self):
        for filename in self.filenames:
            obj = json.load(open(filename, 'r'))
            title = obj['title']
            content = obj['content']
            _id = obj['id']
            print title, _id
            yield FZArticle(title=title, content=content, _id=_id)


class FZArticle(object):
    def __init__(self, title, content, _id):
        self.body = content
        self.title = title
        self.id = _id

    def get_text(self):
        """
        :return: string containing all text in case report
        """
        return " ".join([self.title, self.body])


class RareDiseases(set):
    def __init__(self):
        tree = ET.parse("../../data/orphanet/rare_diseases.xml")
        root = tree.getroot()
        names = root.findall('./DisorderList/Disorder/Name')
        for name in names:
            print name.text


def extract_docid(doc):
    return [doc.title]


def extract_mesh_terms(doc):
    return doc.mesh_terms