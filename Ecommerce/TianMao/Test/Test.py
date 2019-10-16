# Author:Aliex ZJ
#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import time

import requests
from lxml import etree
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait


headers = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9",
    "cookie": "cna=L0CwFSqRDGgCAd9EwPN4s9v5; otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; x=__ll%3D-1%26_ato%3D0; t=3f886137b6f604509bea316d5773e8af; _tb_token_=566eee53ee01; cookie2=1b75d79b47265d251e10fab5baa12bd3; _m_h5_tk=449dee344f5265b55448239d53d1d5ea_1571223838598; _m_h5_tk_enc=8b2015d089a666045b850d29cb1dffea; dnk=%5Cu767D%5Cu767D%5Cu7684%5Cu72D7%5Cu5C3E%5Cu5DF4%5Cu82B1; uc1=lng=zh_CN&cookie14=UoTbnKFVSMp%2FgQ%3D%3D&existShop=false&pas=0&cookie16=UIHiLt3xCS3yM2h4eKHS9lpEOw%3D%3D&tag=8&cookie21=VT5L2FSpczFp&cookie15=URm48syIIVrSKA%3D%3D; uc3=vt3=F8dByuDsdUk70sMmjXw%3D&lg2=URm48syIIVrSKA%3D%3D&id2=UUpjN4zrNdJETg%3D%3D&nk2=05emRgpWdtZcceNuDGg%3D; tracknick=%5Cu767D%5Cu767D%5Cu7684%5Cu72D7%5Cu5C3E%5Cu5DF4%5Cu82B1; lid=%E7%99%BD%E7%99%BD%E7%9A%84%E7%8B%97%E5%B0%BE%E5%B7%B4%E8%8A%B1; _l_g_=Ug%3D%3D; uc4=id4=0%40U2gp9xkNePhwkA3mujHk7ASEEfB0&nk4=0%400SwjusWimre0H6WrAcFT6cSTuthSIm6c8g%3D%3D; unb=2221579274; lgc=%5Cu767D%5Cu767D%5Cu7684%5Cu72D7%5Cu5C3E%5Cu5DF4%5Cu82B1; cookie1=VWsu%2BpKF9hE9HePBZc%2FExBxRmsDaR97K6DS4nKh4iu0%3D; login=true; cookie17=UUpjN4zrNdJETg%3D%3D; _nk_=%5Cu767D%5Cu767D%5Cu7684%5Cu72D7%5Cu5C3E%5Cu5DF4%5Cu82B1; sg=%E8%8A%B145; csg=0fec1004; enc=MlWQUta4quK3OLr1eBmlnoMWCzPV9ufOqEdL33TbR7vzXA9n50GScF4XSpXHihsa6aMUMr27RjIKS9s782TA2Q%3D%3D; whl=-1%260%260%260; l=dBSH0T-4q4bTAJ9WBOCgIZMInnbOGLAVguWXRJ8ei_5dasTvxn7Okgzu8U96cjWcGwLB4nnADjetLe4TJy6foTB7K9cdvdHJBef..; isg=BE5OBQzbnx-F8CsAL8ODKHseiiQaWkiduVNJQniX1dEf2-w14F4D2WpdE0cSQwrh",
    # "referer": "https://detail.tmall.com/item.htm?spm=a1z10.3-b-s.w4011-18877415626.1339.10f56546p15MJZI&id=596624138584&sku_properties=8369595:5557472",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3732.400 QQBrowser/10.5.3819.400"}


url = "https://detail.tmall.com/item.htm?spm=a1z10.3-b-s.w4011-18877415626.1339.10f56546p15MJZI&id=596624138584"
response = requests.get(url).text
# print(response)
selector = etree.HTML(response)
item = selector.xpath('//*[@id="J_AttrUL"]/li')
for i in item:
    print(i)
    print(i.xpath('./text()'))

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