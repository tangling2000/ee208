from whoosh.highlight import top_fragments
from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from whoosh import scoring
from whoosh import sorting
from whoosh.query import *
from whoosh import highlight

def search(keyword):

    results = []
    dirname = "index_img"
    ix = open_dir(dirname=dirname)
    querystring = u"{}".format(keyword)
    searcher = ix.searcher()

    parser = QueryParser("content", ix.schema)
    myquery = parser.parse(querystring)
    with ix.searcher() as searcher:
        hits = searcher.search(myquery,groupedby="src")
        for hit in hits:
            result = {
                'title':hit['title'],
                'src':hit['src'],
                'source':hit['source']
            }
            results.append(result)
    return results

if __name__ == "__main__":
    results = search('北京')
    print(results)
