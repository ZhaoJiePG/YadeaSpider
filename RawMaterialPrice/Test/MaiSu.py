# Author:Aliex ZJ
#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import datetime

from lxml import etree

import requests
import re

# 定义请求头
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
}

# 请求的网址
url = 'http://www.buyplas.com/resource/c0-200.htm'
# session接受调用cookie
response = requests.get(url=url, headers=headers)
context = response.text

# 解析
selector = etree.HTML(context)
table = []

regex = ''
items = re.findall(regex,context)
print(items)

now_time = datetime.datetime.now().strftime('%Y-%m-%d')
print(now_time)

# table.append({'date':date[0],'name':name[0],'num':num[0],'price':price[0],'danwei':danwei[0],'area':area[0]})
# print(table)