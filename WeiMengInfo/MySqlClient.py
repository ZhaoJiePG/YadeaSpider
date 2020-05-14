# Author:Aliex ZJ
#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import datetime

import pandas
import pymysql
from pandas.errors import EmptyDataError

now_time = datetime.datetime.now().strftime('%Y-%m-%d')

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
            resData = pandas.read_csv(file_name, encoding='utf-8', low_memory=False,error_bad_lines=False)
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

if __name__ == '__main__':

    mc154 = MySqlClient(154,'soider')
    mc154.query_sql_lists('''
        SELECT
            weike_wid as fu,
            wid as er
        from 
            spider.weimeng_weike_invite_user_list
        union 
        SELECT
            REPLACE(REPLACE(inviter,'{"wid":',''),'}','')as fu,
            wid as er
        from 
            spider.weimeng_merchant_weike_list''')
