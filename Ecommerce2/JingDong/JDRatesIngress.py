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
from Utils.mysqlUtils import insertIntoMysql, truncateTable, save_to_mysql, createTable

# 爬取天猫评论信息，访问ratelist接口
from Utils.stringUtils import delSpecialChars

now_time = datetime.datetime.now().strftime('%Y-%m-%d')

# 获取商品评论和明细
def JinDongCommentCases(url_list):
    prod_url = url_list[2]
    prod_topic = url_list[1]
    prod_id = re.findall('(\d+)',prod_url)[0]
    print("开始获取商品  "+prod_topic+':'+str(prod_id)+'评论信息')

    # 保存评论数据集合
    rates_list = []

    # 评论网址第一页
    rate_urls = [
        # 默认评论接口
        'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv44&productId={0}&score=0&sortType=6&page={1}&pageSize=10&isShadowSku=0&fold=1',
        # 参考价值不大接口
        'https://club.jd.com/comment/getProductPageFoldComments.action?callback=jQuery1719501&productId={0}&score=4&sortType=5&page={1}&pageSize=5&_=1573096406813']

    # 1.获取连接
    # 请求头
    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        "cookie":'__jdu=1150543271; shshshfpa=0cb162de-cb82-21b8-49a7-7e1fd26a3efd-1570864191; user-key=d5809892-c823-402e-9748-c84b2469d56f; cn=0; shshshfpb=eTsoprn6f4hkN00S8LggPuQ%3D%3D; unpl=V2_ZzNtbRYAS0Z8WkQAehlVB2JQRl0SUUcVd1oTAC8YVFIyV0BYclRCFX0URlVnG10UZwYZWEtcRx1FCEdkeBBVAWMDE1VGZxBFLV0CFSNGF1wjU00zQwBBQHcJFF0uSgwDYgcaDhFTQEJ2XBVQL0oMDDdRFAhyZ0AVRQhHZHsZWARjBhBeRFdzJXI4dmR%2bG1gDbwIiXHJWc1chVEVSexlcDSoDEllDU0YXdg5GZHopXw%3d%3d; __jdv=76161171|baidu-pinzhuan|t_288551095_baidupinzhuan|cpc|0f3d30c8dba7459bb52f2eb5eba8ac7d_0_ef9b8c3e01834be1a7513cdee09fdec4|1572418139698; shshshfp=4ecb84897eabb0f7a4c6348b7cdc7d0a; __jda=122270672.1150543271.1570864187.1572825530.1573090824.9; __jdc=122270672; areaId=12; ipLoc-djd=12-984-3384-0; wlfstk_smdl=gcda47s1yytkclehvxho46m7ddz5g7ow; TrackID=1KNUUCIn3e7IMNektPzhbcu7wSO0kDr7PEe_KWvFCOXkJh4Zo6p9lf8KOj5iwp4Yidll4C9iAu7fQF6LVOjeB1LGNsaTdxOTqpshIt79InXGwUBG-R8JW8h4lpF-aMXFlBoc7nuE4YFFi_IXSENLUoA; thor=F5548B286F0AC84835F479E2098B937588592D856D78425D7FC38CD7238081AFCBA255023DFA3D8E13AF80EB0481FBDF4DA6C1A35102B43FEA63A3914094409E2250E5F462224217F1004694F9EC7CF2DA417BF181A528377DE99BED15AD4C25157B03BD7C98D6058B3B22E3F300B51E9F9A64987B3D551B14DCFF630D20CCBF954CBC1087415F2C2203531C10B881874F74CD45F930D0F4802E5F203320EEDE; pinId=eqbOg6AqvNqT4t6ZRIp7VrV9-x-f3wj7; pin=jd_5580681fb886d; unick=jd_181685ayj; ceshi3.com=103; _tp=OQVsjG6Pu5TIXKleFObW0uc7fxOqC8rImaa7i%2FLjfqM%3D; _pst=jd_5580681fb886d; shshshsID=d4ef035cd6502b3e3bbb5e5859bb09c1_2_1573090894262; __jdb=122270672.4.1150543271|9.1573090824; 3AB9D23F7A4B3C9B=4WQN5JCPKTD4EYGF7GGHYDUIBN64EH5SZHPCNA56CB2G7HP52UGN73YBUMQ2EOMZI4WXVSWB3CSTQT2KOLQIVGGV5A; JSESSIONID=99B9C173D8D05BABCE00F2429A497E26.s1',
        "referer": "{0}".format(prod_url),
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3732.400 QQBrowser/10.5.3819.400"}
    response = requests.get(rate_urls[1].format(prod_id,0), headers=headers)
    rates_jsons = json.loads(re.findall('{.*}', response.text)[0])
    sleep(3)
    # 获取总页数
    pages = rates_jsons['productCommentSummary']['commentCount']
    print("===============================")
    for rate_url in rate_urls:
        for page in range(0,int(pages/10+1)):
            print("总共"+str(pages)+"条评论，正在获取第"+str(page)+"页")
            sleep(3)
            try:
                rates_responses = requests.get(rate_url.format(prod_id,page), headers=headers)
                rates = json.loads(re.findall('{.*}', rates_responses.text)[0])
            except BaseException:
                print("无数据")
                break

            rates_lists = rates['comments']
            for rate_list in rates_lists:
                rate = delSpecialChars(rate_list['content'])
                prod_color = rate_list['productColor']
                prod_name = rate_list['referenceName']
                rate_score = rate_list['score']
                rate_dict = {'add_time':now_time,'prod_name':prod_name,'rate_score':rate_score,'rate':rate,
                             'prod_color':prod_color,'prod_url':prod_url,'prod_topic':prod_topic,'prod_id':prod_id,
                             'sale_num':str(pages)}
                print(rate_dict)
                rates_list.append(rate_dict)
            if(rates_lists==[]):
                break

    # 保存数据到文件
    fileUtils().saveAsCsv(rates_list, './Data/Rates/{0}'.format(str(prod_id)))


if __name__ == '__main__':

    # 获取商品url和评论的url
    url_lists = fileUtils().getCsvFile('./Data/store_url.csv')
    for index in range(0,74):
        url_list = url_lists[index]
        JinDongCommentCases(url_list)

    # 建表
    resData = pd.read_csv('./Data/Rates/58629154676.csv',encoding='utf-8')
    resData = resData.astype(object).where(pd.notnull(resData), None)
    createTable(resData,'spider','pt_jd_ec_rates_info',154)

    # 保存数据
    file_addr = './Data/Rates'
    save_to_mysql(file_addr,'spider','pt_jd_ec_rates_info',154)