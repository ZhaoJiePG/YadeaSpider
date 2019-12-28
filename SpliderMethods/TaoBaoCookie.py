# Author:Aliex ZJ
#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import json
from selenium import webdriver

option = webdriver.ChromeOptions()
option.add_argument('--proxy--server=127.0.0.1:8080')
# 防止机器识别
option.add_experimental_option('excludeSwitches', ['enable-automation'])

# option.add_argument('headless')

# 要换成适应自己操作系统的chromedriver
driver = webdriver.Chrome(
    executable_path='D:\Maven\YadeaSpider\chromedriver.exe',
    chrome_options=option
)

driver.get('https://login.taobao.com/member/login.jhtml?redirectURL=http%3A%2F%2Fbuyertrade.taobao.com%2Ftrade%2Fitemlist%2Flist_bought_items.htm%3Fspm%3D875.7931836%252FB.a2226mz.4.66144265Vdg7d5%26t%3D20110530')
# 这里是为了等待手机扫码登录, 登录后回车即可
input("请回车登录")
dictCookies = driver.get_cookies()
jsonCookies = json.dumps(dictCookies)
# 登录完成后,将cookies保存到本地文件
with open("./cookies_tao.json", "w") as fp:
    fp.write(jsonCookies)