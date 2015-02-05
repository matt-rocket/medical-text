__author__ = 'matias'

import xml.etree.ElementTree as ET



class CaseReports(object):
    def __init__(self,section='A-B'):
        with open("case_report_list_%s.txt" % section) as infile:
            self.filenames = infile.read().split("\n")[:-1]

    def __iter__(self):
        for filename in self.filenames:
            tree = ET.parse(filename)
            root = tree.getroot()
            title = root.find('./front/article-meta/title-group/article-title').text
            abstract = root.find('./front/article-meta/abstract').findall('p')
            yield title
            break


ab_cases = CaseReports('A-B')

for case in ab_cases:
    print case