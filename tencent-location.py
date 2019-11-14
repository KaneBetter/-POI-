import requests
import json
import pandas as pd


# TODO 最大经度，最小经度，最大纬度，最小纬度，注意，必须为整数格式，并且小数点后保留两位
max_lon_default=11930
min_lon_default=11823
max_lat_default=3270
min_lat_default=3115

def get_TecentData(count=4, rank=0):  # 先默认为从rank从0开始
    url = 'https://xingyun.map.qq.com/api/getXingyunPoints'
    locs = ''
    paload = {'count': count, 'rank': rank}
    response = requests.post(url, data=json.dumps(paload))
    datas = response.text
    dictdatas = json.loads(datas)  # dumps是将dict转化成str格式，loads是将str转化成dict格式
    time = dictdatas["time"]  # 有了dict格式就可以根据关键字提取数据了，先提取时间
    file_time = time.replace(":", "-")

    file_name = 'TencentData-' + str(file_time).split(' ')[0] + '-' + str(file_time).split(' ')[1] + ".csv"
    locs = dictdatas["locs"]  # 再提取locs（这个需要进一步分析提取出经纬度和定位次数）
    locss = locs.split(",")
    # newloc=[locss[i:i+3] for i in range(0,len(locss),3)]
    temp = []  # 搞一个容器
    for i in range(int(len(locss) / 3)):
        lat = locss[0 + 3 * i]  # 得到纬度
        lon = locss[1 + 3 * i]  # 得到经度
        count = locss[2 + 3 * i]

        if(min_lat_default<int(lat)<max_lat_default and  min_lon_default<int(lon)<max_lon_default):
            temp.append([int(lat) / 100, int(lon) / 100,   count, time])  # 容器追加四个字段的数据：时间，纬度，经度和定位次数

    if len(temp) == 0:
        print('没爬到数据===================')
        return
    print("temp:===========" + str(temp))
    result = pd.DataFrame(temp)  # 用到神器pandas，
    result.dropna()  # 去掉脏数据，相当于数据过滤了
    result.columns = ['lat', 'lon', 'count', 'time']
    print(file_name)
    result.to_csv(file_name, mode='a', index=False)  # model="a",a的意思就是append，可以把得到的数据一直往TecentData.txt中追加


if __name__ == '__main__':

    get_TecentData()