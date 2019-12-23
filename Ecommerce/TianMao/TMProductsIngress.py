# Author:Aliex ZJ
#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import datetime
import re
import pandas as pd
from time import sleep

import requests
from lxml import etree
from selenium import webdriver
from bs4 import BeautifulSoup
from Utils.fileUtils import fileUtils
from Utils.mysqlUtils import save_to_mysql, createTable
from Utils.stringUtils import delSpecialChars

# 爬取搜索商品数据，selinum+requests

now_time = datetime.datetime.now().strftime('%Y-%m-%d')

def TMCarsInfo(car_name):
    #产品信息集合
    product_list=[]
    # selenium 参数
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    option.add_argument('incognito')
    driver = webdriver.Chrome(
        executable_path='D:\Maven\YadeaSpider\chromedriver.exe',
        chrome_options=option)
    # 请求的url
    url = 'https://list.tmall.com/search_product.htm?q={0}'.format(car_name)
    # 请求连接
    driver.get(url)
    sleep(2)
    html_doc = driver.page_source
    # 主动设置 bs4的解析库,BeautifulSoup对象
    soup = BeautifulSoup(html_doc,'lxml').prettify()
    # 获取页码
    pages = re.findall('共(\d+)页',soup)[0]
    print('*****开始爬取'+car_name+'：总共'+pages+'页*****')
    # 循环解析查询页数
    for page in range(1,int(pages)+1):
        url = 'https://list.tmall.com/search_product.htm?q={0}&totalPage={1}&jumpto={2}'.format(car_name,pages,page)
        print('睡眠5s...开始爬取第'+str(page)+'页========url为'+url)
        driver.get(url)
        sleep(5)
        # 调用xpath解析库
        xpath_date = etree.HTML(BeautifulSoup(driver.page_source,'lxml').prettify())
        products=xpath_date.xpath('//*[@id="J_ItemList"]/div')
        # 获取产品信息
        for product in products:
            prod_url = 'https:'+product.xpath('./div/div[1]/a/@href')[0]
            prod_id = re.findall('\?id=(\d+)',prod_url)[0]
            prod_price = product.xpath('./div/p[1]/em/@title')[0]
            prod_price = prod_price[:-((prod_price.index('.'))-1)]
            prod_title = product.xpath('./div/p[2]/a/@title')[0]
            prod_store = product.xpath('./div/p[3]/span[3]/@data-nick')[0]
            prod_msale = delSpecialChars(product.xpath('./div/p[3]/span[1]/text()')[0])+delSpecialChars(product.xpath('./div/p[3]/span[1]/em/text()')[0])
            prod_rates = delSpecialChars(product.xpath('./div/p[3]/span[2]/text()')[0])+delSpecialChars(product.xpath('./div/p[3]/span[2]/a/text()')[0])
            store_url = 'https:'+product.xpath('./div/div[2]/a/@href')[0]
            store_id = re.findall('\?user_number_id=(\d+)',store_url)[0]

            # 跳转商品url，获取详细信息
            driver.get(prod_url)
            sleep(1)
            prod_reponse = BeautifulSoup(driver.page_source,'lxml').prettify()
            selector = etree.HTML(prod_reponse)
            shop_items = selector.xpath('//*[@id="J_AttrUL"]/li')
            # 商品详细配置描述
            shop_list = []
            for shop_item in shop_items:
                shop_list.append(delSpecialChars(shop_item.xpath('./text()')[0]))
            # 店铺评分
            score_list = []
            scores = selector.xpath('//*[@id="shop-info"]/div[2]/div')
            for score in scores:
                res_score = delSpecialChars(score.xpath('./div[1]/text()')[0])+delSpecialChars(score.xpath('./div[2]/span/text()')[0])
                score_list.append(res_score)
            # 收藏人气
            popularity = '/html/body/div[5]/div/div[2]/div/div[1]/div[2]/p/span[2]'
            # 保存明细
            prod_dict = {'car_name':car_name,'add_time':now_time,'prod_url':prod_url,'prod_title':prod_title,'store_url':store_url,
                         'prod_price':prod_price,'prod_store':prod_store,'prod_msale':prod_msale,'prod_rates':prod_rates,
                         'prod_id':prod_id,'store_id':store_id,'shop_list':str(shop_list),'score_list':str(score_list)}
            try:
                if(int(prod_price) >= 1000):
                    product_list.append(prod_dict)
            except ValueError:
                print('不符合条件的商品')
            print("产品信息：" + str(prod_dict))

    # 关闭driver
    driver.quit()
    return product_list

if __name__ == '__main__':
    car_names =['雅迪电动车','新日电动车','小牛电动车','绿源电动车','小刀电动车','台铃电动车',
                '比德文电动车','立马电动车','新大洲电动车','杰宝大王电动车']
    car_names =['电动车']
    # 爬取商品数据
    for car_name in car_names:
        prod_results = TMCarsInfo(car_name)
        fileUtils().saveAsCsv(prod_results,'./Data/Products/{0}'.format(car_name))

    # # 建表
    # resData = pd.read_csv('./Data/Products/台铃电动车.csv',encoding='utf-8')
    # resData = resData.astype(object).where(pd.notnull(resData), None)
    # createTable(resData,'spider','pt_tm_ec_products_info',154)
    #
    # # 保存数据
    # file_addr = './Data/Products'
    # save_to_mysql(file_addr,'spider','pt_tm_ec_products_info',154)