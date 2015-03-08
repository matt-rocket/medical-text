__author__ = 'matias'

import solr
import os
import json

solr_con = solr.SolrConnection('http://localhost:8983/solr')

count = 0

for subdir, dirs, files in os.walk("data/articles/findzebra"):
    for filename in files:
        with open("data/articles/findzebra/%s" % (filename, ), 'r') as infile:
            data = json.load(infile)
            title = data[u'title'].encode('utf-8')
            text = data[u'content'].encode('utf-8')
            cui = data[u'cui'].encode('utf-8')

            count += 1
            print "added", count
            solr_con.add(_commit=False, id=count,
                         title=title.decode('utf-8'),
                         text=text.decode('utf-8'),
                         resourcename=filename.decode('utf-8'),
                         description=cui.decode('utf-8'),
                         )
solr_con.commit()
