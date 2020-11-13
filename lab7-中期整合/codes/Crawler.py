import threading
import queue
import time
import os
import re
import string
import time
import urllib.error
import urllib.parse
import urllib.request
from bs4 import BeautifulSoup
import random
import math

class Bitarray:
    def __init__(self, size):
        """ Create a bit array of a specific size """
        self.size = size
        self.bitarray = bytearray(math.ceil(size / 8.))
        #返回一个二进制数组，一个bit可以存一位信息，这样的确节省空间，向上取整，所以要用ceil，默认整除是向下取整

    def set(self, n):
        """ Sets the nth element of the bitarray """

        index = int(n / 8)
        #找到块位置
        position = n % 8
        #找到在块中的位置
        self.bitarray[index] = self.bitarray[index] | 1 << (7 - position)
        #对于1进行移位
        #进行或运算将其进行储存

    def get(self, n):
        """ Gets the nth element of the bitarray """

        index = int(n / 8)
        position = n % 8
        return (self.bitarray[index] & (1 << (7 - position))) > 0
        #进行且运算，如果重合，返回的是true，如果不重合，返回的是false

class BloomFilter:
    def __init__(self,n):
        #对于基本参数进行设置
        self.k = 10
        self.m = n*20+1
        #这一步很关键，处以一个素数会让冲突减小一万倍
        self.bitarray = Bitarray(self.m)

    def hash_str(self,keyword,i):
        seed = eval("1313"+i*"13") # 31 131 1313 13131 131313 etc..
        hash = 0
        for i in range(len(keyword)):
            hash = (hash * seed) + ord(keyword[i])
        index = hash%self.m
        return index

    def add_keyword(self,keyword):
        for i in range(self.k):
            index = self.hash_str(keyword=keyword,i=i)
            self.bitarray.set(index)
        
    def check_keyword(self,keyword):
        for i in range(self.k):
            index = self.hash_str(keyword=keyword,i=i)
            if not self.bitarray.get(index):
                return False
        return True

def valid_filename(s):
    valid_chars = "_.%s%s" % (string.ascii_letters, string.digits)
    s = ''.join(c for c in s if c in valid_chars)
    return s

def get_page(page):
    encoding = 'utf-8'
    try:
        req = urllib.request.Request(page)
        req.add_header('User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:80.0) Gecko/20100101 Firefox/80.0')
        content = urllib.request.urlopen(req,timeout=10).read().decode(encoding)
    except:
        content = ""
    return content

def get_all_links(content, page):
    links = []
    soup = BeautifulSoup(content,features='html.parser')
    try:
        for tag in soup.findAll('a',{'href':re.compile('^/item')}):
            link = tag['href']
            link = urllib.parse.urljoin(page,link)
            links.append(link)
    except:
        links = []
    return links

def add_page_to_folder(page, content):
    index_filename = 'index.txt'
    folder = 'source'
    filename = valid_filename(page)

    with open(index_filename,'a') as index:
        index.write(page + '\t' + filename + '\n')

    if not os.path.exists(folder):
        os.mkdir(folder)
    with open(os.path.join(folder,filename),'w') as file:
        file.write(content)

def working():
    global count
    global bloomFilter
    while True:

        page = taskQueue.get()

        if not bloomFilter.check_keyword(page):

            content = get_page(page)
            add_page_to_folder(page,content)
            outlinks = get_all_links(content,'https://baike.baidu.com/')

            varLock.acquire()
            bloomFilter.add_keyword(page)
            if not count % 100:
                print(count)
            count += 1
            varLock.release()

            for link in outlinks:
                taskQueue.put(link)

        taskQueue.task_done()

        if count >= MAXPAGE:
            while not taskQueue.empty():
                taskQueue.get()
                taskQueue.task_done()

if __name__ == '__main__':

    seed = 'https://baike.baidu.com/item/%E4%B8%AD%E5%9B%BD/1122445'
    count = 0
    NUM = 16
    MAXPAGE = 400

    bloomFilter = BloomFilter(MAXPAGE)
    varLock = threading.Lock()
    taskQueue = queue.Queue()

    start = time.perf_counter()

    taskQueue.put(seed)
    for num in range(NUM):
        line = threading.Thread(target=working)
        line.setDaemon(True)
        line.start()
    taskQueue.join()

    end = time.perf_counter()
    print("{} takes {}s by final_crwaler on NUM {}".format(MAXPAGE,end - start,NUM))