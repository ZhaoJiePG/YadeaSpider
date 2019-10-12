# Author:Aliex ZJ
# !/usr/bin/env python3
# -*- coding:utf-8 -*-
import json
import re
from time import sleep

import requests

from Utils.fileUtils import fileUtils


class JingDongCommentCases():
    # 保存评论数据集合
    rate_list = []

    # 评论网址第一页
    url_list = 'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv1342&productId=49927298513&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1'

    # 1.获取连接
    # 请求头
    headers = {
        "referer": "https://item.jd.com/49927298513.html",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3732.400 QQBrowser/10.5.3819.400"}

    # 响应
    response = requests.get(url_list, headers=headers)
    data = response.text
    comment_datas = re.findall('{.*}', data)[0]
    print(comment_datas)
    #
    # # 2.获取总页数和需要分页的个数
    # comment_count = json.loads(comment_datas)['rateDetail']['rateCount']['total']
    # print(comment_count)
    # comment_pages = int(int(comment_count)/20)+2
    # print(comment_pages)

    # 3.循环获取评论
    # for comment_page in range(1,comment_pages):
    #     print('====睡眠5s，开始爬取第'+str(comment_page)+'页评论====')
    #     sleep(5)
    #     # 分页请求网址
    #     comment_url= 'https://rate.tmall.com/list_detail_rate.htm?' \
    #                 'itemId=596624138584&' \
    #                 'spuId=1243962245&' \
    #                 'sellerId=2817130358&' \
    #                 'order=3&' \
    #                 'currentPage={0}&'.format(comment_page)
    #     # 评论数据
    #     comment_data = re.findall('{.*}', requests.get(comment_url, headers=headers).text)[0]
    #     print(comment_data)
    #     try:
    #         comment_json = json.loads(comment_data)['rateDetail']['rateList']
    #         for rate in comment_json:
    #             rateDate = rate['rateDate']
    #             rateContent = rate['rateContent']
    #             auctionSku = rate['auctionSku']
    #             cmsSource = rate['cmsSource']
    #             rate_list.append({'rateDate':rateDate,'rateContent':rateContent,'auctionSku':auctionSku,'cmsSource':cmsSource})
    #             print(rateContent)
    #     except Exception:
    #         print("Error: 没有找到网页内容")
    #     finally:
    #         print("继续执行")
    #
    #     print('===========================================')
    print(rate_list)
    # fileUtils().saveAsCsv(rate_list,'../Data/天猫Comment测试')
if __name__ == '__main__':

    tmc = JingDongCommentCases()