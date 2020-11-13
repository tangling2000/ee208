# 第二次作业文档说明

## 文件说明  

>文件说明中，主要对于文件的用途，产生方式进行介绍。

在总文件夹下，有img文件夹，,codes文件夹，readme.md，report.tex，report.pdf文件，img文件夹存放用于书写报告用的截图，图片等，readmemd，report.tex，report.pdf文件用于对于作业进行说明。

codes文件夹中包括：

+ html文件夹，用于存放爬虫爬下来的页面

+ Biarray.py : 一个用于实现BloomFilter的子类模块

+ BloomFilter.py :实现并进行实验测试BloomFilter的模块

+ crawler.py : 线性顺序爬虫的实现

+ crawler_multi_thread.py : 多线程爬虫的实现

+ crawler_final.py : 加入了BloomFilter的多线程爬虫的实现

+ index : crawler.py 中爬取的链接列表

+ index_mul :crawler_multi_thread.py 中爬取的链接列表

+ index_final : crawler_final.py 中爬取的链接列表

## 测试方法说明

>对于如何实现作业中的要求，的流程进行说明

+ 作业一，实现BloomFilter：测试程序写进了模块的主程序，所以直接对于py文件进行编译即可，其中会将理论和实际的出错率打印到终端（其中hash函数直接在类中进行了重写，所以这里并没有提交有很多哈希函数的哪个模块）

+ 作业二，实现简单的网页爬虫：直接运行crawler.py即可，可以在主程序中修改max_page变量，改变最大的爬取数量，中途每爬取一定数量（10个）的页面就会打印数字，实现进度条功能，最终还会打印程序运行的时间。

+ 作业三，实现多线程爬虫：直接运行crawler_multi_thread.py即可，可以在主程序中修改max_page变量——改变最大的爬取数量，修改NUM变量——改变线程的数量，中途每爬取一定数量（100个）的页面就会打印数字，实现进度条功能，最终还会在终端上打印程序运行的时间，线程数，爬取页面数等信息。

+ 作业拓展：拓展问题的部分在报告中进行了回答，额外实现的带有BloomFilter的多线程爬虫实现在crawler_final.py文件，操作和得到的输出，与多线程爬虫基本一致。
