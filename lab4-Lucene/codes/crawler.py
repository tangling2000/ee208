# SJTU EE208

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
from BloomFilter import BloomFilter

from bs4 import BeautifulSoup

def time_execution(code):
    start = time.perf_counter()
    result = eval(code)
    run_time = time.perf_counter() - start
    return run_time, result

def valid_filename(s):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
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
    soup = BeautifulSoup(content,from_encoding=None,features='html.parser')
    try:
        for tag in soup.findAll('a',{'href':re.compile('^http|^/')}):
            link = tag['href']
            if (link[-4:] != 'html'):
                continue
            if link[0] == '/':
                link = urllib.parse.urljoin(page,link)
            links.append(link)
    except:
        links = []
    return links

def add_page_to_folder(page, content):
    index_filename = 'index.txt'
    folder = 'html'
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
            outlinks = get_all_links(content,page)

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

    seed = 'https://m.guancha.cn/'
    count = 0
    NUM = 64
    MAXPAGE = 20

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