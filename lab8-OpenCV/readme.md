# 第8次作业文档说明ß

## 文件说明  

>文件说明中，主要对于文件的用途，产生方式进行介绍。

在总文件夹下，有img文件夹，codes文件夹，readme.md，report.tex，report.pdf文件，img文件夹存放用于书写报告用的截图，图片等，readmemd，report.tex，report.pdf文件用于对于作业进行说明。

codes文件夹中包括：
+ feature 文件夹：存放实验结果图片的文件夹，其中color代表RGB直方图，grad代表梯度直方图，gray代表梯度直方图，comparison用于比较真实灰度图的显示。
+ images 文件夹：用于存放原始图片的文件夹。
+ work.ipynb ：存放作业源代码的jupyter文件。
+ work.py ：存放作业源代码的py文件。

## 测试方法说明

>对于如何实现作业中的要求，的流程进行说明

对于作业中的各种图片的显示，可以直接运行，work.ipynb的各个代码块，第2，3，4代码块分别生成RGB直方图，灰度直方图，以及梯度直方图，最后一个代码块生成真实灰度图以及cv2直接显示的灰度图的对比。

也可以直接运行work.py文件，直接生成所有的图片。