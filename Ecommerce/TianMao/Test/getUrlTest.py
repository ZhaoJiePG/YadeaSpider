# Author:Aliex ZJ
# !/usr/bin/env python3
# -*- coding:utf-8 -*-
import json
import re
from time import sleep

import requests

from Utils.fileUtils import fileUtils


class TianMaoCommentCases():
    # 保存评论数据集合
    rate_list = []

    # 评论网址第一页
    url_list = 'https://rate.tmall.com/list_detail_rate.htm?' \
               'itemId=596624138584&' \
               'spuId=1243962245&' \
               'sellerId=2817130358&' \
               'order=3&' \
               'currentPage=1&'

    # 1.获取连接
    # 请求头
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "cookie": "cna=L0CwFSqRDGgCAd9EwPN4s9v5; t=3f886137b6f604509bea316d5773e8af; _tb_token_=33135eebeb15b; cookie2=1b0b4e285c2d20c244c712d49635efa6; dnk=%5Cu767D%5Cu767D%5Cu7684%5Cu72D7%5Cu5C3E%5Cu5DF4%5Cu82B1; uc1=pas=0&lng=zh_CN&cookie16=W5iHLLyFPlMGbLDwA%2BdvAGZqLg%3D%3D&cookie15=U%2BGCWk%2F75gdr5Q%3D%3D&cookie21=URm48syIYn73&existShop=false&tag=8&cookie14=UoTbnV%2BOqCmL2A%3D%3D; uc3=id2=UUpjN4zrNdJETg%3D%3D&lg2=VT5L2FSpMGV7TQ%3D%3D&vt3=F8dByuDnzROHAQ3X%2FeU%3D&nk2=05emRgpWdtZcceNuDGg%3D; tracknick=%5Cu767D%5Cu767D%5Cu7684%5Cu72D7%5Cu5C3E%5Cu5DF4%5Cu82B1; lid=%E7%99%BD%E7%99%BD%E7%9A%84%E7%8B%97%E5%B0%BE%E5%B7%B4%E8%8A%B1; uc4=nk4=0%400SwjusWimre0H6WrAcFT6cSTu0IPkewtmQ%3D%3D&id4=0%40U2gp9xkNePhwkA3mujHlbSd34BVR; _l_g_=Ug%3D%3D; unb=2221579274; lgc=%5Cu767D%5Cu767D%5Cu7684%5Cu72D7%5Cu5C3E%5Cu5DF4%5Cu82B1; cookie1=VWsu%2BpKF9hE9HePBZc%2FExBxRmsDaR97K6DS4nKh4iu0%3D; login=true; cookie17=UUpjN4zrNdJETg%3D%3D; _nk_=%5Cu767D%5Cu767D%5Cu7684%5Cu72D7%5Cu5C3E%5Cu5DF4%5Cu82B1; sg=%E8%8A%B145; csg=029a3cd0; enc=x%2BbRQuO%2FU%2FgQU1XAlsZpeiOZ1IHkZYtObQTBaOQawfBHOzzdocAvLvbm28eF8EIDr9V4tZaW0jnMGkmhRNm10g%3D%3D; otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; whl=-1%260%260%260; x=__ll%3D-1%26_ato%3D0; l=cBSH0T-4q4bTAKD8BOCgCZMInnbO9LAfguWXRJ8ei_5ZZsTVpQbOkiBbsU96cjWFTw8B4nnADjetjecb-yWfoTB7K9cdvdC..; isg=BHV1MEyeRJRSkKAV4I7I9ewrkfElZ3NQbmaCt_eaDOx4zpTAv0Nq1eSIGNLdjkG8",
        "referer": "https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.11.7b287e09a2f8pU&id=596624138584&skuId=4315669582772&areaId=320200&user_id=2817130358&cat_id=2&is_b=1&rn=8630e2eec4c15b75a52ce788af26c28b",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3732.400 QQBrowser/10.5.3819.400"}

    # 响应
    response = requests.get(url_list, headers=headers)
    data = response.text
    comment_datas = re.findall('{.*}', data)[0]
    print(comment_datas)

    # 2.获取总页数和需要分页的个数
    comment_count = json.loads(comment_datas)['rateDetail']['rateCount']['total']
    print(comment_count)
    comment_pages = int(int(comment_count)/20)+2
    print(comment_pages)

    # 3.循环获取评论
    for comment_page in range(1,comment_pages):
        print('====睡眠5s，开始爬取第'+str(comment_page)+'页评论====')
        sleep(5)
        # 分页请求网址
        comment_url= 'https://rate.tmall.com/list_detail_rate.htm?' \
                    'itemId=596624138584&' \
                    'spuId=1243962245&' \
                    'sellerId=2817130358&' \
                    'order=3&' \
                    'currentPage={0}&'.format(comment_page)
        # 评论数据
        comment_data = re.findall('{.*}', requests.get(comment_url, headers=headers).text)[0]
        print(comment_data)
        try:
            comment_json = json.loads(comment_data)['rateDetail']['rateList']
            for rate in comment_json:
                rateDate = rate['rateDate']
                rateContent = rate['rateContent']
                auctionSku = rate['auctionSku']
                cmsSource = rate['cmsSource']
                rate_list.append({'rateDate':rateDate,'rateContent':rateContent,'auctionSku':auctionSku,'cmsSource':cmsSource})
                print(rateContent)
        except Exception:
            print("Error: 没有找到网页内容")
        finally:
            print("继续执行")

        print('===========================================')
    print(rate_list)
    fileUtils().saveAsCsv(rate_list,'../Data/天猫Comment测试')
if __name__ == '__main__':

    tmc = TianMaoCommentCases()