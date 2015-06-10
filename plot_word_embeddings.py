import logging
from irmodels.W2Vmodel import W2Vmodel
from textanalysis.texts import PhraseSentenceStream, RawSentenceStream
from textanalysis.phrasedetection import PmiPhraseDetector
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

# setup logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
# phrase detector
phrase_detector = PmiPhraseDetector(RawSentenceStream())
# build model
m = W2Vmodel(PhraseSentenceStream(phrase_detector))


labels = {}

with open("testdiseases.txt", 'r') as infile:
    for line in infile.read().split("\n")[:-1]:
        parts = line.split(",")
        labels[parts[1]] = int(parts[0])

keywords = labels.keys()

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
    'blastoma',
    'carcinoma',
    'neoplasm',
    'lymphoma',
    'melanoma',
    'tumor',
    'aldosterone-producing_adenoma',
    'spitzoid_melanoma',
    'villous_adenoma',
    'adenoma_malignum',
    'uveal_melanoma',
    'somatotroph_adenoma',
    'pleomorphic_adenoma',
    'amelanotic_melanoma',
    'aneurysm',
    'acoma_aneurysm',
    'submitral_aneurysm',
    'osteoporosis',
    'hypoglycemia',
    'hypothyroidism',
    'diabetes_mellitus',
    'virus',
    'hepatitis',
    'borrelia',
    'enterovirus',
    'influenza',
    'cryptococcosis',
    'measles',
    'dengue',
    'gonorrhea',
    'leprosy',
    'aspergillosis',
    'hpv',
    'hiv',
    'aids',
    'malaria',
    'astrovirus',
    'tumor',
    'arthritis',
    'rheumatoid_arthritis',
    'lupus',
    'anthrax',
    'myocardial_infarction',
    'dilatative_cardiomyopathy',
    'non-ischemic_cardiomyopathy',
    'noncompaction_cardiomyopathy',
    'supraventricular_arrhythmia',
    'tako-tsubo_cardiomyopathy',
    'hypertrophic_cardiomyopathy',
    'anxiety',
    'neurosis',
    'mania',
    'bipolar',
    'amnesia',
    'neuropathy',
    'psychosis',
    'narcolepsy',
    'adhd',
    'coma',
    'capgras',
    'dyslexia',
    'dyscalculia',
    'asperger',
    'apraxia',
    'dementia',
    'headache',
    'panic',
    'ocd',
    'autism',
    'ataxia',
    'chorea',
    'cytomegalovirus_retinitis',
    'glaucoma',
    'serpiginous_choroiditis',
    'microbial_keratitis',
    'maculopathy',
    'choroiditis',
    'multifocal_choroiditis',
    'retinopathy',
    'amoebial_colitis',
    'mrsa_enterocolitis',
    'sle',
    'lupus_erythematosis',
    'lupus_erythematosus',
    'psoriasis',
    'urticaria',
    'scleroderma',
    'eczema',
    'lupus_nephritis',
    'lichen_sclerosus',
    'lichen_planus',
    'morphea',
    'dermatitis',
]

merge_to_autoimmune = [3, 4, 5, 7]
for word in labels:
    if labels[word] in merge_to_autoimmune:
        labels[word] = 14
    if labels[word] == 2:
        labels[word] = 1

for word in m.inner_model.vocab:
    parts = ['carcinoma', 'melanoma', 'adenoma', 'tumor', 'cancer']
    if "_" in word and any([w in parts for w in word.split("_")]):
        print word


all_class = [w for w in labels if labels[w] == 13]
#print all_class
#marker_words += all_class

pcs = (0, 1)


classes = ['Cardiovascular','Cancer','Gastrointestinal','Infections','Endocrine','Eye','Respiratory','Neurological','Autoimmune']
class_colours = ['b','c','r','yellow','m','g','pink','k','purple']
label2index = {label:idx for idx, label in enumerate(set(labels.values()))}
color_map = [class_colours[label2index[c]] for c in labels.values()]

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
