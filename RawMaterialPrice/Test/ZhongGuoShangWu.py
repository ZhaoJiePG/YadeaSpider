# Author:Aliex ZJ
#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from lxml import etree

import requests
import re

# 定义请求头
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
    'cookie':'CompNew=0; UserCount=50F+zk6pYMYaLB9DEbsmQVXIH7avJgZdFCNIlVNWP2mRuhYcc9jRJu8VOgNG54oSUkPk6IFXC90fKrXa/Ytnw0U67INIqgVL; Hm_lvt_8c905ec8d12584debce091e1b8c39fc3=1559366230,1559446331,1559693340; ASP.NET_SessionId=dktbkt55q4hhlu55tzkyky55; Hm_lvt_55f4388cb1206cf827c03a4f9ff5cbd0=1559706263,1559780001,1560042660,1560127522; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; CustInfo=50F+zk6pYMasBvSZvR0fH4yeunqew1exUNl6etVB1vPXhK00v20l/rtSxJld2EVWSE71m086t5a3wNPQWY76X+8MPmeWI1OZLCSevsnvuSBAmmuQWULJ23imk3vLCe2KkVnuiOJLNLl4Qmnctq90qBB8Z5cx6lzgkuenq2JmvYQ=; Hm_lpvt_55f4388cb1206cf827c03a4f9ff5cbd0=1560151284'
}

# # session模拟用户登陆=cookiejar
# session = requests.session()
#
# # 模拟的登陆页面
# post_url = "http://www.chinaccm.cn/MemberCenter/Login.aspx"
#
# # post请求保存的账号密码
# post_data = {"txtUserName": "yadea雅迪科技", "txtPassWord": "yadea001"}
#
# # 模拟登陆
# responsee = session.post(url=post_url, data=post_data, headers=headers)
# # print(responsee.content.decode())
#
# cookies = session.cookies

# 二次请求的网址
url='http://www.chinaccm.cn/PriceData/PriceData.aspx?Type=DATA_NATIONALPRICE%2c%E5%9B%BD%E5%86%85%E4%BB%B7%E6%A0%BC&Cata=1&scode=341402&limit=ManuName%2c%E5%8D%8E%E5%B3%B0%3b&dshow=SuppName%2cGrade%2cDate%2cPrice'


# session接受调用cookie
response = requests.get(url=url, headers=headers)
context = response.text

# 解析
table = []
# 解析
selector = etree.HTML(context)
date = selector.xpath('//tr[@class="dmain_right_tab_list"][2]/td[3]/text()')
print(date)
name = selector.xpath('//tr[@class="dmain_right_tab_list"][2]/td[1]/text()')
num = selector.xpath('//tr[@class="dmain_right_tab_list"][2]/td[2]/text()')
res_name = str(name[0]) + '(' + str(num[0]) + ')'
price = selector.xpath('//tr[@class="dmain_right_tab_list"][2]/td[4]/text()')
table.append({'name': res_name, 'date': date[0], 'price': price[0]})



print(table)