__author__ = 'matias'

from irdatastructs import InvertedIndex
from matplotlib import pyplot as plt

index = InvertedIndex("disease")
index.load()

ranking = []
for term in index.index:
    ranking.append((term, len(set(index.index[term]))))

ranking.sort(key=lambda tup:tup[1])

count = 1
for e in ranking:
    print count, e
    count += 1

print len(ranking)

# plot IDF for all disease terms
plt.plot([1.0/tup[1] for tup in ranking[:-1]])
plt.show()