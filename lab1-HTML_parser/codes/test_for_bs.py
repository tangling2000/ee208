import re
import sys
import urllib.request

from bs4 import BeautifulSoup

if __name__ == '__main__':
    url = "http://www.baidu.com"
    content = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(content)
    for url in soup.findAll('a',{'href':re.compile('^http.*')})[0:2]:
        print(type(url['href']))
