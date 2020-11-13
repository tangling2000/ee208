# SJTU EE208

INDEX_DIR = "IndexFiles.index"

from hashlib import new
import sys, os, lucene
import jieba

from java.io import File
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.analysis.core import SimpleAnalyzer,WhitespaceAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.util import Version

"""
This script is loosely based on the Lucene (java implementation) demo class 
org.apache.lucene.demo.SearchFiles.  It will prompt for a search query, then it
will search the Lucene index in the current directory called 'index' for the
search query entered against the 'contents' field.  It will then display the
'path' and 'name' fields for each of the hits it finds in the index.  Note that
search.close() is currently commented out because it causes a stack overflow in
some cases.
"""
def cut_command(command):
    #针对传入的关键词进行分词并转化为布尔查询语句
    keyList = jieba.lcut(command)
    newCommand = " AND ".join(keyList)
    return newCommand

def run(searcher, analyzer):
    # while True:
    print()
    print ("Hit enter with no input to quit.")

    command = "西方新冠肺炎"
    # command = input("Query:")
    if command == '':
        return
    command = cut_command(command)

    print ("Searching for:", command,'\n')
    query = QueryParser("contents", analyzer).parse(command)
    scoreDocs = searcher.search(query, 50).scoreDocs
    print ("%s total matching documents.\n" % len(scoreDocs))

    for i, scoreDoc in enumerate(scoreDocs):
        doc = searcher.doc(scoreDoc.doc)
        path = doc.get('path')
        title = doc.get('title')
        url = doc.get('url')
        print("path: \t{}\ntitle: \t{}\nurl:\t{}\nscore: \t{}\n".format(path,title,url,scoreDoc.score))
            # print 'explain:', searcher.explain(query, scoreDoc.doc)


if __name__ == '__main__':
    STORE_DIR = "index_15000"
    lucene.initVM()#vmargs=['-Djava.awt.headless=true'])
    print ('lucene', lucene.VERSION)
    #base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    directory = SimpleFSDirectory(File(STORE_DIR).toPath())
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = WhitespaceAnalyzer()#Version.LUCENE_CURRENT)
    run(searcher, analyzer)
    del searcher
