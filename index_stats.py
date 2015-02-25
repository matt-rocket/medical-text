__author__ = 'matias'

from PubMedParser.irdatastructs import InvertedIndex
from matplotlib import pyplot as plt

entity_type = "disease"

index = InvertedIndex(entity_type)
index.load()

ranking = []
for term in index.index:
    ranking.append((term, len(set(index.index[term]))))

ranking.sort(key=lambda tup:tup[1])

count = 1
with open("%s_stopwords.txt" % (entity_type,), 'w') as outfile:
    for e in ranking:
        print count, e
        if e[1] > 80:
            outfile.write("%s\n" % (e[0],))
        count += 1

print len(ranking)

# plot IDF for all entity terms
plt.plot([1.0/tup[1] for tup in ranking[:-1]])
plt.show()