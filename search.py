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


if __name__ == "__main__":
    engine = StandardSolrEngine()
    query_input = raw_input("search for:")
    while query_input is not "":
        hits = engine.query(query_input, 50).results
        relevant = []
        partly_relevant = []
        print "--------- RESULTS ---------"
        for hit in hits:
            relevance_input = ""
            while not relevance_input.isdigit():
                relevance_input = raw_input(
                    str(hit[u'id']) + " " + str(hit[u'title']) +
                    " (0=not relevant, 1=partly relevant, 2=relevant) Rating:")
            if relevance_input == "1":
                partly_relevant.append(hit[u'id'])
            elif relevance_input == "2":
                relevant.append(hit[u'id'])
        print "---------------------------"
        print "Relevant:  ", ",".join(relevant)
        print "Partly Relevant:  ", ",".join(partly_relevant)
        print ""
        query_input = raw_input("search for:")