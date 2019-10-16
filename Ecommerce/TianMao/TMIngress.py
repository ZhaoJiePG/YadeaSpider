# Author:Aliex ZJ
#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import datetime
import json
import random
import re
from time import sleep

import requests
from lxml import etree

from Utils.fileUtils import fileUtils

now_time = datetime.datetime.now().strftime('%Y-%m-%d')

# 获取商品评论
def TianMaoCommentCases(index,url_list):
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
    selector = etree.HTML(shop_response)
    shop_items = selector.xpath('//*[@id="J_AttrUL"]/li')
    shop_list = []
    for shop_item in shop_items:
        shop_list.append(shop_item.xpath('./text()')[0].replace('\xa0',''))
    print("产品信息："+str(shop_list))
    print("睡眠15s，开始获取评论信息")
    sleep(15)

    # 获取商品评论
    response = requests.get(rate_url, headers=headers1)
    data = response.text
    comment_datas = re.findall('{.*}', data)[0]
    print(comment_datas)

    # 2.获取总页数和需要分页的个数
    comment_count = json.loads(comment_datas)['rateDetail']['rateCount']['total']
    comment_pages = int(int(comment_count)/20)+2
    print("总评论数："+str(comment_count)+"===总页数："+str(comment_pages)+"===等待5s")
    sleep(3)

    # 3.循环获取评论
    for comment_page in range(1,comment_pages):
        # 随机等待时间
        sleep_list = [10,11,12,13,14,15,16,17,18,19,20]
        sleep_time = random.choice(sleep_list)
        print('====睡眠'+str(sleep_time)+'s，总共'+str(comment_pages)+'页,开始爬取第'+str(comment_page)+'页评论====')
        sleep(sleep_time)
        # 分页请求网址
        comment_url= rate_url.replace('currentPage=1','currentPage={0}').format(comment_page)
        #获取随机cookie
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
                if(rateContent !='此用户没有填写评论!'):
                    rate_list.append({'rateDate':rateDate,'rateContent':rateContent,'auctionSku':auctionSku,
                                      'cmsSource':cmsSource,'shop_list':str(shop_list),
                                      'topic':topic,'store_name':store_name,'shop_title':shop_title,'add_date':now_time})
                    print(rateContent)
        except Exception:
            print("Error: 没有找到网页内容")
        finally:
            print("继续执行")

        print('===========================================')
    # print(rate_list)
    # 保存数据到文件
    fileUtils().saveAsCsv(rate_list,'./Data/Rates/{0}'.format(str(int(index)+1)+shop_title))



if __name__ == '__main__':


    # 获取商品url和评论的url
    url_lists = fileUtils().getCsvFile('./Data/store_url.csv')

    # 爬取商品评论
    for index in range(0,1):
        url_list = url_lists[index]
        print(url_list)
        # 获取天猫评论
        TianMaoCommentCases(index,url_list)

    # 保存数据到文件
    # print(rate_list)
