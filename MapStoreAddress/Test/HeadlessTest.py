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

timeout=2
option = webdriver.ChromeOptions()
# option.add_argument('headless')
# 要换成适应自己操作系统的chromedriver
driver = webdriver.Chrome(
    executable_path='../chromedriver.exe',
    chrome_options=option)


# option.add_argument('headless')
url = 'https://mp.weixin.qq.com/s/Q7Vy8MkgD2GROWQInJUXEQ'


# 打开网站
driver.get(url)

# 模拟点击“搜索”
# search_button = WebDriverWait(driver, timeout).until(
#     lambda d: d.find_element_by_xpath('//div[@id="WXAPPMSG1000000321"]/div/h4'))
# search_button.click()
# sleep(2)

# 切换页面
window_handles = driver.window_handles
# 切换到右边的下一个页面
driver.switch_to.window(window_handles[-1])

# print(driver.page_source)
xpath_date = etree.HTML(driver.page_source)
name = xpath_date.xpath('//div[@id="js_content"]/table[14]/tbody/tr/td[1]/span/strong/text()')[0]
area = xpath_date.xpath('//*[@id="js_content"]/table[14]/tbody/tr/td[2]/span/text()')[0]
price = xpath_date.xpath('//*[@id="js_content"]/table[14]/tbody/tr/td[3]/span/text()')[0]
name1= 'ABS塑件'
print(name +area+price)

xpath_date = etree.HTML(driver.page_source)
name = xpath_date.xpath('//*[@id="js_content"]/table[23]/tbody/tr/td[1]/span/strong/text()')[0]
area = xpath_date.xpath('//*[@id="js_content"]/table[23]/tbody/tr/td[2]/span/text()')[0]
price = xpath_date.xpath('//*[@id="js_content"]/table[23]/tbody/tr/td[3]/span/text()')[0]

print(name +area+price)

# 打印当前页面标题
# driver.close()