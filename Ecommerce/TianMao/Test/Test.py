# Author:Aliex ZJ
#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import re
import time

import requests
from lxml import etree
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait


headers = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9",
    "cookie": "cna=L0CwFSqRDGgCAd9EwPN4s9v5; otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; x=__ll%3D-1%26_ato%3D0; t=3f886137b6f604509bea316d5773e8af; _tb_token_=566eee53ee01; cookie2=1b75d79b47265d251e10fab5baa12bd3; _m_h5_tk=449dee344f5265b55448239d53d1d5ea_1571223838598; _m_h5_tk_enc=8b2015d089a666045b850d29cb1dffea; dnk=%5Cu767D%5Cu767D%5Cu7684%5Cu72D7%5Cu5C3E%5Cu5DF4%5Cu82B1; lid=%E7%99%BD%E7%99%BD%E7%9A%84%E7%8B%97%E5%B0%BE%E5%B7%B4%E8%8A%B1; whl=-1%260%260%260; x5sec=7b22726174656d616e616765723b32223a226364373332303536336432373632316434303834333838643033356339393732434965306d2b3046454c62633135534431704c6464686f4d4d6a49794d5455334f5449334e447378227d; uc1=existShop=false&cookie21=VFC%2FuZ9ainBZ&pas=0&cookie15=W5iHLLyFOGW7aA%3D%3D&cookie16=Vq8l%2BKCLySLZMFWHxqs8fwqnEw%3D%3D&tag=8&cookie14=UoTbnKFVTCOKJg%3D%3D&lng=zh_CN; uc3=id2=UUpjN4zrNdJETg%3D%3D&vt3=F8dByuDsdUXD9npZbSQ%3D&lg2=WqG3DMC9VAQiUQ%3D%3D&nk2=05emRgpWdtZcceNuDGg%3D; tracknick=%5Cu767D%5Cu767D%5Cu7684%5Cu72D7%5Cu5C3E%5Cu5DF4%5Cu82B1; _l_g_=Ug%3D%3D; uc4=id4=0%40U2gp9xkNePhwkA3mujHk7ASAPgyW&nk4=0%400SwjusWimre0H6WrAcFT6cSTuthSJsZbtw%3D%3D; unb=2221579274; lgc=%5Cu767D%5Cu767D%5Cu7684%5Cu72D7%5Cu5C3E%5Cu5DF4%5Cu82B1; cookie1=VWsu%2BpKF9hE9HePBZc%2FExBxRmsDaR97K6DS4nKh4iu0%3D; login=true; cookie17=UUpjN4zrNdJETg%3D%3D; _nk_=%5Cu767D%5Cu767D%5Cu7684%5Cu72D7%5Cu5C3E%5Cu5DF4%5Cu82B1; sg=%E8%8A%B145; csg=cc99f275; enc=B2JID5w8jPfQ4Tmstb2yNtMyWzqqyQqbLWe7bGuqziBTY%2B%2Blk1oKU1jmJlpeeZZH9de7CSzOp0s8heJya%2F2xyw%3D%3D; l=dBSH0T-4q4bTAGh3BOCgIZMInnbttLAfguWXRJ8ei_5Ij_LEg97OkgzTtEp6cjWcGMYB4nnADjetYecu-yWfoTB7K9cdvdHJBef..; isg=BMXFPHNuNOLtJBAFsB6YxTxbwQH1FyNAXvbSh8cqyfwTXuTQj9PY5TL4aMINHpHM",
    "referer": "https://detail.tmall.com/item.htm?spm=a1z10.3-b-s.w4011-18877415626.1339.10f56546p15MJZI&id=596624138584&sku_properties=8369595:5557472",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3732.400 QQBrowser/10.5.3819.400"}

# url  = 'https://dsr-rate.tmall.com/list_dsr_info.htm?itemId=596624138584&spuId=1243962245&sellerId=2817130358' \
#        # '&groupId&_ksTS=1571271589884_207&callback=jsonp208'
# print(url)
# url = 'https://rate.tmall.com/list_detail_rate.htm?itemId=596624138584&spuId=1243962245&sellerId=2817130358&order=3&currentPage=1'
# url = url.replace('rate.tmall.com','dsr-rate.tmall.com') \
#     .replace('list_detail_rate','list_dsr_info.htm') \
#     .replace('&order=3&currentPage=1','')
url = 'https://detail.tmall.com/item.htm?spm=a1z10.3-b-s.w4011-18877415626.1339.10f56546p18MJZI&id=594730742591&sku_properties=8369595:5557472'
print(url)
response = requests.get(url, headers=headers)
data = response.text
print(data)
comment_datas = re.findall('{.*}', data)[0]
print(comment_datas)
print(type(comment_datas))
res = dict(comment_datas)['dsr']['gradeAvg']
print(res)

# url = "https://detail.tmall.com/item.htm?spm=a1z10.3-b-s.w4011-18877415626.1339.10f56546p15MJZI&id=596624138584"
# response = requests.get(url).text
# print(response)
# print(re.findall('"reservePrice":"(\d*\.\d*)"',str(response)))
# print(re.findall('"defaultItemPrice":"(\d*\.\d*)"',str(response)))

# option = webdriver.ChromeOptions()
# # option.add_argument('headless')
#
# # 要换成适应自己操作系统的chromedriver
# driver = webdriver.Chrome(
#     executable_path='D:\Maven\YadeaSpider\Ecommerce\Data\chromedriver.exe',
#     chrome_options=option
# )
#
# url = "https://detail.tmall.com/item.htm?spm=a1z10.3-b-s.w4011-18877415626.1339.10f56546p16MJZI&id=588699357283&skuId=4355060574815"
# driver.get(url)
#
# time.sleep(3)
#
# print(driver.title)
# # print(driver.page_source)
#
# timeout = 5
# id1 = WebDriverWait(driver, timeout).until(
#     lambda d: d.find_element_by_xpath('//*[@id="J_TabBar"]/li[2]/a')
#     # EC.presence_of_element_located((By.XPATH, '//input[@id="kw"]'))
# )
# print("=======")
# print(id1.text)