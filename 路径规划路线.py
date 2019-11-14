#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import re
from bs4 import BeautifulSoup
import json
import xlwt

#参数输入层
ak=input("输入你的ak：（测试用：nmHAExuXWEnmuziPIMCYMFKcKNq9tchB）")
start_lon=input("输入你的起点经度：（紫金港120.09334,30.308693）")
start_lat=input("输入你的起点纬度：（紫金港120.09334,30.308693）")
end_lon=input("输入你的终点经度：（玉泉120.130656,30.271733）")
end_lat=input("输入你的终点纬度：（玉泉120.130656,30.271733）")
mid_point_num=input("输入你的途经点个数：（支持20个途经点）")
mid_point_list=[]
for i in range(0,int(mid_point_num)):
    mid_point_lon=input("输入你的第一个途经点纬度：")
    mid_point_lat=input("输入你的第一个途经点纬度：")
    mid_point_list.append({'mid_point_num':1,'mid_point_lon':mid_point_lon,'mid_point_lat':mid_point_lat})
path_preferences=input("请输入你的路径偏好：（默认值：0。可选值：0：常规路线；1：不走高速；2：躲避拥堵）")
input_coordinate_type=input("请输入你的输入坐标类型：（bd09ll：百度经纬度坐标（默认）；bd09mc：百度墨卡托坐标；gcj02：国测局加密坐标；wgs84：gps设备获取的坐标）")
output_coordinate_type=input("请输入你的输出坐标类型：（bd09ll：百度经纬度坐标（默认）：；bd09ll：百度经纬度坐标；gcj02：国测局加密坐标）")

#拼接url层
url = "http://api.map.baidu.com/direction/v"+path_preferences+"/driving?origin="+start_lat+","+start_lon+"&destination="+end_lat+","+end_lon+"&ak="+ak+"&coord_type="+input_coordinate_type+"&ret_coordtype="+output_coordinate_type

#访问web层
page = requests.get(url)
soup = BeautifulSoup(page.content,'lxml')

#正则匹配层
pattern = re.compile(r'\"path\"\:\"[0-9\.\,\;]*\"')
result1 = pattern.findall(str(soup))

#将匹配内容保存到list1
num=1;
list1=[]
for i in range (0,len(result1)):
    #print(result1[i])
    split1=str(result1[i]).lstrip('path":"').rstrip('"').split(";")
    #print(split1)
    for j in range(0,len(split1)):
        split2=str(split1[j]).split(',')
        list1.append({'num':num,'lon':split2[0],'lat':split2[1]})
        num=num+1

#输出到本地
outputpath=input("电脑输出json地址：（例如/Users/chenkaiqin/Desktop/）")
outputname=input("json文件名字：（例如a.js)")
outputlistname=input("json变量名字：（例如Point_data=)")
if __name__ == "__main__":
    fl=open(outputpath+outputname, 'w')
    fl.write(outputlistname+"=")
    fl.write(json.dumps(list1,ensure_ascii=False,indent=2))
    fl.close()



#输出到excel以便导入arcgis
outputexcelpath=input("电脑输出excel地址：（例如/Users/chenkaiqin/Desktop/）")
outputexcelname=input("excel文件名字：（例如data.xls)")
#file以utf-8格式打开
file = xlwt.Workbook(encoding='utf-8')
#创建一个名为data的表单
table = file.add_sheet('data',cell_overwrite_ok=True)
#表头信息
table_head = ['point_num', 'lat','lon']
#将表头信息写入到表格的第一行
for i in range(len(table_head)):
        table.write(0, i, table_head[i])
# produce_info_list2 是一个二维列表[['x':'1223','xx':2223,'xxxx':'333333']]
for row in range(len(list1)):
        for col in range(0, len(list1[row])):
            if (col==0):
                table.write(row+1,col,list1[row]['num'])
            elif (col==1):
                table.write(row+1,col,list1[row]['lat'])
            elif (col==2):
                table.write(row+1,col,list1[row]['lon'])
file.save(outputexcelpath+outputexcelname)

#输出信息
print("您规划的路径是从"+start_lon+","+start_lat+"到"+end_lon+','+end_lat+".")
print("您设置了"+mid_point_num+"个途经点。")
print("输出成功！"+"  您获得"+str(num)+"点数据！")


# In[ ]:




