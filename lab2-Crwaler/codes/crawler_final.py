# SJTU EE208

import threading
import queue
import time
import os
import re
import string
import time
import sys
import urllib.error
import urllib.parse
import urllib.request
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
    try:
        req = urllib.request.Request(page)
        req.add_header('User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:80.0) Gecko/20100101 Firefox/80.0')
        content = urllib.request.urlopen(req,timeout=10).read().decode("utf-8")
        #添加timeout，并且将编码方式方式转化为utf-8，编码，避免产生乱码
    except:
        content = ""
    return content


def get_all_links(content, page):
    pattern = re.compile(r"(?<=a href=\").+?(?=\")|(?<=a href=\').+?(?=\')")
    try:
        out_links = pattern.findall(content)
        links = []
        for link in out_links:
            if link[0] == '/':
                link = urllib.parse.urljoin(page,link)
                links.append(link)
            elif link[:4] == 'http':
                links.append(link)
            else :
                pass
    except:
        links = []
    return links

def add_page_to_folder(page, content):  # 将网页存到文件夹里，将网址和对应的文件名写入index.txt中
    index_filename = 'index_final.txt'  # index.txt中每行是'网址 对应的文件名'
    folder = 'html'  # 存放网页的文件夹
    filename = valid_filename(page)  # 将网址变成合法的文件名
    index = open(index_filename, 'a') 
    index.write(str(page.encode('utf-8', 'ignore')) + '\t' + filename + '\n')
    #encode返回的是byte类型
    index.close()
    if not os.path.exists(folder):  # 如果文件夹不存在则新建
        os.mkdir(folder)
    f = open(os.path.join(folder, filename), 'w')
    f.write(content)  # 将网页存入文件
    f.close()


def working():
    global count
    global fil
    while True:
        page = q.get()
        if not fil.check_keyword(page):
            content = get_page(page)
            add_page_to_folder(page,content)
            outlinks = get_all_links(content,page)
            #若page在已经爬取的队列之中，我们先进行一些基本操作

            varLock.acquire()
            fil.add_keyword(page)
            if not count % 100:
                print(count)
            count += 1
            #成功加入页面之后才加一，这时候count和len是相同的
            varLock.release()

            for link in outlinks:
                q.put(link)
        q.task_done()

        #如果达到了数量，就将队列中的元素完全取清除
        if count >= max_page:
            while not q.empty():
                q.get()
                q.task_done()

if __name__ == '__main__':

    seed = "https://www.runoob.com"
    max_page = 1000
    count = 0

    start = time.time()
    NUM = 128
    fil = BloomFilter(max_page)
    #将crawled列表换为过滤器
    varLock = threading.Lock()
    q = queue.Queue()
    q.put(seed)

    for i in range(NUM):
        t = threading.Thread(target=working)
        t.setDaemon(True)
        #设定为守护线程
        t.start()
    q.join()
    #q.put使得+1，一对get与task.done使得-1，当为0的时候主线程结束，子线程自动结束

    end = time.time()
    print("{} takes {}s by final_crwaler on NUM {}".format(max_page,end - start,NUM))