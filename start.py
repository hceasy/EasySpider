# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import time
import json


def getRoomList(url):
    reqHeader = {
        'Host': 'sz.lianjia.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,en-US;q=0.7,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'Cookie': 'select_city=440300; cityCode=sh; lianjia_uuid=50bece17-32e4-4f76-b384-8d24a6e14011; ubt_load_interval_b=1490665455607; ubt_load_interval_c=1490665455607; ubta=2299869246.2859018361.1490665438473.1490665463631.1490665466358.3; ubtb=2299869246.2859018361.1490665466359.13C9D0AD6D8B1B86F360EE54F7CD1F04; ubtc=2299869246.2859018361.1490665466359.13C9D0AD6D8B1B86F360EE54F7CD1F04; ubtd=3; all-lj=0a26bbdedef5bd9e71c728e50ba283a3; lianjia_ssid=9ebc6414-8aeb-4201-a86c-19c0d0c91a36; _smt_uid=58d9bffb.49b98bac',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    HtmlConts = requests.get(url, headers=reqHeader)
    _htmlBody = BeautifulSoup(HtmlConts.content, 'lxml')
    _roomList = _htmlBody.select('ul#house-lst li')
    _max = len(_roomList)
    # _max = 1
    t = 0
    while (t < _max):
        _address = '深圳市' + _roomList[t].select('div.other div.con a')[0].get_text().replace(
            '中心租房', '').replace('租房', '') + _roomList[t].select('div.where a.laisuzhou span.region')[0].get_text().replace(' ', '').replace('\xa0', '')
        _price = _roomList[t].select(
            'div.col-3 div.price span.num')[0].get_text()
        try:
            _price = int(_price)
        except:
            return
        _roomSize = _roomList[t].select(
            'div.col-1 span.meters')[0].get_text().replace(' ', '').replace('平米', '')
        _roomSize = int(_roomSize)
        print(_roomSize, _price, _address)
        _index = _price / _roomSize
        _ApiUrl = 'http://apis.map.qq.com/ws/geocoder/v1/?address=' + \
            _address + '&key=K3ABZ-U2PA3-5E33S-3OU5C-QNOEE-AGFSC'
        print(_ApiUrl)
        _addressJson = json.loads(requests.get(_ApiUrl).text)
        if (int(_addressJson['status']) == 0):
            _lng = _addressJson['result']['location']['lng']
            _lat = _addressJson['result']['location']['lat']
            print(('{"lng":%f,"lat":%f,"index":%f},') % (_lng, _lat, _index))
            try:
                with open('E:/Users/Heasy/Desktop/jiage/lianjiasz.txt', 'r') as f:
                    _cont = f.read()
            finally:
                pass
            with open('E:/Users/Heasy/Desktop/jiage/lianjiasz.txt', 'w') as f:
                f.write(_cont + ('{"lng":%f,"lat":%f,"index":%f},') %
                        (_lng, _lat, _index))
        else:
            print(_addressJson)
        t = t + 1
        time.sleep(0.2)


def getList(max):
    _max = max
    t = 1
    while (t <= _max):
        reqURL = 'http://sz.lianjia.com/zufang/pg' + str(t) + '/'
        getRoomList(reqURL)
        t = t + 1
        print(t)


getList(100)
