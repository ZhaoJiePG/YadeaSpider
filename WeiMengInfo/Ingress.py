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
    #
    # # # 增量获取会员列表列(循环获取，每次500次请求，每个请求500条数据)
    # print("********获取会员列表列********")
    # while True:
    #     try:
    #         # 刷新access_token(2小时一次)
    #         print("\n********刷新access_token(2小时一次)********")
    #         access_token = wm.get_access_token()
    #         print(access_token)
    #         wm.get_member_list(access_token=access_token)
    #     except requests.exceptions.ConnectionError:
    #         print("请求次数过多，重新获取")
    #         continue
    #     except TypeError:
    #         print("数据请求结束，退出循环")
    #         break
    # # 增量保存会员列表信息
    # # mc154.create_table(pandas.read_csv('./Data/member_list.csv', low_memory=False), 'weimeng_user_member_list')
    # mc154.truncate_day_data('weimeng_user_member_list',now_time)
    # mc154.insert_into_mysql_file_data('./Data/member_list.csv','weimeng_user_member_list',now_time)
    #
    # # 获取订单列表
    # print("获取获取订单列表情接口")
    # access_token = wm.get_access_token()
    # wm.get_order_list(access_token)
    # mc154.get_create_sql('./Data/order_list.csv','weimeng_sale_order_list')
    # mc154.insert_into_mysql_file_data('./Data/order_list.csv', 'weimeng_sale_order_list', now_time)
    #
    # # # 获取门店列表
    # print("获取门店列表接口")
    # access_token = wm.get_access_token()
    # wm.get_store_list(access_token)
    # mc154.get_create_sql('./Data/store_list.csv','weimeng_store_list')
    # mc154.insert_into_mysql_file_data('./Data/store_list.csv', 'weimeng_store_list', now_time)
    #
    # # 获取门店详情
    # print("获取门店详情接口")
    # access_token = wm.get_access_token()
    # wm.get_store_detail(access_token)
    # mc154.get_create_sql('./Data/store_detail.csv','weimeng_store_detail')
    # mc154.insert_into_mysql_file_data('./Data/store_detail.csv', 'weimeng_store_detail', now_time)
    #
    # # 获取查询导购列表
    # print("获取查询导购列表")
    # access_token = wm.get_access_token()
    # wm.get_store_guider_list(access_token)
    # mc154.get_create_sql('./Data/store_guider_list.csv','weimeng_store_guider_list')
    # mc154.insert_into_mysql_file_data('./Data/store_guider_list.csv', 'weimeng_store_guider_list', now_time)
    #
    # # 获取导购目标列表
    # print("获取导购目标列表")
    # access_token = wm.get_access_token()
    # wm.get_store_guider_target_list(access_token)
    # mc154.get_create_sql('./Data/store_guider_target_list.csv','weimeng_store_guider_target_list')
    # mc154.insert_into_mysql_file_data('./Data/store_guider_target_list.csv', 'weimeng_store_guider_target_list', now_time)
    #
    # # 获取商户优惠券列表
    # print("获取商户优惠券列表")
    # access_token = wm.get_access_token()
    # wm.get_merchant_coupon_list(access_token)
    # mc154.get_create_sql('./Data/merchant_coupon_list.csv','weimeng_merchant_coupon_list')
    # mc154.insert_into_mysql_file_data('./Data/merchant_coupon_list.csv', 'weimeng_merchant_coupon_list', now_time)
    #
    # # 通过券码查询优惠券详情（C端）
    #
    # # 获取商户微客列表
    # print('获取商户微课列表')
    # access_token = wm.get_access_token()
    # wm.get_merchant_weike_list(access_token)
    # mc154.get_create_sql('./Data/merchant_weike_list.csv','weimeng_merchant_weike_list')
    # mc154.insert_into_mysql_file_data('./Data/merchant_weike_list.csv', 'weimeng_merchant_weike_list', now_time)
    #
    # # 获取商户微客明细
    # print('获取商户微课明细')
    # access_token = wm.get_access_token()
    # wm.get_weike_detail(access_token)
    # mc154.get_create_sql('./Data/weike_detail.csv','weimeng_weike_detail')
    # mc154.insert_into_mysql_file_data('./Data/weike_detail.csv', 'weimeng_weike_detail', now_time)
    #
    # # 获取门店库存列表
    # print("获取门店库存列表")
    # access_token = wm.get_access_token()
    # wm.get_store_stock_list(access_token)
    # mc154.get_create_sql('./Data/store_stock_list.csv','weimeng_store_stock_list')
    # mc154.insert_into_mysql_file_data('./Data/store_stock_list.csv', 'weimeng_store_stock_list', now_time)
    #
    # # 获取订单详情
    # print("获取订单详情接口")
    # access_token = wm.get_access_token()
    # wm.get_order_detail(access_token)
    # mc154.get_create_sql('./Data/order_detail.csv','weimeng_sale_order_detail')
    # mc154.insert_into_mysql_file_data('./Data/order_detail.csv', 'weimeng_sale_order_detail', now_time)
    #
    # # 获取产品列表
    # print("获取产品列表")
    # access_token = wm.get_access_token()
    # wm.get_goods_list(access_token)
    # mc154.get_create_sql('./Data/goods_list.csv','weimeng_goods_list')
    # mc154.insert_into_mysql_file_data('./Data/goods_list.csv', 'weimeng_goods_list', now_time)
    #
    # # 获取产品明细
    # print("获取产品明细")
    # access_token = wm.get_access_token()
    # wm.get_goods_detail(access_token)
    # mc154.get_create_sql('./Data/goods_detail.csv','weimeng_goods_detail')
    # mc154.insert_into_mysql_file_data('./Data/goods_detail.csv', 'weimeng_goods_detail', now_time)
    #
    # # 获取售后订单列表
    # print("获取售后订单列表")
    # access_token = wm.get_access_token()
    # wm.get_rights_order_list(access_token)
    # mc154.get_create_sql('./Data/rights_order_list.csv','weimeng_rights_order_list')
    # mc154.insert_into_mysql_file_data('./Data/rights_order_list.csv', 'weimeng_rights_order_list', now_time)
    #
    # # 获取售后订单详情
    # print("获取售后订单详情")
    # access_token = wm.get_access_token()
    # wm.get_rights_order_detail(access_token)
    # mc154.get_create_sql('./Data/rights_order_detail.csv','weimeng_rights_order_detail')
    # mc154.insert_into_mysql_file_data('./Data/rights_order_detail.csv', 'weimeng_rights_order_detail', now_time)
    #
    # # 获取进销存单据列表（出入库）
    # print("获取进销存单据列表（出入库）")
    # access_token = wm.get_access_token()
    # wm.get_inventory_order_list(access_token)
    # mc154.get_create_sql('./Data/inventory_order_list.csv','weimeng_inventory_order_list')
    # mc154.insert_into_mysql_file_data('./Data/inventory_order_list.csv', 'weimeng_inventory_order_list', now_time)
    #
    # # 获取用户明细所有数据
    # print("获取用户明细所有数据")
    # while True:
    #     access_token = wm.get_access_token()
    #     res = wm.get_member_detail(access_token)
    #     if res ==[]:
    #         break
    #
    #
    # 获取微客的邀请客户列表
    print("获取微客的邀请客户列表")
    access_token = wm.get_access_token()
    wm.get_weike_invite_user_list(access_token)
    mc154.get_create_sql('./Data/weike_invite_user_list.csv','weimeng_weike_invite_user_list')
    mc154.insert_into_mysql_file_data('./Data/weike_invite_user_list.csv', 'weimeng_weike_invite_user_list', now_time)

    # 关闭driver客户端
    for i in range(0,50):
        time.sleep(0.2)
        access_token = wm.get_access_token()
    mc154.conn.close()

