# SJTU EE208
import re
import sys
import urllib.parse
import urllib.request

from bs4 import BeautifulSoup


def parseZhihuDaily(content, url):
    zhihulist = list()
    soup = BeautifulSoup(content)
    #解析
    for tag in soup.findAll('a',{'class':'link-button'}):
    #观察网页，知道了我们的日报是储存在a的标签之中，之后在进行遍历
        linkpage = urllib.parse.urljoin(url,tag['href'])
        #先获得我们的超链接，就在本层节点中
        src = tag.img['src']
        #图片位置储存在tag标签的子节点img中
        title = tag.span.text
        #文本信息储存在span节点的text节点中
        zhihu = [src,title,linkpage]
        #构造单个列表
        zhihulist.append(zhihu)
        #向总列表之中加入我们的值
    return zhihulist

#这个是写入的函数，就不多说了
def write_outputs(zhihus, filename):
    file = open(filename, "w", encoding='utf-8')
    for zhihu in zhihus:
        for element in zhihu:
            file.write(element)
            file.write('\t')
        file.write('\n')
    file.close()


def main():
    url = "http://daily.zhihu.com/"
    req = urllib.request.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:80.0) Gecko/20100101 Firefox/80.0')
    #按照教程，添加了消息头，知乎这些大厂再low也会稍微检测一下消息头，所以应当给予一定的尊重
    #(然后我试了试，不加消息头也会返回正确的信息，GG)
    content = urllib.request.urlopen(req).read()
    #这就跟之前一样了
    zhihus = parseZhihuDaily(content, url)
    #获得我们的列表
    write_outputs(zhihus, "result3.txt")
    #写入我们的文件


if __name__ == '__main__':
    main()