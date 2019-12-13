import datetime
import random
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import pandas as pd
import pymysql
from lxml import etree
import requests

now_time = datetime.datetime.now().strftime('%Y-%m-%d')

def praseMaiSu():
    # 保存表数据
    table = []
    timeout = 2
    option = webdriver.ChromeOptions()
    # option.add_argument('headless')
    # 要换成适应自己操作系统的chromedriver
    driver = webdriver.Chrome(executable_path='../chromedriver.exe', chrome_options=option)
    # option.add_argument('headless')

    index = 205
    while True:
        url = 'https://weixin.sogou.com/weixin?type=2&s_from=input&query=买塑观察 第{}期'.format(index)
        driver.get(url)
        index = index - 1

        # 模拟点击“搜索”
        try:
            search_button = WebDriverWait(driver, timeout).until(
                lambda d: d.find_element_by_xpath('//a[@id="sogou_vr_11002601_title_0"]'))
            search_button.click()
        except BaseException:
            print('当前网页数据不匹配')
            continue

        driver.close()

        # 切换页面右边
        window_handles = driver.window_handles
        driver.switch_to.window(window_handles[-1])
        # print(driver.page_source)
        xpath_date = etree.HTML(driver.page_source)
        sleep(5)
        print('当前的期数为：' + str(index + 1))

        qi_key = ''
        try:
            qi_key = xpath_date.xpath('//div[@id="js_content"]/section[2]/section/section/p[2]/strong/span[1]/text()')[
                0]
            print('实际期数：' + qi_key)
            qi_key = int(qi_key)
        except IndexError:
            print('当前网页数据不匹配')
            continue
        except ValueError:
            print('当前网页数据不匹配')
            continue

        if int(index + 1) == qi_key:
            xpath_date = etree.HTML(driver.page_source)
            name = 'ABS' + '(' + str(
                xpath_date.xpath('//div[@id="js_content"]/table[14]/tbody/tr/td[1]/span/strong/text()')[0]) + ')'
            area = xpath_date.xpath('//*[@id="js_content"]/table[14]/tbody/tr/td[2]/span/text()')[0]
            price = xpath_date.xpath('//*[@id="js_content"]/table[14]/tbody/tr/td[3]/span/text()')[0]
            price = price.replace(',', '')
            table.append({'name': name, 'area': area, 'date': now_time, 'price': price, 'add_time': now_time})

            xpath_date = etree.HTML(driver.page_source)
            name = 'PC' + '(' + str(
                xpath_date.xpath('//*[@id="js_content"]/table[23]/tbody/tr/td[1]/span/strong/text()')[0]) + ')'
            area = xpath_date.xpath('//*[@id="js_content"]/table[23]/tbody/tr/td[2]/span/text()')[0]
            price = xpath_date.xpath('//*[@id="js_content"]/table[23]/tbody/tr/td[3]/span/text()')[0]
            price = price.replace(',', '')
            table.append({'name': name, 'area': area, 'date': now_time, 'price': price, 'add_time': now_time})

            driver.quit()
            break
        else:
            print('当前网页数据不匹配')
            continue
    return table

praseMaiSu()