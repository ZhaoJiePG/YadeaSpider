# Author:Aliex ZJ
#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import re
from time import sleep

import requests
from bs4 import BeautifulSoup
from lxml import etree
from selenium import webdriver
url = 'https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.106.1e797e094Nlmpl&id=603373612115&skuId=4400491387330&areaId=320200&user_id=2200699946241&cat_id=2&is_b=1&rn=1de8416f4e54f3af3fbe72bbcea4459c'

# print(requests.get(url).text)

option = webdriver.ChromeOptions()
# option.add_argument('headless')

# 要换成适应自己操作系统的chromedriver
driver = webdriver.Chrome(
    executable_path='D:\Maven\YadeaSpider\Ecommerce\Data\chromedriver.exe',
    chrome_options=option
)

driver.get(url)
sleep(2)
soup = BeautifulSoup(driver.page_source,'lxml').prettify()
print(soup)
driver.get(url)
driver.quit()
