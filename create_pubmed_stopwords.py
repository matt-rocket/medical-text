__author__ = 'matias'

from gensim import corpora, models

print "loading dictionary.."
dictionary = corpora.Dictionary.load('IRmodels/data/sample.dict')

print "loading corpus.."
corpus = corpora.MmCorpus('IRmodels/data/sample.mm')

print "building TF-IDF model.."
tfidf = models.TfidfModel(corpus, id2word=dictionary)

freqs = []
for key in tfidf.idfs:
    freqs.append((dictionary[key], tfidf.idfs[key]))

freqs.sort(key= lambda tup: tup[1],reverse=True)
# high frequency words
hifreqs = [tup for tup in freqs if tup[1] < 2]
lowfreqs = [tup for tup in freqs if tup[1] > 10]


with open('candidate_stopwords.txt','w') as outfile:
    for (word, idf) in hifreqs:
        outfile.write("%s\n" % word.encode('utf-8'))

    for (word, idf) in lowfreqs:
        is_stopword = False
        # remove all words with digit in
        is_stopword = any(c.isdigit() for c in word)

        # remove non-ascii words
        try:
            word.encode('ascii')
        except:
            is_stopword=True

        # quick fix for word collisions
        if word.startswith(('introduction', 'discussion')):
            is_stopword = True

        if is_stopword:
            outfile.write("%s\n" % word.encode('utf-8'))

