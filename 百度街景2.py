# coding: utf-8
# version: python3.5
# author: Yuhao Kang
# collect street view data from BaiduMap
 
import requests
 
 
# Baidu API request
class BaiduAPI():
    def __init__(self):
        # Your baidu api key
        self.api_key = "Y0NpLWAy0GIVoQ01e8at76T4RL8I0vID"
 
    # Each search request
    def search_photo(self, longitude, latitude):
        params = {
            "ak": self.api_key,
            "coordtype": "wgs84ll",
            "location": "{0},{1}".format(longitude, latitude),
            "fov": 360 #设置为360即为全景图
        }
        try:
            # Download pictures
            r = requests.get("http://api.map.baidu.com/panorama/v2", params)
            open("{0}_{1}.jpg".format(longitude, latitude), 'wb').write(r.content)
        except Exception as e:
            open("e:log.txt", 'a').writelines(e)
 
 
if __name__ == '__main__':
    # Read data from csv
    with open('spider_bd_map.txt', 'r') as data:
        lines = data.readlines()
        for line in lines:
            # Get coordinates
            longitude = line.split(',')[0]
            latitude = line.split(',')[1]
            # Get pictures
            baidu = BaiduAPI()
            baidu.search_photo(longitude, latitude)