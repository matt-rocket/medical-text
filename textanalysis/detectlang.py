__author__ = 'matias'

import detectlanguage as dl
from textanalysis.texts import CaseReportLibrary
import pickle
import os

dl.configuration.api_key = ""

def detect_english(text):
    result = dl.detect(text)
    return "en" in [ e['language'] for e in result]


if __name__ == "__main__":
    id2lang = {}

    for case in CaseReportLibrary():
        abstract = case.get_abstract()
        pmcid = case.get_pmcid()
        is_english = detect_english(abstract)
        print is_english, abstract
        id2lang[pmcid] = is_english

    pickle.dump(id2lang, open("data/id2lang", 'w'))
