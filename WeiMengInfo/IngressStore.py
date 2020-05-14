# Author:Aliex ZJ
#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import datetime
import time

import pandas
import requests
import sys
sys.path.append('../')  # 新加入的
print(sys.path)

from WeiMengInfo.MySqlClient import MySqlClient

now_time = datetime.datetime.now().strftime('%Y-%m-%d')
from WeiMengInfo.WeiMengInterface import WeiMengInterface

if __name__ == '__main__':
    client_id = 'EDD3EAB6F807344E8AB5AE583A3E073C'
    client_secret = '9B659BC31EF571D38DFA73DDAA61CC1B'
    week_day = datetime.datetime.now().weekday()
    # 新建微盟实例
    wm = WeiMengInterface(client_id, client_secret)
    # MySql客户端
    mc154 = MySqlClient(154, 'spider')

    # # 获取门店列表
    print("获取门店列表接口")
    access_token = wm.get_access_token()
    wm.get_store_list(access_token)
    mc154.get_create_sql('./Data/store_list.csv','weimeng_store_list')
    mc154.insert_into_mysql_file_data('./Data/store_list.csv', 'weimeng_store_list', now_time)

    # 获取门店详情
    print("获取门店详情接口")
    access_token = wm.get_access_token()
    wm.get_store_detail(access_token)
    mc154.get_create_sql('./Data/store_detail.csv','weimeng_store_detail')
    mc154.insert_into_mysql_file_data('./Data/store_detail.csv', 'weimeng_store_detail', now_time)

    # 获取查询导购列表
    print("获取查询导购列表")
    access_token = wm.get_access_token()
    wm.get_store_guider_list(access_token)
    mc154.get_create_sql('./Data/store_guider_list.csv','weimeng_store_guider_list')
    mc154.insert_into_mysql_file_data('./Data/store_guider_list.csv', 'weimeng_store_guider_list', now_time)

    # 获取导购目标列表
    print("获取导购目标列表")
    access_token = wm.get_access_token()
    wm.get_store_guider_target_list(access_token)
    mc154.get_create_sql('./Data/store_guider_target_list.csv','weimeng_store_guider_target_list')
    mc154.insert_into_mysql_file_data('./Data/store_guider_target_list.csv', 'weimeng_store_guider_target_list', now_time)

    # 获取门店库存列表
    print("获取门店库存列表")
    access_token = wm.get_access_token()
    wm.get_store_stock_list(access_token)
    mc154.get_create_sql('./Data/store_stock_list.csv','weimeng_store_stock_list')
    mc154.insert_into_mysql_file_data('./Data/store_stock_list.csv', 'weimeng_store_stock_list', now_time)

    # 获取产品列表
    print("获取产品列表")
    access_token = wm.get_access_token()
    wm.get_goods_list(access_token)
    mc154.get_create_sql('./Data/goods_list.csv','weimeng_goods_list')
    mc154.insert_into_mysql_file_data('./Data/goods_list.csv', 'weimeng_goods_list', now_time)

    # 获取产品明细
    print("获取产品明细")
    access_token = wm.get_access_token()
    wm.get_goods_detail(access_token)
    mc154.get_create_sql('./Data/goods_detail.csv','weimeng_goods_detail')
    mc154.insert_into_mysql_file_data('./Data/goods_detail.csv', 'weimeng_goods_detail', now_time)

    # 关闭driver客户端
    for i in range(0,10):
        time.sleep(0.2)
        access_token = wm.get_access_token()
    mc154.conn.close()

