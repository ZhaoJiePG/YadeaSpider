# Author:Aliex ZJ
# !/usr/bin/env python3
# -*- coding:utf-8 -*-
import random
import time

import requests

from Yadea.CompetitiveBrandStoreArea.utils.stringUtils import stringUtils


class requestsUtils():

    # 获取随机请求头
    def getRandomAgent(self):
        user_agent_list = [{
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1"},
            {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0"},
            {
                'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"},
            {'User-Agent': "Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50"},
            {
                'User-Agent': "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.41 Safari/535.1 QQBrowser/6.9.11079.201"}]
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

        return stringUtils().unicode2str(data)


# print(requestsUtils().getAjaxDatas('http://www.xinri.com/Ajax/AjaxHandler_XRDDC.ashx'))



