__author__ = 'matias'

import xml.etree.ElementTree as ET
from nltk import word_tokenize



class TokenTrie(object):
    def __init__(self):
        self.path = {}

    def add(self,seq):
        head = self.path
        for token in seq:
            if head.get(token):
                head = head[token]
            else:
                head[token] = {}
                head = head[token]
        head[True] = True

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
                while seq and seq[step] in head:
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
        disease_names = open('../../data/UMLS/diseases.txt').read().split('\n')
        count = 0
        for disease in disease_names:
            self.trie.add(word_tokenize(disease))
            print disease
            count += 1
            #if count > 100000:
            #    break

    def extract(self, text):
        return self.trie.scan(word_tokenize(text))

class CaseReports(object):
    def __init__(self,section='A-B'):
        with open("case_report_list_%s.txt" % section) as infile:
            self.filenames = infile.read().split("\n")

    def __iter__(self):
        for filename in self.filenames:
            tree = ET.parse(filename)
            root = tree.getroot()
            title = root.find('./front/article-meta/title-group/article-title').text
            body_node = root.find('./body')
            body = ET.tostring(body_node,encoding='utf8',method='text').replace("\n", " ")
            yield body




ab_cases = CaseReports('A-B')
d_extractor = DiseaseExtractor()

print d_extractor.extract("I have a 11q syndrome in my head. I'm so 11q and zws right now.")


for case in ab_cases:
    print d_extractor.extract(case)


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