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

    print(rate_list)

if __name__ == '__main__':

    tmc = JingDongCommentCases()