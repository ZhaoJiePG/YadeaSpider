# Author:Aliex ZJ
# !/usr/bin/env python3
# -*- coding:utf-8 -*-
import datetime
import re
import pandas as pd
from time import sleep

import requests
from lxml import etree
from selenium import webdriver
from bs4 import BeautifulSoup

from Utils.requestsUtils import getRandomAgent
from Utils.stringUtils import delSpecialChars
from Utils.fileUtils import fileUtils
from Utils.mysqlUtils import save_to_mysql, createTable

# 爬取搜索商品数据，selinum+requests

now_time = datetime.datetime.now().strftime('%Y-%m-%d')


def JDCarsInfo(car_name):
    # 产品信息集合
    product_list = []
    # selenium 参数
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    option.add_argument('incognito')
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    option.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
    driver = webdriver.Chrome(
        executable_path='D:\Maven\YadeaSpider\chromedriver.exe',
        chrome_options=option)
    # 请求的url
    url = 'https://search.jd.com/Search?keyword={0}&enc=utf-8'.format(car_name)
    # 请求连接
    driver.get(url)
    sleep(2)
    html_doc = driver.page_source
    # 主动设置 bs4的解析库,BeautifulSoup对象
    soup = BeautifulSoup(html_doc, 'lxml').prettify()
    # 获取页码(判断是否有页数)
    pages = etree.HTML(soup).xpath('//*[@id="J_bottomPage"]/span[2]/em[1]/b/text()')
    if len(pages) == 0:
        pages = '1'
    else:
        pages = re.findall('\d+', pages[0])[0]
    print('*****开始爬取' + car_name + '：总共' + pages + '页*****')
    sleep(1)
    # 循环解析查询页数
    for page in range(1, int(pages)+1):

    # for page in range(5):
        url = 'https://search.jd.com/Search?keyword={0}&enc=utf-8&page={1}'.format(car_name, str(page * 2 - 1))
        print('睡眠2s...开始爬取第' + str(page) + '页========url为' + url)
        driver.get(url)
        #sleep(2)
        # 调用xpath解析库
        xpath_date = etree.HTML(BeautifulSoup(driver.page_source, 'lxml').prettify())
        products = xpath_date.xpath('//*[@id="J_goodsList"]/ul/li')
        for product in products:
            # 产品信息
            try:
                prod_store = delSpecialChars(product.xpath('.//a[@class="curr-shop hd-shopname"]/text()')[0])
                prod_price = delSpecialChars(product.xpath('./div/div[3]/strong/i/text()')[0])
                prod_price = prod_price[:-((prod_price.index('.'))-1)]
                prod_url = 'https:'+delSpecialChars(product.xpath('./div/div[4]/a/@href')[0])
                prod_id = re.findall('(\d+)',prod_url)[0]
                store_url = 'https:'+delSpecialChars(product.xpath('./div/div[7]/span/a/@href')[0])
                store_id = re.findall('(\d+)',store_url)[0]
                store_rates = '评价'+delSpecialChars(product.xpath('./div/div[5]/strong/a/text()')[0])

                # 跳转商品url，获取详细信息
                driver.get(prod_url)
                prod_reponse = driver.page_source
                # sleep(1)
                selector = etree.HTML(prod_reponse)
                prod_name = delSpecialChars(selector.xpath('//div[@class="sku-name"]/text()')[0])

                # 商品详细配置描述
                shop_items = selector.xpath('//*[@id="detail"]/div[2]/div[1]/div[1]/ul[2]/li')
                shop_list = []
                for shop_item in shop_items:
                    shop_list.append(delSpecialChars(shop_item.xpath('./text()')[0]))
                # 商店评分
                store_score = delSpecialChars(selector.xpath('//*[@id="crumb-wrap"]/div/div[2]/div[2]/div[2]/div/div/div/div/@title')[0])

                prod_dict = {'prod_store':prod_store,'prod_price':prod_price,'prod_url':prod_url,
                             'store_url':store_url,'store_rates':store_rates,'prod_name':prod_name,
                             'shop_list':str(shop_list),'store_score':store_score,'add_time':now_time,
                             'prod_id':prod_id,'store_id':store_id}
                if(int(prod_price) < 1000):
                    continue
                product_list.append(prod_dict)
                print("产品信息：" + str(prod_dict))
            except BaseException:
                print('商品信息不符合条件')

    # 关闭driver
    driver.quit()
    return product_list


if __name__ == '__main__':
    car_names =['新大洲电动车','小牛电动车','绿源电动车','新日电动车','小刀电动车','台铃电动车','比德文电动车','立马电动车','雅迪电动车']

    # 爬取商品数据
    for car_name in car_names:
        prod_results = JDCarsInfo(car_name)
        fileUtils().saveAsCsv(prod_results,'./Data/Products/{0}'.format(car_name))

    # # 建表
    # resData = pd.read_csv('./Data/Products/新日电动车.csv',encoding='utf-8')
    # resData = resData.astype(object).where(pd.notnull(resData), None)
    # createTable(resData,'spider','pt_jd_ec_products_info')
    #
    # # 保存数据
    # file_addr = './Data/Products'
    # save_to_mysql(file_addr,'spider','pt_jd_ec_products_info')
