# SJTU EE208

INDEX_DIR = "IndexFiles.index"

from os import read, setregid
import sys, os, lucene, threading, time
from datetime import datetime
from bs4 import BeautifulSoup
import jieba

# from java.io import File
from java.nio.file import Paths
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.analysis.core import SimpleAnalyzer,WhitespaceAnalyzer
from org.apache.lucene.document import Document, Field, FieldType, StringField
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig, IndexOptions
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version

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

    def __init__(self, root, storeDir, relationFile):

        if not os.path.exists(storeDir):
            os.mkdir(storeDir)

        # store = SimpleFSDirectory(File(storeDir).toPath())
        store = SimpleFSDirectory(Paths.get(storeDir))
        # analyzer = StandardAnalyzer()
        analyzer = WhitespaceAnalyzer()
        analyzer = LimitTokenCountAnalyzer(analyzer, 1048576)
        config = IndexWriterConfig(analyzer)
        config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
        writer = IndexWriter(store, config)

        self.read_relation(relationFile)
        self.indexDocs(root, writer)
        ticker = Ticker()
        print('commit index')
        threading.Thread(target=ticker.run).start()
        writer.commit()
        writer.close()
        ticker.tick = False
        print('done')

    def read_relation(self,relaionFile):
        self.relation = {}
        with open(relaionFile,'r') as f:
            lines = f.readlines()
            for line in lines:
                m = line.split()
                self.relation[m[1]] = m[0]
        

    def indexDocs(self, root, writer):

        t1 = FieldType()
        t1.setStored(True)
        t1.setTokenized(False)
        t1.setIndexOptions(IndexOptions.NONE)  # Not Indexed
        
        t2 = FieldType()
        t2.setStored(False)
        t2.setTokenized(True)
        t2.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)  # Indexes documents, frequencies and positions.
        
        count = 0
        for root, dirnames, filenames in os.walk(root):
            for filename in filenames:
                if not filename.endswith('.shtml'):
                    continue

                try:
                    path = os.path.join(root, filename)
                    with open(path,'r') as file:
                        contents = file.read()
                    soup = BeautifulSoup(contents,features="html.parser")
                    doc = Document()

                    doc.add(Field("name", filename, t1))
                    doc.add(Field("path", path, t1))

                    url = self.relation[filename]
                    doc.add(Field("url",url,t1))


                    if len(contents) > 0:

                        title = soup.find('title').text  #开始处理开头

                        content = "".join(soup.findAll(text=True))
                        content = jieba.lcut(content)
                        content = ' '.join(content)

                        doc.add(Field("title",title,t1))
                        doc.add(Field("contents", content, t2))       

                    else:
                        doc.add(Field("title","",t1))
                        doc.add(Field("contents", "", t2))

                        print("warning: no content in %s" % filename)
                    writer.addDocument(doc)
                except Exception as e:
                    print("Failed in indexDocs:", e)

                count+=1
                if (count%100==0):
                    writer.commit()
                    print(count)

if __name__ == '__main__':
    lucene.initVM()#vmargs=['-Djava.awt.headless=true'])
    
    print('lucene', lucene.VERSION)
    # import ipdb; ipdb.set_trace()
    start = datetime.now()
    try:
        IndexFiles('html', "index",'index.txt')
        end = datetime.now()
        print(end - start)
    except Exception as e:
        print("Failed: ", e)
        raise e
