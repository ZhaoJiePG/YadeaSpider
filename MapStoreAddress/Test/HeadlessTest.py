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
driver = webdriver.Chrome(executable_path='../chromedriver.exe',chrome_options=option)
# option.add_argument('headless')

index = 250
while True :
    url = 'https://weixin.sogou.com/weixin?type=2&s_from=input&query=买塑观察 第{}期'.format(index)
    driver.get(url)
    index = index-1

    # 模拟点击“搜索”
    try:
        search_button = WebDriverWait(driver, timeout).until(
            lambda d: d.find_element_by_xpath('//a[@id="sogou_vr_11002601_title_0"]'))
        search_button.click()
    except BaseException:
        print('当前网页数据不匹配')
        continue

    driver.close()

    # 切换页面
    window_handles = driver.window_handles
    # 切换到右边的下一个页面
    driver.switch_to.window(window_handles[-1])
    # print(driver.page_source)
    xpath_date = etree.HTML(driver.page_source)

    sleep(20)

    print('当前的期数为：'+str(index+1))
    qi_key = ''
    try:
        qi_key = xpath_date.xpath('//div[@id="js_content"]/section[1]/section/section/p[2]/strong/span[1]/text()')[0]
    except IndexError:
        print('当前网页数据不匹配')
        continue

    print('实际期数：'+qi_key)
    if int(index+1) == int(qi_key):
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
        driver.close()
        break
    else:
        print('当前网页数据不匹配')
        continue

driver.quit()