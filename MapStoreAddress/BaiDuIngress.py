# Author:Aliex ZJ
#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
采用selenium+requests模拟点击百度地图获取门店信息
'''
import datetime
import json
import re
from time import sleep
import pandas as pd
import requests
from lxml import etree
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from Utils.fileUtils import fileUtils
from Utils.mysqlUtils import createTable, save_to_mysql

now_time = datetime.datetime.now().strftime('%Y-%m-%d')


# 模拟请求方法
def BaiDuStoreInfo(queryKey,stores_list):
    url = 'https://map.baidu.com'
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    # 要换成适应自己操作系统的chromedriver
    driver = webdriver.Chrome(
        executable_path='./chromedriver.exe',
        chrome_options=option)


    # 打开网站
    driver.get(url)

    citys = fileUtils().getCsvFile('D:\Maven\YadeaSpider\MapStoreAddress\Data\Baidu_cityCode.csv')
    for city in citys:
        querycity = city[1]
        # 在搜索框中输入文字
        timeout = 5
        search_content = WebDriverWait(driver, timeout).until(
            lambda d: d.find_element_by_xpath('//input[@id="sole-input"]'))
        search_content.send_keys('{0}'.format(querycity+queryKey+'电动车'))
        sleep(2)

        # 模拟点击“搜索”
        search_button = WebDriverWait(driver, timeout).until(
            lambda d: d.find_element_by_xpath('//button[@id="search-button"]'))
        search_button.click()
        sleep(2)
        xpath_date = etree.HTML(driver.page_source)
        count_num = 1
        # 总共多少结果
        try:
            count_num = re.findall('共找到(\d+)个搜索结果',driver.page_source)[0]
            print(querycity+'共找到{0}个搜索结果'.format(count_num))
        except IndexError:
            print("没有搜索结果，进入下一个城市")
            try:
                # 点击清空搜索
                search_button = WebDriverWait(driver, timeout).until(
                    lambda d: d.find_element_by_xpath('//div[@class="searchbox-content-button right-button loading-button cancel-button"]'))
                search_button.click()
            except BaseException:
                print("没有清按钮")
            continue


        # 循环翻页获取所有门店
        for i in range(0,int(float(count_num)/10)+1):
            sleep(2)
            xpath_date = etree.HTML(driver.page_source)
            print("开始获取"+queryKey+"==>"+querycity+"第"+str(i+1)+"页数据")
            li_lists = xpath_date.xpath('//ul[@class="poilist"]/li')
            for li_list in li_lists:
                # 存储结果
                store_address = ''
                store_name = ''
                lon = ''
                lat = ''
                try:
                    store_address = li_list.xpath('./div[@class="cf"]//div[@class="row addr"]/span[@class="n-grey"]/text()')[0]
                    store_name = li_list.xpath('./div[@class="cf"]//div[@class="row"]/span[1]/a/text()')[0]
                    # 请求百度接口获取经纬度
                    reponse = requests.get('http://api.map.baidu.com/geocoding/v3/?address={0}&output=json&ak=K2WGZeDWlluoHpEpt5qo5Sx6VNyvffLB&callback=showLocation&city={1}'.format(store_address,querycity)).text
                    lon_lat = (json.loads(re.findall('{.*}',reponse)[0])['result']['location'])
                    lon = lon_lat['lng']
                    lat = lon_lat['lat']
                except BaseException:
                    print("数据错误或者无法解析经纬度")
                    continue
                # print(re.findall('showLocation&&showLocation(.*)',json.loads(resonsnse)))
                store_dict={'topic':queryKey,'store_address':store_address,'store_name':store_name,
                            'lon':lon,'lat':lat,'add_time':now_time}
                print(store_dict)
                stores_list.append(store_dict)


            # 模拟点击“下一页”
            # xpath_date = etree.HTML(driver.page_source)
            try:
                search_button = WebDriverWait(driver, timeout).until(
                    lambda d: d.find_element_by_xpath('//a[@tid="toNextPage"]'))
                search_button.click()
            except BaseException:
                print('没有下一页,退出循环')
                break

        # 点击清空搜索
        search_button = WebDriverWait(driver, timeout).until(
            lambda d: d.find_element_by_xpath('//div[@class="searchbox-content-button right-button loading-button cancel-button"]'))
        search_button.click()
        sleep(2)
        print()
    driver.close()


if __name__ == '__main__':
    # 查询条件
    queryKeys =['小刀','台铃','小牛','立马','新大洲','新蕾','金箭',
                '倍特','杰宝大王','绿佳','绿驹','玉骑铃','比德文','雅迪','爱玛','绿源','新日']
    for queryKey in queryKeys:
        stores_list = []
        BaiDuStoreInfo(queryKey,stores_list)
        # 保存数据到文件
        fileUtils().saveAsCsv(stores_list, './Data/Stores/{0}'.format(queryKey))
        # print(stores_list)

    # 建表
    # resData = pd.read_csv('D:\Maven\YadeaSpider\MapStoreAddress\Data\Stores\小刀.csv',encoding='utf-8')
    # resData = resData.astype(object).where(pd.notnull(resData), None)
    # createTable(resData,'dim','bd_store_info','127')

    # 保存数据
    # file_addr = './Data/Stores'
    # save_to_mysql(file_addr,'dim','bd_store_info','127')