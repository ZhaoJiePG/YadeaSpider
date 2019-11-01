# Author:Aliex ZJ
# !/usr/bin/env python3
# -*- coding:utf-8 -*-
import random
import time

import requests



# 获取随机请求头
def getRandomAgent():
    user_agent_list = [
        {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3732.400 QQBrowser/10.5.3819.400"},
        {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0"},
        {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"},
        {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0X-Requested-With:XMLHttpRequest"}]
    # 每次请求的浏览器不一样
    random_user_agent = random.choice(seq=user_agent_list)

    return random_user_agent

# 获取请求信息
def getUrl(self,url):
    # 获取随机请求头
    headers = self.getRandomAgent()

    # getip = get_IP()
    #
    # random_ip = getip.get_random_ip
    # # 获取随机代理ip
    # proxies = {"http": random_ip}
    # print(proxies)

    response = requests.get(url, headers=headers)
    data = response.text
    time.sleep(0.1)
    response.close()
    return data

# 获取ajax接口数据
def getAjaxDatas(self,url,province):
    # 获取随机请求头
    headers1 = self.getRandomAgent()
    headers2 = {
        'Host': 'www.xinri.com',
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Length': '274',
        'Connection': 'keep-alive',
        'Referer': 'http://www.xinri.com/service/internet.html'
    }
    headers = dict(**headers1,**headers2)
    # 请求的参数
    data = {'cmd':'getDotList',
            'p':province,
            'c':'e1ILU/Pqwxzqf/C1SOIm1PrnrVkSP+jDXIz5QJGS81BTzOJvsPt73w==',
            'd':'e1ILU/Pqwxzqf/C1SOIm1PrnrVkSP+jDXIz5QJGS81BTzOJvsPt73w==',
            't':'e1ILU/Pqwxzqf/C1SOIm1PrnrVkSP+jDXIz5QJGS81BTzOJvsPt73w=='}

    response = requests.post(url,headers=headers,data=data)
    response.encoding = 'utf-8'
    data = response.text

    # return stringUtils().unicode2str(data)


# print(requestsUtils().getAjaxDatas('http://www.xinri.com/Ajax/AjaxHandler_XRDDC.ashx'))



