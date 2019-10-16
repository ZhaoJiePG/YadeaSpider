# Author:Aliex ZJ
#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import time

import requests
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait


headers = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9",
    "cookie": "cna=L0CwFSqRDGgCAd9EwPN4s9v5; t=3f886137b6f604509bea316d5773e8af; _tb_token_=33135eebeb15b; cookie2=1b0b4e285c2d20c244c712d49635efa6; dnk=%5Cu767D%5Cu767D%5Cu7684%5Cu72D7%5Cu5C3E%5Cu5DF4%5Cu82B1; uc1=pas=0&lng=zh_CN&cookie16=W5iHLLyFPlMGbLDwA%2BdvAGZqLg%3D%3D&cookie15=U%2BGCWk%2F75gdr5Q%3D%3D&cookie21=URm48syIYn73&existShop=false&tag=8&cookie14=UoTbnV%2BOqCmL2A%3D%3D; uc3=id2=UUpjN4zrNdJETg%3D%3D&lg2=VT5L2FSpMGV7TQ%3D%3D&vt3=F8dByuDnzROHAQ3X%2FeU%3D&nk2=05emRgpWdtZcceNuDGg%3D; tracknick=%5Cu767D%5Cu767D%5Cu7684%5Cu72D7%5Cu5C3E%5Cu5DF4%5Cu82B1; lid=%E7%99%BD%E7%99%BD%E7%9A%84%E7%8B%97%E5%B0%BE%E5%B7%B4%E8%8A%B1; uc4=nk4=0%400SwjusWimre0H6WrAcFT6cSTu0IPkewtmQ%3D%3D&id4=0%40U2gp9xkNePhwkA3mujHlbSd34BVR; _l_g_=Ug%3D%3D; unb=2221579274; lgc=%5Cu767D%5Cu767D%5Cu7684%5Cu72D7%5Cu5C3E%5Cu5DF4%5Cu82B1; cookie1=VWsu%2BpKF9hE9HePBZc%2FExBxRmsDaR97K6DS4nKh4iu0%3D; login=true; cookie17=UUpjN4zrNdJETg%3D%3D; _nk_=%5Cu767D%5Cu767D%5Cu7684%5Cu72D7%5Cu5C3E%5Cu5DF4%5Cu82B1; sg=%E8%8A%B145; csg=029a3cd0; enc=x%2BbRQuO%2FU%2FgQU1XAlsZpeiOZ1IHkZYtObQTBaOQawfBHOzzdocAvLvbm28eF8EIDr9V4tZaW0jnMGkmhRNm10g%3D%3D; otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; whl=-1%260%260%260; x=__ll%3D-1%26_ato%3D0; l=cBSH0T-4q4bTAKD8BOCgCZMInnbO9LAfguWXRJ8ei_5ZZsTVpQbOkiBbsU96cjWFTw8B4nnADjetjecb-yWfoTB7K9cdvdC..; isg=BHV1MEyeRJRSkKAV4I7I9ewrkfElZ3NQbmaCt_eaDOx4zpTAv0Nq1eSIGNLdjkG8",
    "referer": "https://detail.tmall.com/item.htm?spm=a1z10.3-b-s.w4011-18877415626.1339.10f56546p15MJZI&id=596624138584&sku_properties=8369595:5557472",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3732.400 QQBrowser/10.5.3819.400"}


url = "https://detail.tmall.com/item.htm?spm=a1z10.3-b-s.w4011-18877415626.1339.10f56546p16MJZI&id=588699357283&skuId=4355060574815"
response = requests.get(url,headers).text
print(response)


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