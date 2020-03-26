import datetime
import random
import re
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import pandas as pd
import pymysql
from lxml import etree
import requests

from Utils import stringUtils
from Utils.stringUtils import delSpecialChars

# 保存表数据
table = []

option = webdriver.ChromeOptions()
# option.add_argument('headless')
driver = webdriver.Chrome(executable_path='../chromedriver.exe', chrome_options=option)

driver.get('https://jiegougang.mysteel.com/')

driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/span').click()

userName = driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/form/div[2]/input")
userName.send_keys('xinzhi')

password = driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/form/div[3]/input[1]")
password.send_keys('88920398')

login = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/form/div[7]')
login.click()
sleep(2)
driver.get("https://rezha.mysteel.com/m/20/0317/09/6141965A7684FF13.html")
sleep(1)
xpath_date = etree.HTML(driver.page_source)

tr_list = xpath_date.xpath('//table[@id="marketTable"]/tbody/tr')

for tr in tr_list:
    print(tr)
    try:
        origin_name = 'Cr系合结钢(40CrΦ20-28)'
        name = delSpecialChars(tr.xpath('./td[1]/a/text()')[0])
        paihao = delSpecialChars(tr.xpath('./td[2]/text()')[0])
        guige = delSpecialChars(tr.xpath('./td[4]/text()')[0])
        area = delSpecialChars(tr.xpath('./td[5]/text()')[0])
        real_name = name+'('+paihao+guige+')'
        if(origin_name == real_name and area=='杭钢'):
            print(real_name)
            print(delSpecialChars(tr.xpath('./td[6]/text()')[0]))

    except BaseException:
        print("error")
        continue

