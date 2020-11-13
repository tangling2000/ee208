# SJTU EE208

import os
import re
import string
import time
import sys
import urllib.error
import urllib.parse
import urllib.request

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


def union_bfs(a, b):
    for e in b:
        if e not in a:
            a.insert(0,e)
#修改为广度优先


def add_page_to_folder(page, content):  # 将网页存到文件夹里，将网址和对应的文件名写入index.txt中
    index_filename = 'index.txt'  # index.txt中每行是'网址 对应的文件名'
    folder = 'html'  # 存放网页的文件夹
    filename = valid_filename(page)  # 将网址变成合法的文件名
    index = open(index_filename, 'w') #修改为w，使得可以反复爬取
    index.write(str(page.encode('utf-8', 'ignore')) + '\t' + filename + '\n')
    #encode返回的是byte类型
    index.close()
    if not os.path.exists(folder):  # 如果文件夹不存在则新建
        os.mkdir(folder)
    f = open(os.path.join(folder, filename), 'w')
    f.write(content)  # 将网页存入文件
    f.close()


def crawl(seed, max_page):
    tocrawl = [seed]
    crawled = []

    while tocrawl:
        page = tocrawl.pop()
        if page not in crawled:
            content = get_page(page)
            add_page_to_folder(page, content)
            outlinks = get_all_links(content, page)
            union_bfs(tocrawl, outlinks)
            crawled.append(page)
        if len(crawled) >= max_page:
            break
        #如果长度大于最大长度，跳出循环
    return crawled


if __name__ == '__main__':

    seed = "https://www.runoob.com/"
    max_page = 100
    [time_crwal,crawled] = time_execution("crawl(seed, max_page)")
    print(time_crwal)