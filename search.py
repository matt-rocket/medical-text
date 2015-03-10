__author__ = 'matias'

import solr


class SearchEngine(object):
    def __str__(self):
        raise NotImplementedError()

    def query(self, query_str, top_n=20):
        raise NotImplementedError()


class StandardSolrEngine(SearchEngine):
    def __init__(self, query_expansion=None):
        self.solr_con = solr.SolrConnection('http://localhost:8983/solr')
        self.name = "Standard Solr Engine"
        self.query_expansion = query_expansion

    def __str__(self):
        if self.query_expansion is not None:
            string = "%s with %s" % (self.name, self.query_expansion,)
        else:
            string = self.name
        return string

    def query(self, query_str, top_n):
        # expand query
        if self.query_expansion is not None:
            query_str = self.query_expansion.expand(query_str)
        # remove special Solr query chars
        query_str = query_str.replace(":", "")
        return self.solr_con.query(query_str, rows=top_n)
