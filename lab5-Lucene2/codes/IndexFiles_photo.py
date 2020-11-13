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
        contents = contents.replace(":\n",':')
        contents = contents.replace(":img",':\n')
        contents = contents + '\n'
        m = re.findall(attr + ':(.*?)\n',contents)
        if m:
            return m
        else:
            return ''
    def indexDocs(self, root, writer):   
        for root, dirnames, filenames in os.walk(root):
            for filename in filenames:
                print("adding", filename)
                path = os.path.join(root, filename)
                file = open(path, encoding='utf8')
                url = file.readline()
                title = file.readline()
                contents = file.read()
                file.close()
                img_url = self.getTxtAttribute(contents, 'img_url')
                img_info = self.getTxtAttribute(contents, 'img_info')
                for i in range(len(img_url)):  
                    if len(img_info[i]) > 0:
                        title = title
                        doc = Document()

                        doc.add(StringField('title', title, Field.Store.YES))
                        doc.add(StringField('url', url, Field.Store.YES))
                        doc.add(StringField('img_url', img_url[i], Field.Store.YES))
                        seg_contents = jieba.lcut_for_search(img_info[i])
                        contents = ' '.join(seg_contents)
                        doc.add(TextField('contents', contents, Field.Store.YES))
                        writer.addDocument(doc)
                    else:
                        continue
if __name__ == '__main__':
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print('lucene', lucene.VERSION)
    start = datetime.now()
    try:
        analyzer = WhitespaceAnalyzer()
        IndexFiles('guancha_photo', "photo_index", analyzer)
        end = datetime.now()
        print(end - start)
    except Exception as e:
        print("Failed: ", e)
        raise e
