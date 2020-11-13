# SJTU EE208

import re
import sys
import urllib.request

from bs4 import BeautifulSoup


def parseURL(content):
    urlset = set()
    #创建树
    soup = BeautifulSoup(content)
    #用tag遍历所有我们符合条件的节点，我们当然按照要求在a中搜索href，并且用正则表达式的方式拟合
    for tag in soup.findAll('a',{'href':re.compile('^http.*')}):
        url = tag['href']
        if (url[-4:] != '.jpg') and (url[-4:] != '.png'):
    #去掉后边四位是.jpg和png的链接来排除图片地址
            urlset.add(url)
    return urlset


def write_outputs(urls, filename):
    file = open(filename, 'w', encoding='utf-8')
    for i in urls:
        file.write(i)
        file.write('\n')
    file.close()


def main():
    url = "http://www.baidu.com"
    content = urllib.request.urlopen(url).read()
    urlSet = parseURL(content)
    write_outputs(urlSet, "result1.txt")

if __name__ == '__main__':
    main()
