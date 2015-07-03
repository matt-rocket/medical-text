__author__ = 'Matias'

from search import ElasticSearchEngine


def judge(eval_file='findzebra.tsv'):

    search = ElasticSearchEngine()

    with open('evaluation/data/%s' % (eval_file,), 'r') as infile:

        records = infile.read().split("\n")

        finished = [1]

        for record in records:
            parts = record.split("\t")
            query_id = int(parts[0])
            if query_id in finished:
                continue
            query = parts[1]
            target = parts[2]
            print query
            ids = []
            hits = search.query(query, top_n=100)
            count = 0
            for hit in hits:
                count += 1
                title = hit['description']
                pmcid = hit['id']
                print "TARGET:", target
                print ""
                print count, "TITLE:", pmcid,  title
                if raw_input("Y/N?").lower() == "y":
                    ids.append(pmcid)
            print "ID:", query_id, "---",  ",".join(ids)



if __name__ == "__main__":
    judge()