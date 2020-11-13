# SJTU EE208

INDEX_DIR = "IndexFiles.index"

import sys, os, lucene

from java.io import File
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.util import Version
from org.apache.lucene.analysis.core import WhitespaceAnalyzer
import jieba


"""
This script is loosely based on the Lucene (java implementation) demo class 
org.apache.lucene.demo.SearchFiles.  It will prompt for a search query, then it
will search the Lucene index in the current directory called 'index' for the
search query entered against the 'contents' field.  It will then display the
'path' and 'name' fields for each of the hits it finds in the index.  Note that
search.close() is currently commented out because it causes a stack overflow in
some cases.
"""
def divide_by_jieba(content):
    content = content.split()
    command = [] #返回的命令
    for i in range(len(content)):
        s = jieba.lcut_for_search(content[i])
        if s[0]==content[i]:
            command.append(s[0])
            continue
        command.append(''.join(['(',' AND '.join(s),')']))

    return ' '.join(command)

def run(searcher, analyzer):
    # while True:
    print()
    print ("Hit enter with no input to quit.")
    # command = raw_input("Query:")
    # command = unicode(command, 'GBK')
    command = '东风' #写入搜索命令，括号与文字中间最好用空格隔开
    
    
    if command == '':
        return
    

    print()
    print ("Searching for:", command)
    command = divide_by_jieba(command) #对搜索命令进行分词
    #print(command)
    query = QueryParser("contents", analyzer).parse(command)
    scoreDocs = searcher.search(query, 20).scoreDocs
    print ("%s total matching documents." % len(scoreDocs))

    for i, scoreDoc in enumerate(scoreDocs):
        doc = searcher.doc(scoreDoc.doc)
        print ('img_url:',doc.get('img_url'),'title:', doc.get("title"),'url:',doc.get('url'))
            # print 'explain:', searcher.explain(query, scoreDoc.doc)


if __name__ == '__main__':
    STORE_DIR = "photo_index"
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print ('lucene', lucene.VERSION)
    #base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    directory = SimpleFSDirectory(File(STORE_DIR).toPath())
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = WhitespaceAnalyzer()#Version.LUCENE_CURRENT)
    run(searcher, analyzer)
    del searcher
