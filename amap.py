# -*- coding: utf-8 -*-
import urllib 
import csv 
import string
import json   
import sys
from urllib.parse import quote
import urllib.request as ur

left_bottom = [120.140183,30.30831];  # 设置区域左下角坐标（高德坐标系） 紫金公园
right_top = [120.041114,30.228378]; #浙江工业大学屏风校区


part_n = 1;  # 设置区域网格（2*2）
url0 = 'https://restapi.amap.com/v3/place/polygon?';
x_item = (right_top[0]-left_bottom[0])/part_n;
y_item = (right_top[1]-left_bottom[1])/part_n;
keyword = '酒店'; #搜索关键词设置
key = '0ff4147adb9a40e6c505efec4c8dfef4'; #高德地图api信令
n = 0; # 切片计数器
datacsv=open("22224.csv", "a+", encoding="utf-8",newline='');
csvwriter = csv.writer(datacsv, dialect=("excel"))
for i in range(part_n):
    for j in range(part_n):
        left_bottom_part = [left_bottom[0]+i*x_item,left_bottom[1]+j*y_item]; # 切片的左下角坐标
        right_top_part = [left_bottom[0]+(i+1)*x_item,left_bottom[1]+(j+1)*y_item]; # 切片的右上角坐标

        for k in range(100):
            url = url0 + '&polygon=' + str(left_bottom_part[0]) + ',' + str(left_bottom_part[1]) + '|'+str(right_top_part[0]) + ',' + str(right_top_part[1]) + '&keywords=' + keyword + '&offset=25&page=' + str(k)  + '&output=json&key=' + key;      
            print(url)
            s=quote(url, safe=string.printable)
            data = ur.urlopen(s);
            hjson = json.loads(data.read().decode('utf-8'));
            if hjson['info'] == 'OK':
                results = hjson['pois'];          
                for m in range(len(results)): # 提取返回的结果
                    csvwriter.writerow(list(results[m].values()))
        n += 1;
        print ('第',str(n),'个切片入库成功')
datacsv.close()

#试例url ： https://restapi.amap.com/v3/place/polygon?polygon=116.460988,40.006919|116.48231,40.007381|116.47516,39.99713|116.472596,39.985227|116.45669,39.984989|116.460988,40.006919&keywords=kfc&output=json&key=0ff4147adb9a40e6c505efec4c8dfef4