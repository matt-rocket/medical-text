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


words = {'depression': 1,
         'escitalopram': 1,
         'paroxetine': 1,
         'lymphoma': 2,
         'leukemia': 3,
         'imatinib': 3,
         'cancer': 2,
         'tumor': 2,
         'rituxan': 2,
         'rituximab': 2}

# disease data
keywords = words.keys()
X = np.zeros(shape=(len(keywords), m.inner_model.layer1_size))
for idx, word in enumerate(keywords):
    if word in m.inner_model.vocab:
        X[idx, :] = m.inner_model[word]
        print word, X[idx, :]

print X

# fit PCA on diseases
pca = PCA(n_components=2)
pca.fit(X)


# transform drug data
PC = pca.transform(X)

marker_words = ['depression', 'escitalopram', 'tumor', 'imatinib']

# plot PC1 and PC2
pcs = (0, 1)
classes = ['Lymphoma', 'Depression', 'Leukemia']
class_colours = ['r','b', 'g']
label2index = {label:idx for idx, label in enumerate(set(words.values()))}
color_map = [class_colours[label2index[c]] for c in words.values()]

plt.figure(figsize=(20, 20))
plt.scatter(PC[:, pcs[0]], PC[:, pcs[1]], c=color_map, s=1, alpha=0.01, edgecolors='none')
plt.xlim((-2.4, 1.7))
plt.ylim((-1.4, 1.6))
plt.xlabel("PC-1")
plt.ylabel("PC-2")
plt.title("Disease-Drug analogy")
for label, x, y in zip(keywords, PC[:, pcs[0]], PC[:, pcs[1]]):
    if label in marker_words:
        plt.annotate(label, xy=(x, y), fontsize=20)

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