__author__ = 'matias'

import xml.etree.ElementTree as ET
from nltk import word_tokenize
import os.path
import pickle


class TokenTrie(object):
    def __init__(self):
        self.path = {}
        # try to load from cache
        if os.path.isfile("trie.cache"):
            try:
                print "loading trie cache.."
                self.path = pickle.load(open("trie.cache"))
            except:
                raise IOError("not good!")
            print "succesfully loaded trie cache.."

    def is_empty(self):
        return self.path == {}

    def add(self,seq):
        head = self.path
        for token in seq:
            if head.get(token):
                head = head[token]
            else:
                head[token] = {}
                head = head[token]
        head[True] = True

    def save_to_cache(self):
        with open("trie.cache",'w') as outfile:
            pickle.dump(self.path, outfile)

    def scan(self,seq):
        found_seqs = []
        while seq:
            token = seq.pop(0)
            if token in self.path:
                # try to find a match
                match = [token]
                step = 0
                head = self.path[token]
                if True in head and match:
                    # pass list by value
                    found_seqs.append(match[:])
                while len(seq)>step and seq[step] in head:
                    print seq[step]
                    match.append(seq[step])
                    head = head[seq[step]]
                    step += 1
                    if True in head:
                        found_seqs.append(match)
        # get longest sequence
        return found_seqs



class DiseaseExtractor(object):
    def __init__(self):
        self.trie = TokenTrie()
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

class CaseReports(object):
    def __init__(self,section='A-B', filename=None):
        with open("case_report_list_%s.txt" % section) as infile:
            self.filenames = infile.read().split("\n")
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




ab_cases = CaseReports('A-B', r"C:\Users\matias\Desktop\thesis\data\pubmed\articles.A-B\Ann_Gastroenterol\Ann_Gastroenterol_2013_26(2)_165.nxml")
d_extractor = DiseaseExtractor()



for body in ab_cases:
    print body
    print d_extractor.extract(body)


"""
for i in range(50):
    t = TokenTrie()
    t.add(word_tokenize("slemt lunge prut"))
    t.add(word_tokenize("slemt slemhed"))
    t.add(word_tokenize("slemt"))
    t.add(word_tokenize("bums"))
    t.add(word_tokenize("lunge prut"))

    text = "bums slemt det er et eksempel af slemt slemhed i maven og slemt lunge prut i halsen"
    hits = t.scan(word_tokenize(text))

    print text
    print hits
    print ""
"""