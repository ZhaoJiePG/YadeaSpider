# Author:Aliex ZJ
#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import re


class Address():

    def __init__(self):
        self.name = ''  # 地址名
        self.addr = ''  # 地址
        self.area = ''  # 区
        self.city = ''  # 市
        self.tag = ''   # 标签
        self.prov = ''  # 省

    def fill(self, info):
        # 摘取信息
        name = re.findall('"geo_type":.*,"name":"(.*?)","navi_update_time', info)
        if name: self.name = name[0]
        tag = re.findall('std_tag":"(.*?)"', info)
        if tag and tag[0] != '': self.tag = tag[0]
        else:
            tag = re.findall('di_tag":"(.*?)"', info)
            if tag: self.tag = tag[0]
        addr = re.findall('addr":"(.*?)"', info)
        if addr:  self.addr = addr[0]
        area = re.findall('area_name":"(.*?)","city_id', info)
        if area: self.area = area[0]
        city = re.findall('city_name":"(.*?)"',info)
        if city: self.city = city[0]
        prov = re.findall('\[(.*?)\(.*\|', info)
        if prov: self.prov = prov[0]

    def __str__(self):
        string = self.name+'\n'+self.addr+'\n'+self.prov+self.city+self.area+'\n'+self.tag
        return string