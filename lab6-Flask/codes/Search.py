from whoosh.highlight import top_fragments
from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from whoosh import scoring
from whoosh.query import *
from whoosh import highlight

class BracketFormatter(highlight.Formatter):
    def format_token(self, text, token, replace=False):
        tokentext = highlight.get_text(text, token, replace)
        return "<mark>{}</mark>".format(tokentext)

def search(keyword):

    results = []
    dirname = "index"
    ix = open_dir(dirname=dirname)
    querystring = u"{}".format(keyword)
    searcher = ix.searcher()
    hi = highlight.Highlighter()
    brf = BracketFormatter()

    parser = QueryParser("content", ix.schema)
    myquery = parser.parse(querystring)
    with ix.searcher() as searcher:
        hits = searcher.search(myquery,limit=None)
        hits.formatter = brf
        for hit in hits:
            result = {
                'title':hit['title'],
                'abstract':hit.highlights('content',top=1),
                'url':hit['url']
            }
            results.append(result)
    return results

if __name__ == "__main__":
    results = search('特朗普')
    print(results[0]['abstract'])
