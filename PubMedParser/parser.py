__author__ = 'matias'

import os
import xml.etree.ElementTree as ET


def get_type(filepath):
    # the strange prefix is a workaround to handle filepaths longer than 255 chars
    tree = ET.parse(r"\\?\\" + filepath)
    root = tree.getroot()
    return root.attrib['article-type']


root_folder = r"C:\Users\matias\Desktop\thesis\data\pubmed\articles.O-Z"

types = {}
hits = 0
total = 0

case_reports = []

for subdir, dirs, files in os.walk(root_folder):
    for filename in files:
        total += 1
        filepath = os.path.join(subdir, filename)
        article_type = get_type(filepath)
        if article_type == "case-report":
            print filepath
            case_reports.append(filepath)
            hits += 1
        else:
            print hits,"/",total

with open('case_report_list_O-Z.txt','w') as outfile:
    for filename in case_reports:
        outfile.write("%s\n" % filename)

