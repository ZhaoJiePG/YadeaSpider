# Author:Aliex ZJ
#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import json
import time


from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import wait
from selenium.webdriver.support.wait import WebDriverWait
from twisted.conch.telnet import EC

from Utils.stringUtils import delSpecialChars

# start_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

start_time = '2019-12-28 15:59:59'
print('开始时间'+start_time)
option = webdriver.ChromeOptions()
option.add_argument('--proxy--server=127.0.0.1:8080')
# 防止机器识别
# option.add_experimental_option('excludeSwitches', ['enable-automation'])
option.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
option.add_argument('headless')

# 要换成适应自己操作系统的chromedriver
dirver = webdriver.Chrome(
    executable_path='D:\Maven\YadeaSpider\chromedriver.exe',
    chrome_options=option
)

# 初次建立连接, 随后方可修改cookie
dirver.get('http://www.taobao.com')
# 删除第一次登录是储存到本地的cookie
dirver.delete_all_cookies()
# 读取登录时储存到本地的cookie
with open("D:\Maven\YadeaSpider\SpliderMethods\cookies_tao.json", "r", encoding="utf8") as fp:
    ListCookies = json.loads(fp.read())

for cookie in ListCookies:
    dirver.add_cookie({
        'domain': '.taobao.com',  # 此处xxx.com前，需要带点
        'name': cookie['name'],
        'value': cookie['value'],
        'path': '/',
        'expires': None
    })

dirver.refresh()
# 再次访问页面，便可实现免登陆访问
# dirver.get("https://h5.m.taobao.com/cart/order.html?itemId=45310442213&item_num_id=45310442213&_input_charset=utf-8&buyNow=true&v=0&skuId=4229240488184&quantity=1&spm=a215p.8274340.4.d1&visa=701e9209f542c59d&_s")

while True:
    print("当前时间"+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
    if(str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))==start_time):
        # 提交订单
        dirver.get("https://h5.m.taobao.com/cart/order.html?itemId=609197376738&item_num_id=609197376738&_input_charset=utf-8&buyNow=true&v=0&skuId=4284389077805&quantity=1&spm=a215p.8274340.4.d1&visa=701e9209f542c59d&_s")
        time.sleep(0.5)
        try:
            dirver.find_element_by_xpath('//div[@id="submitOrder_1"]/div[2]/div[2]/div/span').click()
        except BaseException:
            print("=========================")
        print("结束时间"+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
        break