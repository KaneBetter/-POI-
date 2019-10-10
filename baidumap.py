# -*- coding: utf-8 -*-
import urllib 
import csv 
import string
import json   
import sys
from urllib.parse import quote
import urllib.request as ur
left_bottom = [120.041095,30.149111];  # 设置区域左下角坐标（百度坐标系） 香山文化创意园
right_top = [120.220469,30.296903]; # 设置区域右上角坐标（百度坐标系） 杭州东站
#left_bottom = [120.047994,30.234518];  # 设置区域左下角坐标（百度坐标系） 浙工大屏风校区
#right_top = [120.146305,30.314114]; # 设置区域右上角坐标（百度坐标系） 紫金公园
#left_bottom = [118.351816,29.192344];  # 设置区域左下角坐标（百度坐标系）
#right_top = [118.554718,29.550779]; 


part_n = 7;  # 设置区域网格（2*2）
url0 = 'http://api.map.baidu.com/place/v2/search?';
x_item = (right_top[0]-left_bottom[0])/part_n;
y_item = (right_top[1]-left_bottom[1])/part_n;
query = '酒店'; #搜索关键词设置
ak = 'Cn9S9Pld37yAFg2Lj9BrwCV0IjrSl69C'; #百度地图api信令
n = 0; # 切片计数器
datacsv=open("34444.csv", "a+", encoding="utf-8",newline='');
csvwriter = csv.writer(datacsv, dialect=("excel"))
for i in range(part_n):
    for j in range(part_n):
        left_bottom_part = [left_bottom[0]+i*x_item,left_bottom[1]+j*y_item]; # 切片的左下角坐标
        right_top_part = [left_bottom[0]+(i+1)*x_item,left_bottom[1]+(j+1)*y_item]; # 切片的右上角坐标
        #left_bottom_part = [left_bottom[0]+i*x_item,left_bottom[1]+j*y_item]; # 切片的左下角坐标
        #right_top_part = [right_top[0]+i*x_item,right_top[1]+j*y_item]; # 切片的右上角坐标

        for k in range(20):
            url = url0 + 'query=' + query + '&page_size=20&page_num=' + str(k) + '&scope=1&bounds=' + str(left_bottom_part[1]) + ',' + str(left_bottom_part[0]) + ','+str(right_top_part[1]) + ',' + str(right_top_part[0]) + '&output=json&ak=' + ak;      
            s=quote(url, safe=string.printable)
            data = ur.urlopen(s);
            hjson = json.loads(data.read().decode('utf-8'));
            if hjson['message'] == 'ok':
                results = hjson['results'];          
                for m in range(len(results)): # 提取返回的结果
                    csvwriter.writerow(list(results[m].values()))
        n += 1;
        print ('第',str(n),'个切片入库成功')
datacsv.close()
