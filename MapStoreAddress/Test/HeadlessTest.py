# Author:Aliex ZJ
#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import re
from time import sleep

from lxml import etree
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


# location='/server/python/selenium/geckodriver'
location='D:\Maven\YadeaSpider\MapStoreAddress\geckodriver.exe'

driver = webdriver.Firefox(executable_path=location)
# option.add_argument('headless')
url = 'https://map.baidu.com'

# 打开网站
driver.get(url)

# 打印当前页面标题
print(driver.title)
driver.close()