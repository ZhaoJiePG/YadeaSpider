# Author:Aliex ZJ
# !/usr/bin/env python3
# -*- coding:utf-8 -*-
import datetime
import time

import pandas
import requests
import sys

from WeiMengInfo.PrestoClient import PrestoClient

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
    # mc154 = MySqlClient(154, 'spider')
    access_token = wm.get_access_token()

    dict_abc = {1:'a',2:'b',3:'c',4:'d',5:'e',6:'f',7:'g',8:'h',9:'i',10:'j',11:'k',12:'l',13:'m'}

    append_str1 = ''
    append_str2 = ''
    append_str3 = ''

    index = 0
    while True:
        index = index + 1
        # 初始化，跳出第一次循环
        if (index == 1):
            continue
        # 当前字段表名
        column = 'weike'+str(index)
        # 上个字段表名
        last_column = 'weike' + str(index-1)
        append_str1 = column
        append_str2 = append_str2 + '\n,{0}.wid as {1}'.format(column,column)
        append_str3 = append_str3 +'''
            left join ods.s07_spider_weimeng_merchant_weike_list as {0}
            on {1}.inviter={2}.wid
            '''.format(column,column,last_column)
        # 动态拼接sql
        sql = '''
            select
                count({0})
            from 
                (select
                    weike1.inviter as zero
                    ,weike1.wid as weike1{1}
                from
                    ods.s07_spider_weimeng_merchant_weike_list as weike1{2}
                )'''.format(append_str1,append_str2,append_str3)
        # 查询是否结束
        presto202 = PrestoClient('202')
        res = presto202.queryBySql(sql)[0][0]
        print('当前结果'+str(res))
        # if res == 0:
        if index == 10:
            print('数据到尽头，结束循环，当前循环表到'+column)
            # 创建表
            presto202.queryBySql('create table ods.s07_weimeng_weike_process_relation as '
                                 +sql.replace('count({})'.format(column),'*')
                                 +" where zero='0'")
            break

