# Author:Aliex ZJ
#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import datetime
import re
from time import sleep

import pandas as pd

import pymysql
from lxml import etree
from pandas.errors import EmptyDataError
from selenium import webdriver
from xpinyin import Pinyin

# 今日日期
now_time = datetime.datetime.now().strftime('%Y-%m-%d')

def praseHuiLv():
    table = []
    p = Pinyin()
    login_url = 'https://finance.sina.com.cn/money/forex/hq/USDCNY.shtml'

    option = webdriver.ChromeOptions()
    # option.add_experimental_option('excludeSwitches', ['enable-automation'])
    option.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
    driver = webdriver.Chrome(executable_path='D:\Maven\YadeaSpider\RawMaterialPrice\chromedriver.exe', chrome_options=option)
    driver.get(login_url)
    xpath_date = etree.HTML(driver.page_source)
    # 瞬时时间
    huilv_shunshi = xpath_date.xpath('/html/body/div[3]/div[4]/div[2]/div[4]/div[1]/div/h5/text()')[0]
    huilvs = xpath_date.xpath('//div[@class="quote_detail_wrap"]/ul/li')
    huilv_dict = {}
    for huilv in huilvs:
        print(huilv.xpath('./label/text()')[0]+huilv.xpath('./text()')[0])
        key = 'huilv_'+p.get_pinyin(u"{0}".format(huilv.xpath('./label/text()')[0]), '')
        value = huilv.xpath('./text()')[0]
        huilv_dict['{}'.format(key)]=value
    huilv_dict['add_time'] = now_time
    huilv_dict['huilv_shunshi'] = huilv_shunshi
    table.append(huilv_dict)

    df = pd.DataFrame(table)
    df.to_csv('./Data/{0}.csv'.format('huilv'), sep=',', header=True, index=False, encoding='utf-8')
    print('{0}.csv'.format('huilv')+"保存成功")
    driver.quit()

def truncateTable(databaseName,tableName,port):
    config = dict(host='10.149.1.{0}'.format(port), user='root', password='root',
                  cursorclass=pymysql.cursors.DictCursor)
    # 建立连接
    conn = pymysql.Connect(**config)
    print(conn)
    # 自动确认commit True
    conn.autocommit(1)
    # 设置光标
    cursor = conn.cursor()
    # # 选择连接database
    conn.select_db(databaseName)
    truncate_sql = "DELETE FROM {0} WHERE add_time='{1}'".format(tableName,now_time)
    print(truncate_sql)
    cursor.execute(truncate_sql)

def insertIntoMysql(data,databaseName,tableName,port):
    config = dict(host='10.149.1.{0}'.format(port), user='root', password='root',
                  cursorclass=pymysql.cursors.DictCursor)
    # 建立连接
    conn = pymysql.Connect(**config)
    print(conn)
    # 自动确认commit True
    conn.autocommit(1)
    # 设置光标
    cursor = conn.cursor()
    # # 选择连接database
    conn.select_db(databaseName)
    # 提取数据转list 这里有与pandas时间模式无法写入因此换成str 此时mysql上格式已经设置完成
    # df['日期'] = df['日期'].astype('str')
    values = data.values.tolist()
    # 根据columns个数
    s = ','.join(['%s' for _ in range(len(data.columns))])
    # executemany批量操作 插入数据 批量操作比逐个操作速度快很多
    cursor.executemany('INSERT INTO {} VALUES ({})'.format(tableName, s), values)

def save_to_mysql(file_name,database_name,table_name,port):
    try:
        resData = pd.read_csv(file_name,encoding='utf-8')
        # 去除空值
        resData = resData.astype(object).where(pd.notnull(resData), None)
        print(resData)
        # 插入数据库
        insertIntoMysql(resData,database_name,table_name,port)
    except EmptyDataError:
        print("当前商品不符合规则")

    sleep(2)

if __name__ == '__main__':
    # 爬取汇率
    praseHuiLv()

    try:
        # 清除本日
        truncateTable('spider','huilv','154')

        # 保存数据
        file_addr = './Data/huilv.csv'
        save_to_mysql(file_addr,'spider','huilv','154')

        # 清除本日
        truncateTable('spider','huilv','127')

        # 保存数据
        file_addr = './Data/huilv.csv'
        save_to_mysql(file_addr,'spider','huilv','127')
    except BaseException:
        print("数据格式不匹配")

