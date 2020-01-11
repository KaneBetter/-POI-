# _*_ coding: utf-8 _*_

import urllib
from urllib.request import urlopen
import threading
from optparse import OptionParser
from bs4 import BeautifulSoup
import sys
import re
from cv2 import cv2
try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse
import queue
import hashlib
import matplotlib.pyplot as plt
import numpy as np


def download(url, name):
    conn = urlopen(url)
    outimg = conn.read()
    data_img = cv2.imdecode(np.asarray(bytearray(outimg), dtype=np.uint8), 1)
    conn.close()#这里一定要关闭，不然爬几次之后会报连接错误
    cv2.imwrite(name, data_img)
    plt.imshow(data_img)    
    print('Pic Saved!')
    return data_img

fp = open("spider_bd_map.txt","r") # 我的是沿一条直线爬数据，txt里面存的是起点和终点的经纬度坐标，向下面一样
#116.375654,39.99982
#116.375923,39.993643

start_end_points = fp.readlines()
start_point = start_end_points[0]
start_point = start_point.strip('\n')
start_point = start_point.split(',')
start_point_jin = start_point[0]
start_point_wei = start_point[1]

end_point = start_end_points[1]
end_point = end_point.strip('\n')
end_point = end_point.split(',')
end_point_jin = end_point[0]
end_point_wei = end_point[1]

jins = np.arange(float(start_point_jin)*1000000, float(end_point_jin)*1000000, 1)*0.000001
points_num = len(jins)
weis = np.linspace(float(start_point_wei)*1000000, float(end_point_wei)*1000000, points_num)*0.000001

for iPoint in range(points_num):
    jin = jins[iPoint]
    wei = weis[iPoint]
    #这里要注意下，对应的经纬度没有街景图的地方，输出的会是无效图片
    print(jin, wei)
    img_name = "out_image\\beijing\\" + str(jin) + "_" + str(wei) +".jpg"
    url = "http://api.map.baidu.com/panorama/v2?ak=Y0NpLWAy0GIVoQ01e8at76T4RL8I0vID&width=1024&height=512&location="+str(jin)+","+str(wei)+"&fov=180"  # 你的KEY"
    print(url)
    outimg = download(url, img_name)

fp.close()