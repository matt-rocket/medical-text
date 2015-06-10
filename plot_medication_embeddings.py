import logging
from irmodels.W2Vmodel import W2Vmodel
from textanalysis.texts import PhraseSentenceStream, RawSentenceStream
from textanalysis.phrasedetection import PmiPhraseDetector
import numpy as np
from random import sample
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

# setup logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
# phrase detector
phrase_detector = PmiPhraseDetector(RawSentenceStream())
# build model
m = W2Vmodel(PhraseSentenceStream(phrase_detector))

diseases = {}
drugs = {}

with open("testdiseases.txt", 'r') as infile:
    for line in infile.read().split("\n")[:-1]:
        parts = line.split(",")
        diseases[parts[1]] = int(parts[0])

with open("testmedication.txt", 'r') as infile:
    for line in infile.read().split("\n")[:-1]:
        parts = line.split(",")
        drugs[parts[1]] = int(parts[0])

# disease data
keywords = diseases.keys()
X = np.zeros(shape=(len(keywords), m.inner_model.layer1_size))
for idx, word in enumerate(keywords):
    if word in m.inner_model.vocab:
        X[idx, :] = m.inner_model[word]

# fit PCA on diseases
pca = PCA(n_components=4)
pca.fit(X)

# disease data
keywords = drugs.keys()
D = np.zeros(shape=(len(keywords), m.inner_model.layer1_size))
for idx, word in enumerate(keywords):
    if word in m.inner_model.vocab:
        D[idx, :] = m.inner_model[word]

# transform drug data
PC = pca.transform(D)

weights = {6:50, 9:100, 1:50, 13:100}
# plot PC1 and PC2
marker_words =  ['xanax', 'prosac', 'methotrexate', 'amoxillin', 'ritalin', 'prednisone', 'cyclophosphamide', 'lithium', 'cloxacillin']
keywords = []


pcs = (0, 1)
classes = ['Neurological', 'Infections', 'Cancer', 'Cardiovascular']
class_colours = ['yellow','k','c','b']
label2index = {label:idx for idx, label in enumerate(set(drugs.values()))}
color_map = [class_colours[label2index[c]] for c in drugs.values()]

plt.figure(figsize=(20, 20))
plt.scatter(PC[:, pcs[0]], PC[:, pcs[1]], c=color_map, s=30, alpha=0.5, edgecolors='none')
plt.xlim((-2.4, 1.7))
plt.ylim((-1.4, 1.6))
for label, x, y in zip(keywords, PC[:, pcs[0]], PC[:, pcs[1]]):
    if label in marker_words:
        plt.annotate(label, xy=(x, y), fontsize=9)

import matplotlib.patches as mpatches
recs = []
for i in range(0,len(class_colours)):
    recs.append(mpatches.Rectangle((0, 0), 1, 1, fc=class_colours[i]))
plt.legend(recs, classes, loc=3)

plt.show()


"""

keywords = diseases.keys()

X = np.zeros(shape=(len(keywords), m.inner_model.layer1_size))

for idx, word in enumerate(keywords):
    if word in m.inner_model.vocab:
        X[idx, :] = m.inner_model[word]
    else:
        print word, "not in vocab"



pca = PCA(n_components=4)
pca.fit(X)

PC = pca.transform(X)

marker_words = [
]


pcs = (0, 1)


classes = ['Cancer','Infections','Neurological']
class_colours = ['r','yellow','k']
label2index = {label:idx for idx, label in enumerate(set(diseases.values()))}
color_map = [class_colours[label2index[c]] for c in diseases.values()]

plt.figure(figsize=(20, 20))
plt.scatter(PC[:, pcs[0]], PC[:, pcs[1]], c=color_map, s=70, alpha=0.7, edgecolors='none')
for label, x, y in zip(keywords, PC[:, pcs[0]], PC[:, pcs[1]]):
    if label in marker_words:
        plt.annotate(label, xy=(x, y), fontsize=9)


import matplotlib.patches as mpatches
recs = []
for i in range(0,len(class_colours)):
    recs.append(mpatches.Rectangle((0,0),0.5,0.5,fc=class_colours[i]))
plt.legend(recs,classes,loc=3)

plt.show()
"""