# Author:Aliex ZJ
#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import re

import requests

# url='https://item.jd.com/53704257271.html'

# headers = {
#     'Accept': '*/*',
#     'Accept-Encoding': 'gzip,deflate,br',
#     'Accept-Language': 'zh-CN,zh;q=0.9',
#     'Connection': 'keep-alive',
#     'Cookie': 'unpl=V2_ZzNtbUZVQBIlDBNTeBhbAGIDEl5KVEpHcw1HVi5JDFZmBhpaclRCFX0URlVnGV8UZwcZXUNcQRFFCEdkeBBVAWMDE1VGZxBFLV0CFSNGF1wjU00zQwBBQHcJFF0uSgwDYgcaDhFTQEJ2XBVQL0oMDDdRFAhyZ0AVRQhHZHsZWARjBhBeRFdzJXI4dmR%2fGlsBZQMiXHJWc1chVEZceBpfSGcDFlxGUkEWcwh2VUsa; __jdu=1150543271; shshshfpa=0cb162de-cb82-21b8-49a7-7e1fd26a3efd-1570864191; user-key=d5809892-c823-402e-9748-c84b2469d56f; cn=0; shshshfp=4ecb84897eabb0f7a4c6348b7cdc7d0a; __jda=122270672.1150543271.1570864187.1570867576.1572223296.3; __jdc=122270672; __jdv=122270672|direct|-|none|-|1572223296470; shshshfpb=eTsoprn6f4hkN00S8LggPuQ%3D%3D; areaId=12; ipLoc-djd=12-984-3384-0; 3AB9D23F7A4B3C9B=NW7TBRN3JQ7SSFS7HGFCEWZV3PDRCFWGRICQPKCUAHPCAR5EUO4EC2N2WMNWLCQZZPJS6AKO2JGFXOQNTMYMAE764U; __jdb=122270672.2.1150543271|3.1572223296; shshshsID=4bf52b5e4dd7daa1f6ad27cfe7777316_2_1572223314309',
#     'Host': 'btshow.jd.com',
#     'Referer': 'https://item.jd.com/53704257271.html',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3732.400 QQBrowser/10.5.3819.400'
# }
# url = 'https://item.jd.com/27156324216.html'
# response = requests.get(url,headers=headers).text
# print(response)
from bs4 import BeautifulSoup
from lxml import etree
from selenium import webdriver

from Utils.stringUtils import delSpecialChars

# option = webdriver.ChromeOptions()
# option.add_argument('headless')
# option.add_argument('incognito')
# driver = webdriver.Chrome(
#     executable_path='D:\Maven\YadeaSpider\Ecommerce\Data\chromedriver.exe',
#     chrome_options=option)

url='https://item.jd.com/27156324216.html'

# response = requests.get(url).text
# driver.get(url)

# html_doc = driver.page_source
# res = etree.HTML(html_doc)
# print(html_doc)
# print('=====')
# name = delSpecialChars(res.xpath('//div[@class="sku-name"]/text()')[0])
# print(name)

# print(re.findall('<divclass="sku-name">(.*)</div><divclass="news">',html_doc))
# print('==========')
# print(re.findall('<lidata-tab="trigger"data-anchor="#detail".*>([\u4e00-\u9fa5]+)</li>',html_doc))
# driver.quit()


page = 259

for i in range(0,int(259/10+1)):
    print(i)