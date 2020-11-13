# SJTU EE208

INDEX_DIR = "IndexFiles.index"

import sys, os, lucene, threading, time, re
from datetime import datetime

from java.io import File
from java.nio.file import Path
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType, StringField, TextField
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version
from org.apache.lucene.analysis.core import WhitespaceAnalyzer
import jieba

"""
This class is loosely based on the Lucene (java implementation) demo class 
org.apache.lucene.demo.IndexFiles.  It will take a directory as an argument
and will index all of the files in that directory and downward recursively.
It will index on the file path, the file name and the file contents.  The
resulting Lucene index will be placed in the current directory and called
'index'.
"""

class Ticker(object):

    def __init__(self):
        self.tick = True

    def run(self):
        while self.tick:
            sys.stdout.write('.')
            sys.stdout.flush()
            time.sleep(1.0)

class IndexFiles(object):
    """Usage: python IndexFiles <doc_directory>"""

    def __init__(self, root, storeDir, analyzer):

        if not os.path.exists(storeDir):
            os.mkdir(storeDir)

        store = SimpleFSDirectory(File(storeDir).toPath())
        analyzer = LimitTokenCountAnalyzer(analyzer, 1048576)
        config = IndexWriterConfig(analyzer)
        config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
        writer = IndexWriter(store, config)

        self.indexDocs(root, writer)
        ticker = Ticker()
        print('commit index')
        threading.Thread(target=ticker.run).start()
        writer.commit()
        writer.close()
        ticker.tick = False
        print('done')

    def getTxtAttribute(self, contents, attr):
        m = re.search(attr + ': (.*?)\n',contents)
        if m:
            return m.group(1)
        else:
            return ''
    def indexDocs(self, root, writer):   
        for root,dirnames,filenames in os.walk(root):
            for dirname in dirnames: #遍历文件夹
                path1 = os.path.join(root,dirname)
                for trivial1 , trivial2 , filenames in os.walk(path1): #遍历文件夹下的文件
                    for filename in filenames:
                        #print(root,dirnames,filename)
                        print("adding", filename)
                        # try:
                        path = os.path.join(path1, filename)
                        file = open(path, encoding='utf8')
                        page = file.readline()
                        title = file.readline()
                        contents = file.read()
                        file.close()

                        # jieba 分词
                        seg_contents = jieba.lcut_for_search(contents)
                        contents = ' '.join(seg_contents)
                        url = page
                        seg_url = jieba.lcut_for_search(page)
                        page = ' '.join(list(set(seg_url)-set(['.','http','https','/',':','?','=','html','shtml','www'])))

                        doc = Document()
                        doc.add(StringField("name", filename, Field.Store.YES))
                        doc.add(StringField("path", path, Field.Store.YES))
                        if len(contents) > 0:
                            doc.add(TextField('title', title, Field.Store.YES))
                            doc.add(TextField('site', page, Field.Store.YES))
                            doc.add(TextField('url',url,Field.Store.YES))
                            doc.add(TextField('contents', contents, Field.Store.YES))
                        else:
                            print("warning: no content in %s" % filename)
                        writer.addDocument(doc)

if __name__ == '__main__':
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print('lucene', lucene.VERSION)
    start = datetime.now()
    try:
        analyzer = WhitespaceAnalyzer()
        IndexFiles('page', "index", analyzer)
        end = datetime.now()
        print(end - start)
    except Exception as e:
        print("Failed: ", e)
        raise e
