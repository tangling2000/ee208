# SJTU EE208

INDEX_DIR = "IndexFiles.index"

import sys, os, lucene

from java.io import File
from java.nio.file import Path
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.util import Version
from org.apache.lucene.search import BooleanQuery
from org.apache.lucene.search import BooleanClause
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

def divide_site(page):
    seg_url = jieba.lcut_for_search(page)
    return ' AND '.join(list(set(seg_url)-set(['.','http','https','/',':','?','='])))

def parseCommand(command):
    #解析命令行，形成一个字典
    allowed_opt = ['site']
    command_dict = {}
    opt = 'contents'
    #以空格分割
    for i in command.split(' '):
        #对于一个小结构，以：为分割
        if ':' in i:
            opt, value = i.split(':')[:2]
            opt = opt.lower()
            if opt in allowed_opt and value != '':
                command_dict[opt] = command_dict.get(opt, '') + ' ' + divide_site(value)
        else:
            command_dict[opt] = command_dict.get(opt, '') + ' ' + divide_by_jieba(i)
    return command_dict

def run(searcher, analyzer):
    #while True:
        print()
        print ("Hit enter with no input to quit.")
        #command = input("Query:")
        # command = unicode(command, 'GBK')
        command = '环保节能社会 site:guancha.cn'
        if command == '':
            return

        print()
        print ("Searching for:", command)
        
        command_dict = parseCommand(command)
        print(command_dict)
        querys = BooleanQuery.Builder()
        for k,v in command_dict.items():
            query = QueryParser(k, analyzer).parse(v)
            # print(query)
            querys.add(query, BooleanClause.Occur.MUST)
        scoreDocs = searcher.search(querys.build(), 50).scoreDocs
        print("%s total matching documents." % len(scoreDocs))

        for scoreDoc in scoreDocs:
            doc = searcher.doc(scoreDoc.doc)
##            explanation = searcher.explain(query, scoreDoc.doc)
            print("------------------------")
            print('path:', doc.get("path"))
            print('name:', doc.get("name"))
            print('title:', doc.get('title'))
            print('url:', doc.get('url'))
##            print explanation


if __name__ == '__main__':
    STORE_DIR = "index"
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print('lucene', lucene.VERSION)
    #base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    directory = SimpleFSDirectory(File(STORE_DIR).toPath())
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = WhitespaceAnalyzer()
    run(searcher, analyzer)
    del searcher
