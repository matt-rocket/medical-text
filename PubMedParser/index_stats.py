__author__ = 'matias'

from irdatastructs import InvertedIndex
from matplotlib import pyplot as plt
from math import log

index = InvertedIndex("disease")
index.load()

ranking = []
for term in index.index:
    ranking.append((term, len(set(index.index[term]))))

ranking.sort(key=lambda tup:tup[1])

for e in ranking:
    print e

print len(ranking)

plt.plot([log(tup[1]) for tup in ranking[:-1]])
plt.show()