# Author:Aliex ZJ
#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# 保存数据到mysql
import os
from time import sleep
import pandas as pd

import pymysql
from pandas.errors import EmptyDataError


def createTable(df,database_name,table_name,port):
    config = dict(host='10.149.1.{0}'.format(port), user='root', password='root',
                  cursorclass=pymysql.cursors.DictCursor)
    # 建立连接
    conn = pymysql.Connect(**config)
    print(conn)
    # 自动确认commit True
    conn.autocommit(1)
    # 设置光标
    cursor = conn.cursor()
    # 选择连接database
    conn.select_db(database_name)
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
    cursor.execute('CREATE TABLE {}({})'.format(table_name,make_table_sql(df)))

    conn.close()

def truncateTable(databaseName,tableName,port):
    config = dict(host='10.149.1.{0}'.format(port), user='root', password='root',
                  cursorclass=pymysql.cursors.DictCursor)
    # 建立连接
    conn = pymysql.Connect(**config)
    print(conn)
    # 自动确认commit True
    conn.autocommit(1)
    # 设置光标
    cursor = conn.cursor()
    # # 选择连接database
    conn.select_db(databaseName)
    truncate_sql = 'DELETE FROM {0}'.format(tableName)
    cursor.execute(truncate_sql)

def insertIntoMysql(data,databaseName,tableName,port):
    config = dict(host='10.149.1.{0}'.format(port), user='root', password='root',
                  cursorclass=pymysql.cursors.DictCursor)
    # 建立连接
    conn = pymysql.Connect(**config)
    print(conn)
    # 自动确认commit True
    conn.autocommit(1)
    # 设置光标
    cursor = conn.cursor()
    # # 选择连接database
    conn.select_db(databaseName)
    # 提取数据转list 这里有与pandas时间模式无法写入因此换成str 此时mysql上格式已经设置完成
    # df['日期'] = df['日期'].astype('str')
    values = data.values.tolist()
    # 根据columns个数
    s = ','.join(['%s' for _ in range(len(data.columns))])
    # executemany批量操作 插入数据 批量操作比逐个操作速度快很多
    cursor.executemany('INSERT INTO {} VALUES ({})'.format(tableName, s), values)

# 保存到数据库
def save_to_mysql(file_addr,database_name,table_name,port):
    # 清空数据
    truncateTable(database_name,table_name,port)
    for dirs in os.walk(file_addr):
        fileList = dirs[2]
        for fileName in fileList:
            # 读取每个文件
            csvFile=file_addr+'/{0}'.format(fileName)
            print('开始存储'+str(csvFile)+'数据到mysql')
            try:
                resData = pd.read_csv(csvFile,encoding='utf-8')
                # 去除空值
                resData = resData.astype(object).where(pd.notnull(resData), None)
                print(resData)
                # 插入数据库
                insertIntoMysql(resData,database_name,table_name,port)
            except EmptyDataError:
                print("当前商品不符合规则")

            sleep(2)