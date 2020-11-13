import os.path
from whoosh.fields import Schema, STORED, ID, KEYWORD, TEXT
from whoosh.index import create_in
from jieba.analyse import ChineseAnalyzer

if __name__ =="__main__":
    schema = Schema(title=TEXT(stored=True,sortable=True),
                    content=TEXT(stored=True,sortable=True,analyzer=ChineseAnalyzer()),
                    url=ID(stored=True),
                    source=ID(stored=True))

    if not os.path.exists("index"):
        os.mkdir("index")

    create_in("index", schema)