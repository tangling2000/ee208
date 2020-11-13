import re
import sys
import urllib.request

from bs4 import BeautifulSoup

url = "http://daily.zhihu.com/"
req = urllib.request.Request(url)
# req.add_header('User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:80.0) Gecko/20100101 Firefox/80.0')
#按照教程，添加了消息头，不然应该不会返回我们希望的网页
content = urllib.request.urlopen(req).read()
# soup = BeautifulSoup(content)
# for tag in soup.findall('img',{'src':re.compile('^http.*\.(jpg|png)$')}):
#     print(tag)
with open('test.html','wb') as f:
    f.write(content)
soup = BeautifulSoup(content)
for tag in soup.findAll('a'):
    print(tag)
