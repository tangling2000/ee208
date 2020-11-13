# SJTU EE208
import time

def get_page(page):
    print("downloading page {}".format(page))
    time.sleep(0.5)
    return g.get(page, [])
    #字典的get方法，第一个参数是访问的键，第二个参数是访问失败返回的默认值


def get_all_links(content):
    return content
    #没有任何意义，因为我们这里是模拟，而非真实URL


def union_dfs(a, b):
    #这里b代表产生的新url，a代表待爬取的队列
    for e in b:
        if e not in a:
            a.append(e)
            #若e不在a，就把e放进a的尾部



def union_bfs(a, b):
    #这里b代表待爬队列，a代表已经爬取的队列，e代表新获得的url
    for e in b:
        if e not in a:
            a.insert(0,e)
            #若e不再a，就把e放进a的头部


def crawl(seed, method):
    tocrawl = [seed]
    crawled = []
    graph = {}
    while tocrawl:
        page = tocrawl.pop()
        #从待爬取队列中弹出一个url
        if page not in crawled:
            content = get_page(page)
            #从url中获得信息
            outlinks = get_all_links(content)
            #从信息中得到新的url列表

            graph[page] = outlinks
            #这一步进行对图进行操作，将一个url于其产生的url列表以键值对的形式存储在字典中
            #没有对于顺序进行重排，因为字典本来就没有顺序

            globals()['union_{}'.format(method)](tocrawl, outlinks)
            #globals返回这个模块中所有全局对象，包括变量，函数，类，以键值对返回，
            #键是对象对的名称，值是对象的“实质”，这里访问函数就是直接调用函数。
            #以两种方式，将新得到的URL放进待爬取的列表
            crawled.append(page)
            #把这个已经爬到的物体放进历史的尘埃
    return graph, crawled
    #返回我们的url结构，以及爬过的url列表（crwal本身就反应了一种次序。）


g = {'A': ['B', 'C', 'D'],
        'B': ['E', 'F'],
        'D': ['G', 'H'],
        'E': ['I', 'J'],
        'G': ['K', 'L']}


graph_dfs, crawled_dfs = crawl('A', 'dfs')
print('graph_dfs:', graph_dfs)
print('crawled_dfs:', crawled_dfs)

graph_bfs, crawled_bfs = crawl('A', 'bfs')
print('graph_bfs:', graph_bfs)
print('crawled_bfs:', crawled_bfs)
