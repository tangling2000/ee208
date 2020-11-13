import os.path
from whoosh.fields import Schema, STORED, ID, KEYWORD, TEXT
from whoosh.index import create_in
from jieba.analyse import ChineseAnalyzer

if __name__ =="__main__":
    schema_doc = Schema(title=TEXT(stored=True,sortable=True),
                    content=TEXT(stored=True,sortable=True,analyzer=ChineseAnalyzer()),
                    url=ID(stored=True))

    if not os.path.exists("index_doc"):
        os.mkdir("index_doc")

    create_in("index_doc", schema_doc)

    schema_img = Schema(title=TEXT(stored=True,sortable=True),
                    content=TEXT(stored=True,sortable=True,analyzer=ChineseAnalyzer()),
                    src=ID(stored=True),
                    source=ID(stored=True))

    if not os.path.exists("index_img"):
        os.mkdir("index_img")

    create_in("index_img", schema_img)