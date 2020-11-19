from cv2 import cv2
from matplotlib import pyplot as plt
import numpy as np

for i in range(1,4):
    #处理彩色直方图
    #读取图片
    img_bgr = cv2.imread('images/img{}.jpg'.format(i))
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    #得到数据
    feature_rgb_total = np.sum(img_rgb,axis=(0,1))
    feature_rgb = np.array([i / np.sum(feature_rgb_total) for i in feature_rgb_total])

    plt.figure()
    plt.bar(['R','G','B'],feature_rgb,color=['red','green','blue'])
    plt.ylim(0, 1) 
    plt.grid()
    plt.title('RGB histogram for img{}.jpg'.format(i))
    plt.savefig('./feature/color/img{}.jpg'.format(i),dpi=100)

    #灰度直方图
    #读取图片
    img_gray_int = cv2.imread('images/img{}.jpg'.format(i),0)
    #得到数据
    feature_gray = img_gray_int.flatten()
    #绘制图片
    plt.figure()
    plt.hist(feature_gray,bins=range(256),density = True)
    plt.xlim(0,256)
    plt.title('Grayscaness histogram for img{}.jpg'.format(i))
    plt.savefig('./feature/gray/img{}.jpg'.format(i),dpi=100)

    #梯度直方图
    #将数组类型转化为浮点，方便处理
    img_gray = img_gray_int.astype(np.float)
    #得到高度
    hight = img_gray.shape[0]
    width = img_gray.shape[1]
    #得到水平梯度梯度和竖直梯度图，并切割掉边缘不用的元素
    gy = np.array([img_gray[i+1,:]-img_gray[i-1,:] for i in range(1,hight-1)])[:,1:width-1]
    gx = np.array([img_gray[:,j+1]-img_gray[:,j-1] for j in range(1,width-1)])[:,1:hight-1].transpose()
    #对于水平梯度和竖直梯度进行处理，并压平
    feature_grad = np.floor((gy**2 + gx**2)**0.5).flatten()
    #绘制图片
    plt.figure()
    plt.hist(feature_grad,bins=range(361),density = True)
    plt.xlim(0,361)
    plt.title('Grad histogram for img{}.jpg'.format(i))
    plt.savefig('./feature/grad/img{}.jpg'.format(i),dpi=100)

#思考题
img_gray = cv2.imread('images/img{}.jpg'.format(1),0)
plt.figure(figsize=(15,5))
plt.subplot(121)
plt.title('defualt')
plt.axis('off')
plt.imshow(img_gray)
plt.subplot(122)
plt.title('gray')
plt.axis('off')
plt.imshow(img_gray,cmap="gray")
plt.savefig('./feature/comparison.jpg',bbox_inches='tight',dpi=200)