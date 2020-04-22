import datetime
import random
import re
import time
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import pandas as pd
import pymysql
from lxml import etree
import requests

from RawMaterialPrice.Ingress import getUrlList
from Utils import stringUtils
from Utils.stringUtils import delSpecialChars

now_time = datetime.datetime.now().strftime('%Y-%m-%d')
now_day = datetime.datetime.now().strftime('%d')

if now_day[0:1] == '0':
    now_day = now_day[1:2]
else:
    now_day = now_day

now_day = '14'

# 保存表数据
table = []

option = webdriver.ChromeOptions()
# option.add_argument('headless')
driver = webdriver.Chrome(executable_path='../chromedriver.exe', chrome_options=option)
# 模拟登陆
driver.get('https://jiegougang.mysteel.com/')
driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/span').click()
# 账号密码
userName = driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/form/div[2]/input")
userName.send_keys('xinzhi')
password = driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/form/div[3]/input[1]")
password.send_keys('88920398')
login = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/form/div[7]')
login.click()

time.sleep(5)
#1.Cr系合结钢(40CrΦ20-28)
print("开始获取Cr系合结钢(40CrΦ20-28)材料价格")
mySteelUrls = getUrlList('../Data/RawUrl.csv', '我的钢铁网')
stellurl1 = mySteelUrls[0]
origin_name = stellurl1['我的钢铁网'][0]
steelUrl = stellurl1['我的钢铁网'][1]
driver.get(steelUrl)
time.sleep(1)
button = driver.find_element_by_link_text('{}日上海市场Cr系合结钢价格行情'.format(now_day))
real_url = button.get_attribute('href')

print("爬取材料："+origin_name+"网址为"+real_url)
sleep(1)
driver.get(real_url)
sleep(1)
xpath_date = etree.HTML(driver.page_source)
# 数据更新日期
tr_list = xpath_date.xpath('//table[@id="marketTable"]/tbody/tr')
for tr in tr_list:
    try:
        # origin_name = 'Cr系合结钢(40CrΦ20-28)'
        name = delSpecialChars(tr.xpath('./td[1]/a/text()')[0])
        paihao = delSpecialChars(tr.xpath('./td[2]/text()')[0])
        guige = delSpecialChars(tr.xpath('./td[4]/text()')[0])
        area = delSpecialChars(tr.xpath('./td[5]/text()')[0])
        real_name = name+'('+guige+')'
        if(origin_name == real_name and area=='杭钢' and paihao=='40Cr'):
            price = delSpecialChars(tr.xpath('./td[6]/text()')[0])
            steelDict = {'name': real_name, 'area': area, 'date': now_time, 'price': price, 'add_time': now_time}
            print(steelDict)
            table.append(steelDict)
    except BaseException:
        print("error")
        continue
print('{}日上海市场Cr系合结钢价格行情获取成功'.format(now_day))
print('===================================================')


#2.热轧板卷(5.5-11.75*1500*CQ235B)
print("开始获取热轧板卷(5.5-11.75*1500*CQ235B)材料价格")
mySteelUrls = getUrlList('../Data/RawUrl.csv', '我的钢铁网')
stellurl1 = mySteelUrls[1]
origin_name = stellurl1['我的钢铁网'][0]
steelUrl = stellurl1['我的钢铁网'][1]
driver.get(steelUrl)
time.sleep(1)
for path in ['（15：40）','（09：35）','（09：30）','（11：10）','（14:25）']:
    try:
        button = driver.find_element_by_link_text('{0}日{1}上海市场热轧板卷价格行情'.format(now_day,path))
        real_url = button.get_attribute('href')
        print("当前时间有数据")
        break
    except BaseException:
        print("当前时间没有数据，跳出此页")
        continue
sleep(1)
driver.get(real_url)
sleep(1)
xpath_date = etree.HTML(driver.page_source)
# 数据更新日期
# date = delSpecialChars(xpath_date.xpath('/html/body/div[8]/div[2]/div[1]/div[1]/text()')[0])[0:10]
tr_list = xpath_date.xpath('//table[@id="marketTable"]/tbody/tr')
for tr in tr_list:
    try:
        # origin_name = 'Cr系合结钢(40CrΦ20-28)'
        name = delSpecialChars(tr.xpath('./td[1]/a/text()')[0])
        paihao = delSpecialChars(tr.xpath('./td[3]/text()')[0])
        guige = delSpecialChars(tr.xpath('./td[2]/text()')[0])
        area = delSpecialChars(tr.xpath('./td[4]/text()')[0])
        real_name = name+'('+guige+')'
        # print(real_name + area)
        if(origin_name == real_name and area=='鞍钢/本钢' and paihao=='Q235B'):
            price = delSpecialChars(tr.xpath('./td[5]/text()')[0])
            steelDict = {'name': real_name, 'area': area, 'date': now_time, 'price': price, 'add_time': now_time}
            print(steelDict)
            table.append(steelDict)
    except BaseException:
        print("error")
        continue
print('{0}日{1}上海市场热轧板卷价格行情价格行情获取成功'.format(now_day,path))
print('===================================================')

#3.冷轧无取向硅钢(0.5*1200*C)
print("开始获取冷轧无取向硅钢(0.5*1200*C)材料价格")
mySteelUrls = getUrlList('../Data/RawUrl.csv', '我的钢铁网')
stellurl1 = mySteelUrls[2]
origin_name = stellurl1['我的钢铁网'][0]
steelUrl = stellurl1['我的钢铁网'][1]
driver.get(steelUrl)
time.sleep(1)
button = driver.find_element_by_link_text('{}日上海市场无取向硅钢价格行情'.format(now_day))
real_url = button.get_attribute('href')

sleep(1)
driver.get(real_url)
sleep(1)
xpath_date = etree.HTML(driver.page_source)
# 数据更新日期
# date = delSpecialChars(xpath_date.xpath('/html/body/div[8]/div[2]/div[1]/div[1]/text()')[0])[0:10]
tr_list = xpath_date.xpath('//table[@id="marketTable"]/tbody/tr')
for tr in tr_list:
    try:
        name = delSpecialChars(tr.xpath('./td[1]/a/text()')[0])
        paihao = delSpecialChars(tr.xpath('./td[3]/text()')[0])
        guige = delSpecialChars(tr.xpath('./td[2]/text()')[0])
        area = delSpecialChars(tr.xpath('./td[4]/text()')[0])
        real_name = name+'('+guige+')'
        # print(real_name + area)
        if(origin_name == real_name and area=='宝钢' and paihao=='B50A350'):
            price = delSpecialChars(tr.xpath('./td[5]/text()')[0])
            steelDict = {'name': real_name, 'area': area, 'date': now_time, 'price': price, 'add_time': now_time}
            print(steelDict)
            table.append(steelDict)
    except BaseException:
        print("error")
        continue
print('{}日上海市场无取向硅钢价格行情价格行情获取成功'.format(now_day,path))
print('===================================================')
print(table)
driver.quit()