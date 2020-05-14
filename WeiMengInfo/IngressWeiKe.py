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
    time.sleep(1)
    client_id = 'EDD3EAB6F807344E8AB5AE583A3E073C'
    client_secret = '9B659BC31EF571D38DFA73DDAA61CC1B'
    week_day = datetime.datetime.now().weekday()
    # 新建微盟实例
    wm = WeiMengInterface(client_id, client_secret)
    # MySql客户端
    mc154 = MySqlClient(154, 'spider')

    # # 获取商户微客列表
    print('获取商户微课列表')
    access_token = wm.get_access_token()
    wm.get_merchant_weike_list(access_token)
    mc154.get_create_sql('./Data/merchant_weike_list.csv','weimeng_merchant_weike_list')
    mc154.insert_into_mysql_file_data('./Data/merchant_weike_list.csv', 'weimeng_merchant_weike_list', now_time)

    # 获取商户微客明细
    # print('获取商户微课明细')
    # access_token = wm.get_access_token()
    # wm.get_weike_detail(access_token)
    # mc154.get_create_sql('./Data/weike_detail.csv','weimeng_weike_detail')
    # mc154.insert_into_mysql_file_data('./Data/weike_detail.csv', 'weimeng_weike_detail', now_time)

    # 获取微客的邀请客户列表
    print("获取微客的邀请客户列表")
    access_token = wm.get_access_token()
    wm.get_weike_invite_user_list(access_token)
    mc154.get_create_sql('./Data/weike_invite_user_list.csv','weimeng_weike_invite_user_list')
    mc154.insert_into_mysql_file_data('./Data/weike_invite_user_list.csv', 'weimeng_weike_invite_user_list', now_time)
    #
    # # 获取用户微信
    # access_token = wm.get_access_token()
    # wm.get_user_info(access_token)

    # 关闭driver客户端
    for i in range(0,10):
        time.sleep(0.2)
        access_token = wm.get_access_token()
    mc154.conn.close()

