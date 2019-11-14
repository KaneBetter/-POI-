# -*- coding:utf-8 -*-
# 第一行必须有，否则报中文字符非ascii码错误
import urllib.request
from urllib.parse import quote
import numpy as np
import json
import pandas as pd
from pandas import Series, DataFrame


#TODO 1
# 高德上申请的key
key = '6363r65fghfrrr' # 需替换为自己的
# TODO 2 搜索的城市名(全名)
addr_name = '福建'


url = 'http://restapi.amap.com/v3/config/district?'
def getlnglat(address):

    uri = url + 'keywords=' + quote(address) + '&key=' + key + '&subdistrict=1' + '&extensions=all'

    # 访问链接后，api会回传给一个json格式的数据
    temp = urllib.request.urlopen(uri)

    temp = json.loads(temp.read())

    # polyline是坐标，name是区域的名字
    Data = temp["districts"][0]['polyline']
    name = temp["districts"][0]['name']
    # polyline数据是一整个纯文本数据，不同的地理块按照|分，块里面的地理信息按照；分，横纵坐标按照，分，因此要对文本进行三次处理
    Data_Div1 = Data.split('|')  # 对结果进行第一次切割，按照|符号
    len_Div1 = len(Data_Div1)  # 求得第一次切割长度

    num = 0
    len_Div2 = 0  # 求得第二次切割长度，也即整个数据的总长度
    while num < len_Div1:
        len_Div2 += len(Data_Div1[num].split(';'))
        num += 1

    num = 0
    num_base = 0
    output = np.zeros((len_Div2, 5)).astype(np.float)  # 循环2次，分割；与，
    while num < len_Div1:
        temp = Data_Div1[num].split(';')
        len_temp = len(temp)
        num_temp = 0
        while num_temp < len_temp:
            output[num_temp + num_base, :2] = np.array(temp[num_temp].split(','))  # 得到横纵坐标
            output[num_temp + num_base, 2] = num_temp + 1  # 得到横纵坐标的连接顺序
            output[num_temp + num_base, 3] = num + 1  # 得到块的序号
            num_temp += 1
        num_base += len_temp
        num += 1

    output = DataFrame(output, columns=['经度', '纬度', '连接顺序', '块', '名称'])
    output['名称'] = name

    return output


def getSubName(address):  # 获取搜索区域的名称，部分区域例如鼓楼重名太多，因此返回城市代码，将城市代码作为参数给上述函数

    uri = url + 'keywords=' + quote(address) + '&key=' + key + '&subdistrict=1' + '&extensions=all'

    temp = urllib.request.urlopen(uri)
    temp = json.loads(temp.read())

    list0 = temp['districts'][0]['districts']
    num_Qu = 0
    output = []
    while num_Qu < len(list0):
        output.append(list0[num_Qu]['adcode'])
        num_Qu += 1

    return output


num = 0
ad = getSubName(addr_name)  # 得到福州下属区域的城市代码
add = getlnglat(addr_name)  # 得到福州整个的边界数据
while num < len(ad):
    add = pd.concat([add, getlnglat(ad[num].encode("utf-8"))])  # 得到福州下属的全部区域的边界数据
    num += 1
add.to_csv('{0}.csv'.format(addr_name), encoding='gbk')
