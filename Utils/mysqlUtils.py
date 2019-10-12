# Author:Aliex ZJ
#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# 保存数据到mysql
import pymysql
def saveToMysql(data,databaseName,tableName):
    config = dict(host='10.149.1.154', user='root', password='root',
                  cursorclass=pymysql.cursors.DictCursor)
    # 建立连接
    conn = pymysql.Connect(**config)
    print(conn)
    # 自动确认commit True
    conn.autocommit(1)
    # 设置光标
    cursor = conn.cursor()

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

    def csv2mysql(db_name, table_name, df):
        # 创建database
        cursor.execute('CREATE DATABASE IF NOT EXISTS {}'.format(db_name))
        # # 选择连接database
        conn.select_db(db_name)
        # # 创建table
        cursor.execute('DROP TABLE IF EXISTS {}'.format(table_name))
        cursor.execute('CREATE TABLE {}({})'.format(table_name,make_table_sql(df)))
        # # 删除今日数据
        truncate_sql = 'DELETE FROM {0}'.format(table_name)
        cursor.execute(truncate_sql)
        # 提取数据转list 这里有与pandas时间模式无法写入因此换成str 此时mysql上格式已经设置完成
        # df['日期'] = df['日期'].astype('str')
        values = df.values.tolist()
        # 根据columns个数
        s = ','.join(['%s' for _ in range(len(df.columns))])
        # executemany批量操作 插入数据 批量操作比逐个操作速度快很多
        cursor.executemany('INSERT INTO {} VALUES ({})'.format(table_name, s), values)

    csv2mysql(databaseName, tableName, data)

    conn.close()

def insertIntoMysql(data,databaseName,tableName):
    config = dict(host='10.149.1.154', user='root', password='root',
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
    # truncate_sql = 'DELETE FROM {0}'.format(tableName)
    # cursor.execute(truncate_sql)
    # 提取数据转list 这里有与pandas时间模式无法写入因此换成str 此时mysql上格式已经设置完成
    # df['日期'] = df['日期'].astype('str')
    values = data.values.tolist()
    # 根据columns个数
    s = ','.join(['%s' for _ in range(len(data.columns))])
    # executemany批量操作 插入数据 批量操作比逐个操作速度快很多
    cursor.executemany('INSERT INTO {} VALUES ({})'.format(tableName, s), values)

