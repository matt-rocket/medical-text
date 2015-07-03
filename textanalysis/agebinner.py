__author__ = 'Matias'

import re

def is_age(word):
    return word[-5:] == "-year"

def age_bin(word):
    age = int(re.match("(\d+)-year", word).group(1))
    age = (age / 10) * 10
    return str(age)+"-year"
