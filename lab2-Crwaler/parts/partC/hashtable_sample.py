import time
import copy
from matplotlib import pyplot as plt
from GeneralHashFunctions import GeneralHashFunctions

def make_hashtable(b):
    table = []
    for i in range(b):
        table.append([])
    return table

def hashtable_get_bucket(table,keyword):
    b = len(table)
    #得到bucket的个数，将此作为b
    index = hash_string(keyword=keyword,b=b)
    #得到索引
    bucket = table[index]
    return bucket
    #将table中对应索引的bucket返回

def hash_string(keyword,b,method="RSHash"):
    h = getattr(GeneralHashFunctions,method)(keyword)
    index = h%b
    #使用一种哈希函数得到关键字的索引
    return index

def hashtable_add(table,keyword):
    bucket = hashtable_get_bucket(table=table,keyword=keyword)
    bucket.append(keyword)
    #将是否已经存在放在外边符合函数运行逻辑，加只是一个操作，本身不应该具备检查的功能，使用时可能会造成误解

def hashtable_lookup(table,keyword):
    bucket = hashtable_get_bucket(table=table,keyword=keyword)
    for word in bucket:
        if keyword == word:
            return True
    return False
    
def get_random_string():
    import random
    return ''.join(random.sample([chr(i) for i in range(48, 123)], 6))
    #从unicode码的第48到122号字符中随机挑选六个组合形成一个单词

tocrawl = [get_random_string() for i in range(10**4)]
#初始化待爬取列表，加入10000个随机组成的六字单词
tocrawl_copy = copy.deepcopy(tocrawl)
#深度复制，产生待爬取url的副本

def time_execution(code):
    # start = time.clock()
    start = time.perf_counter()
    result = eval(code)
    # run_time = time.clock() - start
    run_time = time.perf_counter() - start
    #time。clock方法在python3.8已经被移除，使用perf_counter函数加以替代
    return run_time, result

def crawl(tocrawl):
    crawled = []
    while tocrawl:
        page = tocrawl.pop()
        if page not in crawled:
            #crawl page
            crawled.append(page)
    return crawled

def crawl_hashtable(tocrawl):
    table = make_hashtable(100)
    while tocrawl:
        page = tocrawl.pop()
        if not hashtable_lookup(table,page):
            #crawl page
            hashtable_add(table, page)
    return table

[time_crawl, crawled] = time_execution('crawl(tocrawl)')
[time_crawl_hashtable, table] = time_execution('crawl_hashtable(tocrawl_copy)')
print(time_crawl)
print(time_crawl_hashtable)
