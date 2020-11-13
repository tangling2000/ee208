from os import write
from whoosh.index import open_dir
from bs4 import BeautifulSoup
import os
import re

from whoosh.util import text

def read_relation(relation_file):
    relation = {}
    with open(relation_file,'r') as f:
        lines = f.readlines()
        for line in lines:
            m = line.split()
            relation[m[1]] = m[0]
    return relation

if __name__ == "__main__":
    dirname = "index_img"
    ix = open_dir(dirname=dirname)
    writer = ix.writer()

    count = 0
    root = "source"
    relation_file = "index.txt"

    relation = read_relation(relation_file=relation_file)

    for root, dirnames, filenames in os.walk(root):
        for filename in filenames:
            try:
                path = os.path.join(root, filename)
                with open(path,'r') as file:
                    contents = file.read()
                soup = BeautifulSoup(contents,features="html.parser")

                url = relation[filename]
                if len(contents) > 0:
                    title = soup.find('title').text  #开始处理开头
                else:
                    print("no content")
                    continue
                
                for tag in soup.findAll('img',{'src':re.compile('^https')}):
                    src = tag['src']
                    content = tag.text
                    # " ".join([tag.parent.next_sibling.next_sibling.text,tag.text])
                    writer.add_document(
                        title=u"{}".format(title),
                        content=u"{}".format(content),
                        src=u"{}".format(src),
                        source=u"{}".format(url)
                    )

                    count+=1
                    if (count%100==0):
                        print(count)
                
            except Exception as error:
                print("Failed in indexDocs:", error)



    writer.commit()