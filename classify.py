__author__ = 'Matias'

import json
import numpy as np
from sklearn import cross_validation, grid_search
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC, LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, BaggingClassifier, AdaBoostClassifier
from sklearn.metrics import confusion_matrix, roc_auc_score
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import label_binarize
from collections import Counter
import matplotlib.pyplot as plt


labels = json.load(open('classification/data/labels.json'))
bow = np.loadtxt(open('classification/data/bow.txt'))
tfidf = np.loadtxt(open('classification/data/tfidf.txt'))
rands = np.random.rand(len(labels['labels']), 10)

docvec_counts = [40, 45, 50]#[5, 10, 15, 20, 25, 30, 35, 40, 45, 50]

inputs = {}#{'bow': bow, 'rands': rands, 'tfidf': tfidf}

for count in docvec_counts:
    inputs["docvecs"+str(count)] = np.loadtxt(open("classification/data/docvecs%s.txt" % (count, )))


y = np.array([int(x) for x in labels['labels']])
# remove "0" labeled observations
idx = y != 0
y = y[idx]

# collapse classes
y[y == 1] = 1
y[y == 2] = 1
y[y == 6] = 1
y[y == 3] = 2
y[y == 4] = 2
y[y == 5] = 2

class_counts = Counter(y)
class_weight = {n: float(class_counts[n])/sum(class_counts.values()) for n in class_counts}

classifiers = {
    #'logit':{
    #    'classifier': LogisticRegression(),
    #    'parameters': {'C': list(np.linspace(1e-4, 1e4)), 'penalty': ['l1', 'l2'], 'dual': [False]},
    #},
    'random forest':{
        'classifier': RandomForestClassifier(),
        'parameters': {
            'n_estimators': range(10,100,5),
            'min_samples_split': range(1,10,1),
            'min_samples_leaf': range(1,5,1),
            'criterion': ['gini']
        }
    }
}


for name in classifiers:
    for key in inputs:
        scores = np.zeros(shape=(1, 10))
        for i in range(10):
            X = inputs[key]
            X = X[idx, :]
            X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.4)

            clf = grid_search.GridSearchCV(
                classifiers[name]['classifier'],
                classifiers[name]['parameters'],
                verbose=False,
                n_jobs=1
            )
            clf.fit(X_train, y_train)
            logit_score = clf.score(X_test, y_test)
            #auc_score = roc_auc_score(y_test, clf.predict(X_test))
            #print auc_score
            scores[0, i] = logit_score

        mean_score = scores.mean()
        std_score = scores.std()
        print key, name, mean_score, std_score



"""
boosted_logit = AdaBoostClassifier(MultinomialNB())
parameters = {
    'n_estimators': range(5,50,5),
    'learning_rate': list(np.linspace(0.1, 1.0, num=10))
}
clf = grid_search.GridSearchCV(boosted_logit, parameters, verbose=True)
clf.fit(X_train, y_train)
boosted_logit_score = clf.score(X_test, y_test)
print clf.best_params_
print "Boosted Logit", boosted_logit_score
"""


"""
logit_army = BaggingClassifier(LogisticRegression(), max_features=0.5, max_samples=0.5)
parameters = {
    'n_estimators': range(5,50,5),
}
clf = grid_search.GridSearchCV(logit_army, parameters, verbose=True)
clf.fit(X_train, y_train)
logit_army_score = clf.score(X_test, y_test)
print clf.best_params_
print "LogitArmy", logit_army_score
"""


"""
gbt = GradientBoostingClassifier()
parameters = {
    'n_estimators': range(5,50,5),
    'max_depth': range(1, 3),
    'learning_rate': list(np.linspace(0.1, 1.0, num=5)),
}
clf = grid_search.GridSearchCV(gbt, parameters, verbose=True)
clf.fit(X_train, y_train)
gbt_score = clf.score(X_test, y_test)
print clf.best_params_
print "GradientBoostedTree", gbt_score
"""



"""
forest = RandomForestClassifier()
parameters = {
    'n_estimators': range(10,100,5),
    'min_samples_split': range(1,10,1),
    'min_samples_leaf': range(1,5,1),
    'criterion': ['gini']
}
clf = grid_search.GridSearchCV(forest, parameters, verbose=True)
clf.fit(X_train, y_train)
forest_score = clf.score(X_test, y_test)
print clf.best_params_
print "Random Forest", forest_score
"""

"""
X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.4)

#nb = MultinomialNB(alpha=0.1)
#svm = OneVsRestClassifier(LinearSVC(penalty='l1', dual=False))
logit = OneVsRestClassifier(LogisticRegression(penalty='l2'))
#forest = RandomForestClassifier(n_estimators=10)

#nb.fit(X_train, y_train)
#svm.fit(X_train, y_train)
logit.fit(X_train, y_train)
#forest.fit(X_train, y_train)

#print forest.score(X_test, y_test)

#nb_y_hat = nb.predict(X_test)
#svm_y_hat = svm.predict(X_test)
logit_y_hat = logit.predict(X_test)

#nb_score = nb.score(X_test, y_test)
#nb_conf = confusion_matrix(y_test, nb_y_hat)
#svm_score = svm.score(X_test, y_test)
#svm_conf = confusion_matrix(y_test, svm_y_hat)
logit_score = logit.score(X_test, y_test)
logit_conf = confusion_matrix(y_test, logit_y_hat)

#print svm_conf
#print svm_score
print logit_conf
print logit_score

plt.matshow(svm_conf)
plt.show()

plt.matshow(logit_conf)
plt.show()
"""