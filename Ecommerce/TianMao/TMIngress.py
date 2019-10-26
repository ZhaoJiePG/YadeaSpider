# Author:Aliex ZJ
# !/usr/bin/env python3
# -*- coding:utf-8 -*-
import datetime
import json
import os
import random
import re
import pandas as pd
from time import sleep

import requests
from lxml import etree
from pandas.errors import EmptyDataError

from Utils.fileUtils import fileUtils
from Utils.mysqlUtils import insertIntoMysql, truncateTable

now_time = datetime.datetime.now().strftime('%Y-%m-%d')


# 获取商品评论和明细
def TianMaoCommentCases(index, url_list):
    # 保存评论数据集合
    rate_list = []

    # 评论网址第一页
    rate_url = url_list[4]
    # print(rate_url)
    refer_url = url_list[3]
    # print(refer_url)
    topic = url_list[0]
    store_name = url_list[1]
    shop_title = url_list[2]

    # 获取随机cookie
    cookie_list = fileUtils().getCsvFile('../Data/Cookie.csv')
    cookie = random.choice(cookie_list)[0]
    # 获取随机浏览器信息
    ua_list = fileUtils().getCsvFile('../Data/UserAgent.csv')
    ua = random.choice(ua_list)[0]

    # 1.获取连接
    # 请求头
    headers1 = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "cookie": "{0}".format(cookie),
        "referer": "{0}".format(refer_url),
        "user-agent": "{0}".format(ua)}

    # 获取商品信息
    shop_response = requests.get(refer_url).text
    # 商品价格
    reserve_Price = re.findall('"reservePrice":"(\d*\.\d*)"', str(shop_response))[0]
    # defaultitem_Price = re.findall('"defaultItemPrice":"(\d*\.\d*)"', str(shop_response))[0]
    selector = etree.HTML(shop_response)
    shop_items = selector.xpath('//*[@id="J_AttrUL"]/li')
    # 详细信息
    shop_list = []
    for shop_item in shop_items:
        shop_list.append(shop_item.xpath('./text()')[0].replace('\xa0', ''))
    print("产品信息：" + str(shop_list))
    print("睡眠15s，开始获取评论信息")
    sleep(15)

    # 获取商品评论
    response = requests.get(rate_url, headers=headers1)
    data = response.text
    comment_datas = re.findall('{.*}', data)[0]
    print(comment_datas)

    # 2.获取总页数和需要分页的个数
    comment_count = json.loads(comment_datas)['rateDetail']['rateCount']['total']
    comment_pages = int(int(comment_count) / 20) + 2
    print("总评论数：" + str(comment_count) + "===总页数：" + str(comment_pages) + "===等待5s")
    sleep(12)

    # 获取平均评价评分
    avgrate_url = rate_url.replace('rate.tmall.com','dsr-rate.tmall.com')\
        .replace('list_detail_rate.htm','list_dsr_info.htm')\
        .replace('&order=3&currentPage=1','')
    avg_response = requests.get(avgrate_url, headers=headers1).text
    avg_rate = json.loads(re.findall('{.*}', avg_response)[0])['dsr']['gradeAvg']
    print("该商品平均评分:"+str(avg_rate)+"分,等待15s")
    sleep(12)

    # 3.循环获取评论
    for comment_page in range(1, comment_pages):
        # 随机等待时间
        sleep_list = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
        sleep_time = random.choice(sleep_list)
        print('====睡眠' + str(sleep_time) + 's，总共' + str(comment_pages) + '页,开始爬取第' + str(comment_page) + '页评论====')
        sleep(sleep_time)
        # 分页请求网址
        comment_url = rate_url.replace('currentPage=1', 'currentPage={0}').format(comment_page)
        # 获取随机cookie
        cookie_list = fileUtils().getCsvFile('../Data/Cookie.csv')
        cookie = random.choice(cookie_list)[0]
        # 获取随机浏览器信息
        ua_list = fileUtils().getCsvFile('../Data/UserAgent.csv')
        ua = random.choice(ua_list)[0]
        # 请求头
        headers2 = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9",
            "cookie": "{0}".format(cookie),
            "referer": "{0}".format(refer_url),
            "user-agent": "{0}".format(ua)}
        print(headers2)

        # 评论数据
        comment_data = re.findall('{.*}', requests.get(comment_url, headers=headers2).text)[0]
        print(comment_data)
        try:
            comment_json = json.loads(comment_data)['rateDetail']['rateList']
            for rate in comment_json:
                rateDate = rate['rateDate']
                rateContent = rate['rateContent']
                auctionSku = rate['auctionSku']
                cmsSource = rate['cmsSource']
                if (rateContent != '此用户没有填写评论!'):
                    rate_list.append({'rate_date': rateDate, 'rate_content': rateContent, 'auction_sku': auctionSku,
                                      'cms_source': cmsSource, 'shop_list': str(shop_list),'reserve_rice':reserve_Price,
                                      'avg_rate':avg_rate,
                                      'topic': topic, 'store_name': store_name, 'shop_title': shop_title,
                                      'add_date': now_time})
                    print(rateContent)
        except Exception:
            print("Error: 没有找到网页内容")
        finally:
            print("继续执行")

        print('===========================================')
    # print(rate_list)
    # 保存数据到文件
    fileUtils().saveAsCsv(rate_list, './Data/Rates/{0}'.format(str(int(index) + 1)))
    sleep(10)

# 保存到数据库
def save_to_mysql(file_addr):
    # 清空数据
    truncateTable('spider','rates_tianmao')
    for dirs in os.walk(file_addr):
        fileList = dirs[2]
        for fileName in fileList:
            # 读取每个文件
            csvFile=file_addr+'/{0}'.format(fileName)
            print('开始存储'+str(csvFile)+'数据到mysql')
            try:
                resData = pd.read_csv(csvFile,encoding='utf-8')
                # 去除空值
                resData = resData.astype(object).where(pd.notnull(resData), None)
                # 插入数据库
                insertIntoMysql(resData,'spider','rates_tianmao')
            except EmptyDataError:
                print("当前商品无评论")

            sleep(2)

if __name__ == '__main__':

    # 获取商品url和评论的url
    url_lists = fileUtils().getCsvFile('./Data/store_url.csv')

    # 爬取商品评论
    # for index in range(143, 169):
    #
    #     url_list = url_lists[index]
    #     print(url_list)
    #     # 获取天猫评论
    #     TianMaoCommentCases(index, url_list)

    file_addr = './Data/Rates'
    save_to_mysql(file_addr)

