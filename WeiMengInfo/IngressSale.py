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
    time.sleep(20)
    client_id = 'EDD3EAB6F807344E8AB5AE583A3E073C'
    client_secret = '9B659BC31EF571D38DFA73DDAA61CC1B'
    week_day = datetime.datetime.now().weekday()
    # 新建微盟实例
    wm = WeiMengInterface(client_id, client_secret)
    # MySql客户端
    mc154 = MySqlClient(154, 'spider')

    # 获取订单列表
    print("获取获取订单列表情接口")
    access_token = wm.get_access_token()
    wm.get_order_list(access_token)
    mc154.get_create_sql('./Data/order_list.csv','weimeng_sale_order_list')
    mc154.insert_into_mysql_file_data('./Data/order_list.csv', 'weimeng_sale_order_list', now_time)

    # 获取商户优惠券列表
    print("获取商户优惠券列表")
    access_token = wm.get_access_token()
    wm.get_merchant_coupon_list(access_token)
    mc154.get_create_sql('./Data/merchant_coupon_list.csv','weimeng_merchant_coupon_list')
    mc154.insert_into_mysql_file_data('./Data/merchant_coupon_list.csv', 'weimeng_merchant_coupon_list', now_time)

    # 获取订单详情
    print("获取订单详情接口")
    access_token = wm.get_access_token()
    wm.get_order_detail(access_token)
    mc154.get_create_sql('./Data/order_detail.csv','weimeng_sale_order_detail')
    mc154.insert_into_mysql_file_data('./Data/order_detail.csv', 'weimeng_sale_order_detail', now_time)

    # 获取售后订单列表
    print("获取售后订单列表")
    access_token = wm.get_access_token()
    wm.get_rights_order_list(access_token)
    mc154.get_create_sql('./Data/rights_order_list.csv','weimeng_rights_order_list')
    mc154.insert_into_mysql_file_data('./Data/rights_order_list.csv', 'weimeng_rights_order_list', now_time)

    # 获取售后订单详情
    print("获取售后订单详情")
    access_token = wm.get_access_token()
    wm.get_rights_order_detail(access_token)
    mc154.get_create_sql('./Data/rights_order_detail.csv','weimeng_rights_order_detail')
    mc154.insert_into_mysql_file_data('./Data/rights_order_detail.csv', 'weimeng_rights_order_detail', now_time)

    # 获取进销存单据列表（出入库）
    print("获取进销存单据列表（出入库）")
    access_token = wm.get_access_token()
    wm.get_inventory_order_list(access_token)
    mc154.get_create_sql('./Data/inventory_order_list.csv','weimeng_inventory_order_list')
    mc154.insert_into_mysql_file_data('./Data/inventory_order_list.csv', 'weimeng_inventory_order_list', now_time)

    # 用户优惠券
    access_token = wm.get_access_token()
    wm.get_coupon_page_by_wid(access_token)

    # 关闭driver客户端
    for i in range(0,10):
        time.sleep(0.2)
        access_token = wm.get_access_token()
    mc154.conn.close()