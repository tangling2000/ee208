# SJTU EE208

import re
import sys
import urllib.request

from bs4 import BeautifulSoup


def parseURL(content):
    img_set = set()
    #创建树
    soup = BeautifulSoup(content)
    #用tag遍历所有我们符合条件的节点，我们当然按照要求在a中搜索href，并且用正则表达式的方式拟合
    for tag in soup.findAll('img',{'src':re.compile('^http.*\.(jpg|png)$')}):
    #这里我们匹配的是用jpg或者png结尾的图片，应该世面上大部分都是这个格式才对
        url = tag['src']
        img_set.add(url)
    return img_set


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
    write_outputs(urlSet, "result2.txt")

if __name__ == '__main__':
    main()
