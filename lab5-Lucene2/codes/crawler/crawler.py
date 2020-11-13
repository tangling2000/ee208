# SJTU EE208

import threading
import queue
import time
import os
import re
import string
import sys
import urllib.error
import urllib.parse
import urllib.request
import GeneralHashFunctions  
from Bitarray import Bitarray  #引入Bitarray中的类

from bs4 import BeautifulSoup


def Hash_LookUp(page):  #查找page是否存在
    global constant
    for func in dir(GeneralHashFunctions):
        if  func.endswith("Hash"):
            if crawled.get(abs(getattr(GeneralHashFunctions,func)(page))%constant)==1:
                continue
            else :
                return 1
    return 0        


def valid_filename(s):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    s = ''.join(c for c in s if c in valid_chars)
    return s


def get_page(page):
    print('downloading page %s' % page)
    content = ''
    try:
        content = urllib.request.urlopen(page,timeout=4).read()
    except :
        pass
    
    return content


def get_all_links(content, page):
    links = []
    soup = BeautifulSoup(content,'html.parser')
    f=0

    for i in soup.findAll('a',{'href' : re.compile('^https.*guancha|^/.*')}):
        if re.compile('.*?s=|.*#comment').match(i.get('href','')):
            continue

        if re.compile('^http').match(i.get('href','')):
            links.append(i.get('href',''))
            
        else :
            links.append(urllib.parse.urljoin(page,i.get('href','')))
    # print(str(content))
    # link_list =re.findall(r"(?<=a href=\").+?(?=\")|(?<=a href=\').+?(?=\')" ,str(content))  #利用re来查找所有a链href之间的值 ，参考https://blog.csdn.net/zhuhengv/article/details/50342213
    # for i in link_list:
    #     if re.compile('^http').match(i):
    #         links.append(i)
    #     elif re.compile('^/').match(i):
    #         links.append(urllib.parse.urljoin(page,i))

    # content = ''.join(soup.get_text())
    if soup.find('div',{'class':'content all-txt'}):
        img = []
        text = soup.find('div',{'class':'content all-txt'})
        for i in text.findAll('img'):
            url = ' '
            info = ' '
            url=i.get('src')
            try:
                info=i.parent.next_sibling.next_sibling.text
            except:
                try:
                    info=i.parent.previous_sibling.previous_sibling.text
                except:
                    info = text.text
            if info == '':
                continue
            url = url.replace('\n','')
            url = url.replace('\t','')
            info = info.replace('\n','')
            info = info.replace('\t','')
            img = img + ['img_url:',url,'\n','img_info:',info,'\n']
        img = ''.join(img)
        content = ''.join([soup.head.title.text ,'\n',img])


    else:
        f=1
    


    return list(set(links)), content,f


def add_page_to_folder(page, content):  # 将网页存到文件夹里，将网址和对应的文件名写入index.txt中
    try:
        index_filename = 'index_guancha_photo.txt'  # index.txt中每行是'网址 对应的文件名'
        folder = 'guancha_photo'  # 存放网页的文件夹
        filename = valid_filename(page)  # 将网址变成合法的文件名
        index = open(index_filename, 'a',encoding='utf-8')
        index.write(page + '\t' + filename + '\n')
        index.close()
        if not os.path.exists(folder):  # 如果文件夹不存在则新建
            os.mkdir(folder)
        f = open(os.path.join(folder, filename), 'w', encoding='utf-8')
        f.write(''.join([page,'\n',content]))  # 将网页存入文件
        f.close()
        return 1
    except:
        return 0

count=0

def working():
    global max_page,count 
    while True:
    
        page = q.get()
        f=0

        varLock.acquire()              #查找时也需要使用全局变量，所以上锁
        if Hash_LookUp(page):
            varLock.release()          #这里释放查找时上的锁
            content = get_page(page)
            outlinks,content,f = get_all_links(content,page)
            
            

            varLock.acquire()          
            for link in outlinks:
                if(max_page<=0):      
                    break
                q.put(link)

            for func in dir(GeneralHashFunctions):
                if func.endswith('Hash'):
                    crawled.set(abs(getattr(GeneralHashFunctions,func)(page))%constant)
        
            if max_page<=0:
                varLock.release()
                print("Clearing...")
                while q.empty()==0:
                    q.task_done()
                    page=q.get()
                
                varLock.acquire()
                print("complete")
        

            if f==0 and add_page_to_folder(page,content):
                max_page-=1

        
            varLock.release()
            
        else:
            varLock.release()   #这里释放查找不匹配情况下，查找上的锁
        q.task_done()
    
        




start = time.time()
NUM = 128             #线程数
# seed = sys.argv[1]    
# max_page = int(sys.argv[2])
seed = 'https://www.guancha.cn/'
max_page = 7000
crawled = Bitarray(max_page*20)
constant = max_page*20   #Hash值需要%的常数
varLock = threading.Lock()
q = queue.Queue()
q.put(seed)
for i in range(NUM):
    t = threading.Thread(target=working)
    t.setDaemon(True)
    t.start()
q.join()
end = time.time()
print(end - start)
print(max_page)
