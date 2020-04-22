# Author:Aliex ZJ
# !/usr/bin/env python3
# -*- coding:utf-8 -*-
import datetime
import json
import os
import re
import time

import pandas
import pymysql
import requests
import logging

from pandas.errors import EmptyDataError
from pandas.tests.frame.test_validate import dataframe

now_time = datetime.datetime.now().strftime('%Y-%m-%d')

# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
from selenium import webdriver


# MySql客户端
class MySqlClient():
    def __init__(self, port, database):
        self.port = port
        self.database = database
        config = dict(host='10.149.1.{0}'.format(port), user='root', password='root',
                      cursorclass=pymysql.cursors.DictCursor)
        # 建立连接
        self.conn = pymysql.Connect(**config)
        self.conn.autocommit(1)
        self.cursor = self.conn.cursor()
        self.conn.select_db(self.database)

    # 创建表
    def create_table(self, df, table_name):
        # 自动确认commit True
        self.conn.autocommit(1)
        # 设置光标
        cursor = self.conn.cursor()
        # 选择连接database
        self.conn.select_db(self.database)

        def make_table_sql(df):
            global char
            columns = df.columns.tolist()
            types = df.ftypes
            # 添加id 制动递增主键模式
            make_table = []
            for item in columns:
                if 'int' in types[item]:
                    char = item + ' BIGINT'
                elif 'float' in types[item]:
                    char = item + ' FLOAT'
                elif 'object' in types[item]:
                    char = item + ' VARCHAR(255)'
                elif 'datetime' in types[item]:
                    char = item + ' DATETIME'
                make_table.append(char)
            return ','.join(make_table)

        cursor.execute('DROP TABLE IF EXISTS {}'.format(table_name))
        cursor.execute('CREATE TABLE {}({})'.format(table_name, make_table_sql(df)))

    # 清空今日数据
    def truncate_day_data(self, table_name, add_time):
        # 选择连接database
        truncate_sql = "DELETE FROM {0} WHERE add_time='{1}'".format(table_name, add_time)
        print(truncate_sql)
        self.cursor.execute(truncate_sql)
        print('清除本日数据成功')

    # 清空数据
    def truncate_table(self, table_name):
        # 选择连接database
        truncate_sql = "DELETE FROM {0}".format(table_name)
        print(truncate_sql)
        self.cursor.execute(truncate_sql)
        print('清除数据成功')

    # 按照文件和日期增量插入数据
    def insert_into_mysql_file_data(self, file_name, table_name, add_time):
        try:
            resData = pandas.read_csv(file_name, encoding='utf-8', low_memory=False)
            # 去除空值
            resData = resData.astype(object).where(pandas.notnull(resData), None)
            resData = resData[resData['add_time'] == add_time]
            print(resData)
            # 提取数据转list 这里有与pandas时间模式无法写入因此换成str 此时mysql上格式已经设置完成
            # df['日期'] = df['日期'].astype('str')
            values = resData.values.tolist()
            # 根据columns个数
            s = ','.join(['%s' for _ in range(len(resData.columns))])
            # executemany批量操作 插入数据 批量操作比逐个操作速度快很多
            self.cursor.executemany('INSERT INTO {} VALUES ({})'.format(table_name, s), values)
            print('数据插入成功')
        except EmptyDataError:
            print("当前商品不符合规则")

    # 查询
    def query_sql_list(self, sql, column):
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        list = []
        for res in data:
            a = res[column]
            list.append(a)
        return list

    # 查询
    def query_sql_lists(self, sql):
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        return data

    # 获取建表语句
    def get_create_sql(self,file_name,table_name):
        header = open(file_name,'r',encoding='utf-8').readlines()[0]
        try:
            self.cursor.execute("drop table {};".format(table_name))
        except BaseException:
            print("表已存在")
        sql = "CREATE TABLE {} (".format(table_name)+header.replace(',',' varchar(255) DEFAULT NULL,')+" varchar(255) DEFAULT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8;"
        print(sql)
        self.cursor.execute(sql)
        print("动态建表成功")



# 微盟实列
class WeiMengInterface():
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        # option = webdriver.ChromeOptions()
        # self.driver = webdriver.Chrome(executable_path='./chromedriver.exe', chrome_options=option)

    def get_csv_line(self, file_name, add_time, line):
        resData = pandas.read_csv(file_name, encoding='utf-8', low_memory=False)
        # 去除空值
        resData = resData.astype(object).where(pandas.notnull(resData), None)
        resData = resData[resData['add_time'] == add_time]
        return resData[line].values

    def get_csv_line_only(self, file_name, line):
        resData = pandas.read_csv(file_name, encoding='utf-8', low_memory=False)
        # 去除空值
        resData = resData.astype(object).where(pandas.notnull(resData), None)
        return resData[line].values

    # 保存csv格式(插入不覆盖)
    def save_as_csv_insert(self, data, file_name):
        df = pandas.DataFrame(data).drop_duplicates()
        df.to_csv("{}.csv".format(file_name), sep=',', header=False, index=False, encoding='utf-8', mode='a')
        # print("{}.csv".format(file_name) + "保存成功")

    # 保存csv格式(删除并创建+表头)
    def save_as_csv_create(self, data, file_name):
        df = pandas.DataFrame(data).drop_duplicates()
        df.to_csv("{}.csv".format(file_name), sep=',', header=True, index=False, encoding='utf-8')
        # print("{}.csv".format(file_name) + "保存成功")

    # 获取文件的最后一条数据
    def get_file_last_line(self, file_name):
        with open(file_name, 'r') as fp:
            lines = fp.readlines()
        last_line = lines[-1]
        return last_line

    # 保存文件
    def save_as_file_insert(self, file_name, data):
        with open(file_name, 'a+') as fp:
            fp.write('\n')
            fp.write(data)
        print('游标' + data + '写入成功')

    # 登陆保存cookie
    # def login_save_cookiie(self):
    #     # 手动登陆
    #     login_url = "http://account.weimob.com/"
    #     self.driver.get(login_url)
    #     time.sleep(20)
    #     cookie = self.driver.get_cookies()
    #     self.driver.quit()
    #     # 保存cookie
    #     jsonCookies = json.dumps(cookie)
    #     with open('WeiMengCookie.json', 'w') as f:
    #         f.write(jsonCookies)

    # 获取code
    # def get_code(self):
    #     # 授权网站
    #     url = 'https://dopen.weimob.com/fuwu/b/oauth2/authorize?enter=wm&view=pc&response_type=code&scope=default&client_id=EDD3EAB6F807344E8AB5AE583A3E073C&redirect_uri=https://www.baidu.com'
    #     # 初始化，清空cookie
    #     self.driver.get(url)
    #     self.driver.delete_all_cookies()
    #     # 读入文件获取cookie
    #     fr = open('./Data/WeiMengCookie.json', 'r')
    #     cookielist = json.load(fr)
    #     print(cookielist)
    #     fr.close()
    #     for cookie in cookielist:
    #         if 'expiry' in cookie:
    #             del cookie['expiry']
    #         self.driver.add_cookie(cookie)
    #     # 授权网站
    #
    #     self.driver.get(url)
    #     time.sleep(1)
    #     # 模拟点击授权
    #     self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/form/div[2]/a').click()
    #     time.sleep(1)
    #     # 获取code
    #     print(self.driver.current_url)
    #     code = re.findall('code=(.*)', self.driver.current_url)[0]
    #     print("code获取成功：" + code)
    #     self.driver.quit()
    #     return code

    # 通过code，请求获取refresh_token
    def get_refresh_token(self, code):
        print("获取新的refresh_token")
        # https://dopen.weimob.com/fuwu/b/oauth2/authorize?enter=wm&view=pc&response_type=code&scope=default&client_id=EDD3EAB6F807344E8AB5AE583A3E073C&redirect_uri=https://www.baidu.com
        url = "https://dopen.weimob.com/fuwu/b/oauth2/token?code={0}&grant_type=authorization_code&client_id={1}&client_secret={2}&redirect_uri=https://www.baidu.com" \
            .format(code, self.client_id, self.client_secret)
        res = requests.post(url).json()
        refresh_token = res['refresh_token']
        with open('./Data/refresh_token', 'w') as f:
            f.write(refresh_token)
        print("新" + refresh_token + "写入成功")

    # 通过refresh_token请求获取access_token
    def get_access_token(self):
        with open('./Data/refresh_token', 'r') as f:
            refresh_token = f.read()
        url = "https://dopen.weimob.com/fuwu/b/oauth2/token?grant_type=refresh_token&client_id={0}&client_secret={1}&refresh_token={2}" \
            .format(self.client_id, self.client_secret, refresh_token)
        print(url)
        res = requests.post(url).json()
        access_token = res["access_token"]
        print("access_token 刷新成功：" + access_token)
        return access_token

    # 会员列表列(微商城)
    def get_member_list(self, access_token):
        # member_table = []
        url = 'https://dopen.weimob.com/api/1_0/mc/member/getMemberList?accesstoken={0}'.format(access_token)
        print("会员列表列接口url：" + url)
        # cursor  滚动游标
        # size    滚动数量
        cursor = self.get_file_last_line('./Data/member_list_cursor')
        data = {
            "cursor": cursor,
            "size": 1
        }
        i = 1
        # 循环获取
        while True:
            member_table = []
            json_data = json.dumps(data)
            res = requests.post(url=url, data=json_data).json()
            print(json_data)
            print("第" + str(i) + "次请求")
            print(res)
            # 获取新游标
            new_cursor = res['data']['cursor']
            int(new_cursor)
            self.save_as_file_insert('./Data/member_list_cursor', str(new_cursor))
            # 获取会员数据
            member_list = res['data']['items']
            for members in member_list:
                member = {}
                # 获取只需要的字段
                for item in dict(members).keys():
                    if item != "":
                        member[item] = str(members[item]).replace('\'','\"').lower()
                member["add_time"] = now_time
                member_table.append(member)
                # 游标为0创建，否则插入
            print("当前游标" + data["cursor"])
            if data["cursor"] == '0':
                self.save_as_csv_create(data=member_table, file_name='./Data/member_list')
            else:
                self.save_as_csv_insert(data=member_table, file_name='./Data/member_list')
            # 改变游标
            data["cursor"] = self.get_file_last_line('./Data/member_list_cursor')
            if data["cursor"] != 0:
                data["size"] = 500
            i = i + 1
            if (i == 500):
                break

    # 客户详情会员(微商城)
    def get_member_detail(self, access_token):
        url = 'https://dopen.weimob.com/api/1_0/mc/member/getMemberDetail?accesstoken={0}'.format(access_token)
        print("客户详情接口url：" + url)
        mc = MySqlClient(154, 'spider')
        wids = mc.query_sql_list(
            """SELECT
                wid
            from 
                spider.weimeng_user_member_list as a 
            where not exists (
                SELECT
                    wid 
                from 
                    spider.weimeng_user_member_detail as b 
                where a.wid=b.wid)limit 500""", 'wid')

        print("需要获取" + str(len(wids)) + "个用户信息")
        member_table = []
        # 读取非会员
        NoneMember = self.get_csv_line_only('./Data/NoneMember.csv', 'wid')
        wids = list(set(wids).difference(set(NoneMember)))
        i = 0
        for wid in wids:
            try:
                i = i + 1
                print("开始第" + str(i) + "次请求" + str(wid) + "用户的数据")
                data = json.dumps({
                    "type": 0,
                    "wid": "{}".format(wid)
                })
                res = requests.post(url, data).json()
                # 获取会员数据
                members = res['data']
                member = {}
                # 获取只需要的字段
                for item in dict(members).keys():
                    if item != "":
                        member[item] = str(members[item]).replace('\'','\"')
                member["add_time"] = now_time
                member_table.append(member)
                if i == 500: break
                # 判断文件是否存在,存在插入，不存在创建表头
                # if (not os.path.exists('./Data/member_detail.csv')):
                #     self.save_as_csv_create(data=member_table, file_name='./Data/member_detail')
                # else:
                #     self.save_as_csv_insert(data=member_table, file_name='./Data/member_detail')
            except requests.exceptions.SSLError:
                print('请求次数过多，重新请求')
                break
            except requests.exceptions.ConnectionError:
                print('链接异常，重新请求')
                break
            except TypeError:
                self.save_as_file_insert('./Data/NoneMember.csv', str(wid))
                print('不是会员，跳出')
                continue
        self.save_as_csv_create(data=member_table, file_name='./Data/member_detail')
        mc.insert_into_mysql_file_data('./Data/member_detail.csv', 'weimeng_user_member_detail', now_time)
        mc.conn.close()
        return member_table

    # 获取订单列表(智慧零售)
    def get_order_list(self, access_token):
        sale_order_table = []
        i = 0
        while True:
            i = i + 1
            data = {
                "pageNum": i,
                "pageSize": 100
            }
            data_json = json.dumps(data)
            print(data_json)
            response = requests.post(
                'https://dopen.weimob.com/api/1_0/ec/order/queryOrderList?accesstoken={}'.format(access_token),
                data=data_json).json()
            sale_orders = response["data"]["pageList"]
            if sale_orders == []:
                print("数据全部请求完成")
                break
            for sale_order in sale_orders:
                sale_order_dict = {}
                for item in dict(sale_order).keys():
                    if item != "":
                        sale_order_dict[item] = str(sale_order[item]).replace('\'','\"')
                sale_order_dict["add_time"] = now_time
                sale_order_table.append(sale_order_dict)
            print("请求" + str(i))
        self.save_as_csv_create(data=sale_order_table, file_name='./Data/order_list')

    # 获取订单详情(智慧零售)
    def get_order_detail(self, access_token):
        url = 'https://dopen.weimob.com/api/1_0/ec/order/queryOrderDetail?accesstoken={0}'.format(access_token)
        print("客户详情接口url：" + url)
        mc = MySqlClient(154, 'spider')
        orderNos = mc.query_sql_list(
            """	SELECT
                    orderNo
                from 
                    spider.weimeng_sale_order_list""", 'orderNo')

        print("需要获取" + str(len(orderNos)) + "个订单信息")
        print(orderNos)
        member_table = []
        i = 0
        for orderNo in orderNos:
            try:
                i = i + 1
                print("开始第" + str(i) + "次请求" + str(orderNo) + "订单的数据")
                data = json.dumps({
                    "orderNo": orderNo
                })
                res = requests.post(url, data).json()
                # 获取会员数据
                members = res['data']
                member = {}
                # 获取只需要的字段
                for item in dict(members).keys():
                    if item != "":
                        member[item] = str(members[item]).replace('\'','\"')
                member["add_time"] = now_time
                member_table.append(member)
            except requests.exceptions.SSLError:
                print('请求次数过多，重新请求')
                break
            except requests.exceptions.ConnectionError:
                print('链接异常，重新请求')
                break
        self.save_as_csv_create(data=member_table, file_name='./Data/order_detail')
        mc.conn.close()

    # 获取门店列表(智慧零售)
    def get_store_list(self, access_token):
        sale_order_table = []
        i = 0
        while True:
            i = i + 1
            data = {
                "pageNum": i,
                "pageSize": 100
            }
            data_json = json.dumps(data)
            print(data_json)
            response = requests.post(
                'https://dopen.weimob.com/api/1_0/ec/merchant/queryStoreList?accesstoken={}'.format(access_token),
                data=data_json).json()
            sale_orders = response["data"]["pageList"]
            if sale_orders == []:
                print("数据全部请求完成")
                break
            for sale_order in sale_orders:
                sale_order_dict = {}
                for item in dict(sale_order).keys():
                    if item != "":
                        sale_order_dict[item] = str(sale_order[item]).replace('\'','\"')
                sale_order_dict["add_time"] = now_time
                sale_order_table.append(sale_order_dict)
            print("请求" + str(i))
        self.save_as_csv_create(data=sale_order_table, file_name='./Data/store_list')

    # 获取订单详情(智慧零售)
    def get_store_detail(self, access_token):
        url = 'https://dopen.weimob.com/api/1_0/ec/merchant/getStoreInfo?accesstoken={0}'.format(access_token)
        print("客户详情接口url：" + url)
        mc = MySqlClient(154, 'spider')
        storeIds = mc.query_sql_list(
            """	SELECT
                    id
                from 
                    spider.weimeng_store_list""", 'id')

        print("需要获取" + str(len(storeIds)) + "个门店信息")
        member_table = []
        i = 0
        for storeId in storeIds:
            try:
                i = i + 1
                print("开始第" + str(i) + "次请求" + str(storeId) + "门店的数据")
                data = json.dumps({
                    "storeId": storeId
                })
                res = requests.post(url, data).json()
                # 获取会员数据
                members = res['data']
                member = {}
                # 获取只需要的字段
                for item in dict(members).keys():
                    if item != "":
                        member[item] = str(members[item]).replace('\'','\"')
                member["add_time"] = now_time
                member_table.append(member)
            except requests.exceptions.SSLError:
                print('请求次数过多，重新请求')
                break
            except requests.exceptions.ConnectionError:
                print('链接异常，重新请求')
                break
        self.save_as_csv_create(data=member_table, file_name='./Data/store_detail')
        mc.conn.close()

    # 查询导购列表(智慧零售)
    def get_store_guider_list(self, access_token):
        sale_order_table = []
        i = 0
        while True:
            i = i + 1
            data = {
                "pageNum": i,
                "pageSize": 100
            }
            data_json = json.dumps(data)
            print(data_json)
            response = requests.post(
                'https://dopen.weimob.com/api/1_0/ec/guide/findGuiderList?accesstoken={}'.format(access_token),
                data=data_json).json()
            sale_orders = response["data"]["pageList"]
            if sale_orders == []:
                print("数据全部请求完成")
                break
            for sale_order in sale_orders:
                sale_order_dict = {}
                for item in dict(sale_order).keys():
                    if item != "":
                        sale_order_dict[item] = str(sale_order[item]).replace('\'','\"')
                sale_order_dict["add_time"] = now_time
                sale_order_table.append(sale_order_dict)
            print("请求" + str(i))
        self.save_as_csv_create(data=sale_order_table, file_name='./Data/store_guider_list')

    # 获取导购目标列表(智慧零售)
    def get_store_guider_target_list(self, access_token):
        sale_order_table = []
        i = 0
        while True:
            i = i + 1
            data = {
                "fiscalYear": 2020,
                "pageNum": i,
                "pageSize": 100
            }
            data_json = json.dumps(data)
            print(data_json)
            try:
                response = requests.post(
                    'https://dopen.weimob.com/api/1_0/ec/guide/queryGuiderTargetList?accesstoken={}'.format(
                        access_token), data=data_json).json()
                sale_orders = response["data"]["pageList"]

                for sale_order in sale_orders:
                    sale_order_dict = {}
                    for item in dict(sale_order).keys():
                        if item != "":
                            sale_order_dict[item] = str(sale_order[item]).replace('\'','\"')
                    sale_order_dict["add_time"] = now_time
                    sale_order_table.append(sale_order_dict)
            except TypeError:
                print("数据全部请求完成")
                break
        self.save_as_csv_create(data=sale_order_table, file_name='./Data/store_guider_target_list')

    # 获取商户优惠券列表(智慧零售)
    def get_merchant_coupon_list(self, access_token):
        sale_order_table = []
        i = 0
        while True:
            i = i + 1
            data = {
                "pageSize": 20,
                "pageNum": i
            }
            data_json = json.dumps(data)
            print(data_json)
            response = requests.post(
                'https://dopen.weimob.com/api/1_0/ec/coupon/getMerchantCouponList?accesstoken={}'.format(access_token),
                data=data_json).json()
            sale_orders = response["data"]["pageList"]
            if sale_orders == []:
                print("数据全部请求完成")
                break
            for sale_order in sale_orders:
                sale_order_dict = {}
                for item in dict(sale_order).keys():
                    if item != "":
                        sale_order_dict[item] = str(sale_order[item]).replace('\'','\"')
                sale_order_dict["add_time"] = now_time
                sale_order_table.append(sale_order_dict)
        self.save_as_csv_create(data=sale_order_table, file_name='./Data/merchant_coupon_list')

    # 获取商户微客列表
    def get_merchant_weike_list(self, access_token):
        sale_order_table = []
        i = 0
        while True:
            i = i + 1
            data = {
                "pageSize": 50,
                "pageNum": i
            }
            data_json = json.dumps(data)
            print(data_json)
            response = requests.post(
                'https://dopen.weimob.com/api/1_0/newsdp/weike/getMerchantWeikeList?accesstoken={}'.format(
                    access_token), data=data_json).json()
            sale_orders = response["data"]["pageList"]
            if sale_orders == []:
                print("数据全部请求完成")
                break
            for sale_order in sale_orders:
                sale_order_dict = {}
                for item in dict(sale_order).keys():
                    if item != "":
                        sale_order_dict[item] = str(sale_order[item]).replace('\'','\"')
                sale_order_dict["add_time"] = now_time
                sale_order_table.append(sale_order_dict)
        self.save_as_csv_create(data=sale_order_table, file_name='./Data/merchant_weike_list')

    # 获取微客的基本信息
    def get_weike_detail(self, access_token):
        url = 'https://dopen.weimob.com/api/1_0/newsdp/weike/getWeike?accesstoken={0}'.format(access_token)
        print("客户详情接口url：" + url)
        mc = MySqlClient(154, 'spider')
        orderNos = mc.query_sql_list(
            """	SELECT
                    wid
                from 
                    spider.weimeng_sale_order_list""", 'wid')

        print("需要获取" + str(len(orderNos)) + "个订单信息")
        print(orderNos)
        member_table = []
        i = 0
        for orderNo in orderNos:
            try:
                i = i + 1
                print("开始第" + str(i) + "次请求" + str(orderNo) + "微客的数据")
                data = json.dumps({
                    "wid": orderNo
                })
                res = requests.post(url, data).json()
                # 获取会员数据
                members = res['data']
                member = {}
                # 获取只需要的字段
                for item in dict(members).keys():
                    if item != "":
                        member[item] = str(members[item]).replace('\'','\"')
                member["add_time"] = now_time
                member_table.append(member)
            except requests.exceptions.SSLError:
                print('请求次数过多，重新请求')
                break
            except requests.exceptions.ConnectionError:
                print('链接异常，重新请求')
                break
            except TypeError:
                print('没有数据，重新请求')
                continue
        self.save_as_csv_create(data=member_table, file_name='./Data/weike_detail')
        mc.conn.close()

    # 获取商户分账记录列表
    def get_commission_record_list(self, access_token):
        url = 'https://dopen.weimob.com/api/1_0/newsdp/order/getCommissionRecordList?accesstoken={0}'.format(
            access_token)
        print("客户详情接口url：" + url)
        mc = MySqlClient(154, 'spider')
        orders = mc.query_sql_lists(
            """	SELECT
                merchantinfo,
                orderno
            from 
                weimeng_sale_order_detail""")

        for order in orders:
            storeid = eval(order['merchantinfo'])['storeId']
            orderid = order['orderno']
        member_table = []
        i = 0
        # for orderNo in orderNos:
        #     try:
        #         i = i + 1
        #         print("开始第"+str(i)+"次请求" + str(orderNo) + "订单的数据")
        #         data = json.dumps({
        #             "orderNo": orderNo
        #         })
        #         res = requests.post(url, data).json()
        #         # 获取会员数据
        #         members = res['data']
        #         member = {}
        #         # 获取只需要的字段
        #         for item in dict(members).keys():
        #             if item != "":
        #                 member[item] = str(members[item])
        #         member["add_time"] = now_time
        #         member_table.append(member)
        #     except requests.exceptions.SSLError:
        #         print('请求次数过多，重新请求')
        #         break
        #     except requests.exceptions.ConnectionError:
        #         print('链接异常，重新请求')
        #         break
        # self.save_as_csv_create(data=member_table, file_name='./Data/order_detail')
        # mc.conn.close()

    # 获取门店库存列表
    # http://yun.weimob.com/saas/word/detailApi.html?tag=282&menuId=1&id=550
    def get_store_stock_list(self, access_token):
        sale_order_table = []
        i = 0
        while True:
            i = i + 1
            data = {
                "pageNum": i,
                "pageSize": 500,
                "queryParameter": {
                    "searchType": 0,
                    "type": 1
                }
            }
            data_json = json.dumps(data)
            print(data_json)
            response = requests.post(
                'https://dopen.weimob.com/api/1_0/ec/stock/queryStoreStockListWithPage?accesstoken={}'.format(
                    access_token), data=data_json).json()
            sale_orders = response["data"]["pageList"]
            if sale_orders == []:
                print("数据全部请求完成")
                break
            for sale_order in sale_orders:
                sale_order_dict = {}
                for item in dict(sale_order).keys():
                    if item != "":
                        sale_order_dict[item] = str(sale_order[item]).replace('\'','\"')
                sale_order_dict["add_time"] = now_time
                sale_order_table.append(sale_order_dict)
        self.save_as_csv_create(data=sale_order_table, file_name='./Data/store_stock_list')

    # 获取进销存单据列表
    # http://yun.weimob.com/saas/word/detailApi.html?tag=282&menuId=1&id=562
    # def get_inventory_order_list(self, access_token):
    #     sale_order_table = []
    #     i = 0
    #     while True:
    #         i = i + 1
    #         data = {
    #             "pageNum": i,
    #             "pageSize": 500,
    #             "queryParameter": {
    #                 "searchType": 0,
    #                 "type": 1
    #             }
    #         }
    #         data_json = json.dumps(data)
    #         print(data_json)
    #         response = requests.post(
    #             'https://dopen.weimob.com/api/1_0/ec/stock/queryInventoryOrderListWithPage?accesstoken={}'.format(
    #                 access_token), data=data_json).json()
    #         sale_orders = response["data"]["pageList"]
    #         if sale_orders == []:
    #             print("数据全部请求完成")
    #             break
    #         for sale_order in sale_orders:
    #             sale_order_dict = {}
    #             for item in dict(sale_order).keys():
    #                 if item != "":
    #                     sale_order_dict[item] = str(sale_order[item]).replace('\'','\"')
    #             sale_order_dict["add_time"] = now_time
    #             sale_order_table.append(sale_order_dict)
    #     self.save_as_csv_create(data=sale_order_table, file_name='./Data/store_stock_list')

if __name__ == '__main__':
    client_id = 'EDD3EAB6F807344E8AB5AE583A3E073C'
    client_secret = '9B659BC31EF571D38DFA73DDAA61CC1B'
    week_day = datetime.datetime.now().weekday()
    # 新建微盟实例
    wm = WeiMengInterface(client_id, client_secret)
    # MySql客户端
    mc154 = MySqlClient(154, 'spider')

    # # 每周一获取code
    # if (week_day == 99):
    #     print("********周一，开始获取code********")
    #     code = wm.get_code()
    #     # 获取refresh_token(一周获取一次)
    #     print("\n********获取refresh_token********")
    #     wm.get_refresh_token(code=code)

    # # 增量获取会员列表列(循环获取，每次500次请求，每个请求500条数据)
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
    # # # 获取订单列表
    # print("获取获取订单列表情接口")
    # access_token = wm.get_access_token()
    # wm.get_order_list(access_token)
    # # mc154.create_table(pandas.read_csv('./Data/order_list.csv', low_memory=False), 'weimeng_sale_order_list')
    # mc154.truncate_table('weimeng_sale_order_list')
    # mc154.insert_into_mysql_file_data('./Data/order_list.csv', 'weimeng_sale_order_list', now_time)
    #
    # # # 获取门店列表
    # print("获取门店列表接口")
    # access_token = wm.get_access_token()
    # wm.get_store_list(access_token)
    # # mc154.create_table(pandas.read_csv('./Data/store_list.csv', low_memory=False), 'weimeng_store_list')
    # mc154.truncate_table('weimeng_store_list')
    # mc154.insert_into_mysql_file_data('./Data/store_list.csv', 'weimeng_store_list', now_time)
    #
    # # 获取门店详情
    # print("获取门店详情接口")
    # access_token = wm.get_access_token()
    # wm.get_store_detail(access_token)
    # # mc154.create_table(pandas.read_csv('./Data/store_detail.csv', low_memory=False), 'weimeng_store_detail')
    # mc154.truncate_table('weimeng_store_detail')
    # mc154.insert_into_mysql_file_data('./Data/store_detail.csv', 'weimeng_store_detail', now_time)
    #
    # # 获取查询导购列表
    # print("获取查询导购列表")
    # access_token = wm.get_access_token()
    # wm.get_store_guider_list(access_token)
    # # mc154.create_table(pandas.read_csv('./Data/store_guider_list.csv', low_memory=False), 'weimeng_store_guider_list')
    # mc154.truncate_table('weimeng_store_guider_list')
    # mc154.insert_into_mysql_file_data('./Data/store_guider_list.csv', 'weimeng_store_guider_list', now_time)
    #
    # # 获取导购目标列表
    # print("获取导购目标列表")
    # access_token = wm.get_access_token()
    # wm.get_store_guider_target_list(access_token)
    # # mc154.create_table(pandas.read_csv('./Data/store_guider_target_list.csv', low_memory=False), 'weimeng_store_guider_target_list')
    # mc154.truncate_table('weimeng_store_guider_target_list')
    # mc154.insert_into_mysql_file_data('./Data/store_guider_target_list.csv', 'weimeng_store_guider_target_list', now_time)
    #
    # # 获取商户优惠券列表
    # print("获取商户优惠券列表")
    # access_token = wm.get_access_token()
    # wm.get_merchant_coupon_list(access_token)
    # # mc154.create_table(pandas.read_csv('./Data/merchant_coupon_list.csv', low_memory=False), 'weimeng_merchant_coupon_list')
    # mc154.truncate_table('weimeng_merchant_coupon_list')
    # mc154.insert_into_mysql_file_data('./Data/merchant_coupon_list.csv', 'weimeng_merchant_coupon_list', now_time)
    #
    # # 通过券码查询优惠券详情（C端）
    #
    # # 获取商户微客列表
    # print('获取商户微课列表')
    # access_token = wm.get_access_token()
    # wm.get_merchant_weike_list(access_token)
    # # mc154.create_table(pandas.read_csv('./Data/merchant_weike_list.csv', low_memory=False), 'weimeng_merchant_weike_list')
    # mc154.truncate_table('weimeng_merchant_weike_list')
    # mc154.insert_into_mysql_file_data('./Data/merchant_weike_list.csv', 'weimeng_merchant_weike_list', now_time)
    #
    # # 获取商户微客明细
    # print('获取商户微课明细')
    # access_token = wm.get_access_token()
    # wm.get_weike_detail(access_token)
    # # mc154.create_table(pandas.read_csv('./Data/weike_detail.csv', low_memory=False), 'weimeng_weike_detail')
    # mc154.truncate_table('weimeng_weike_detail')
    # mc154.insert_into_mysql_file_data('./Data/weike_detail.csv', 'weimeng_weike_detail', now_time)

    # 获取门店库存列表
    # access_token = wm.get_access_token()
    # wm.get_store_stock_list(access_token)
    # mc154.get_create_sql('./Data/store_stock_list.csv','weimeng_store_stock_list')
    # mc154.insert_into_mysql_file_data('./Data/store_stock_list.csv', 'weimeng_store_stock_list', now_time)

    # # 获取商户分账记录列表
    # # access_token = wm.get_access_token()
    # # wm.get_commission_record_list(access_token)
    #
    # # 获取订单详情
    print("获取订单详情接口")
    access_token = wm.get_access_token()
    wm.get_order_detail(access_token)
    mc154.get_create_sql('./Data/order_detail.csv','weimeng_sale_order_detail')
    mc154.insert_into_mysql_file_data('./Data/order_detail.csv', 'weimeng_sale_order_detail', now_time)
    #
    # # 获取用户明细所有数据
    # while True:
    #     access_token = wm.get_access_token()
    #     res = wm.get_member_detail(access_token)
    #     if res ==[]:
    #         break
    #
    # # 关闭driver客户端
    for i in range(0,50):
        time.sleep(0.2)
        access_token = wm.get_access_token()
    mc154.conn.close()

