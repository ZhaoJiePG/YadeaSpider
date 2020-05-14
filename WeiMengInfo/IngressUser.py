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
    time.sleep(10)
    client_id = 'EDD3EAB6F807344E8AB5AE583A3E073C'
    client_secret = '9B659BC31EF571D38DFA73DDAA61CC1B'
    week_day = datetime.datetime.now().weekday()
    # 新建微盟实例
    wm = WeiMengInterface(client_id, client_secret)
    # MySql客户端
    mc154 = MySqlClient(154, 'spider')

    # # 增量获取会员列表列(循环获取，每次500次请求，每个请求500条数据)
    print("********获取会员列表列********")
    while True:
        try:
            # 刷新access_token(2小时一次)
            print("\n********刷新access_token(2小时一次)********")
            access_token = wm.get_access_token()
            print(access_token)
            wm.get_member_list(access_token=access_token)
        except requests.exceptions.ConnectionError:
            print("请求次数过多，重新获取")
            continue
        except TypeError:
            print("数据请求结束，退出循环")
            break
    # 增量保存会员列表信息
    # mc154.create_table(pandas.read_csv('./Data/member_list.csv', low_memory=False), 'weimeng_user_member_list')
    mc154.truncate_day_data('weimeng_user_member_list',now_time)
    mc154.insert_into_mysql_file_data('./Data/member_list.csv','weimeng_user_member_list',now_time)

    # 获取用户明细所有数据
    print("获取用户明细所有数据")
    while True:
        try:
            access_token = wm.get_access_token()
            res = wm.get_member_detail(access_token)
        except ValueError:
            break
        if res ==[]:
            break

    # 获取用户会员卡明细
    access_token = wm.get_access_token()
    wm.get_query_user_info(access_token)

    # 关闭driver客户端
    for i in range(0,10):
        time.sleep(0.2)
        access_token = wm.get_access_token()
    mc154.conn.close()