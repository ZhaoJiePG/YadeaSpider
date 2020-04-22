# Author:Aliex ZJ
#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import pandas
import prestodb


conn=prestodb.dbapi.connect(
    host='10.149.1.202',
    port=8090,
    user='root',
    catalog='hive',
    schema='ods',
)
cur = conn.cursor()
# cur.execute('SELECT * FROM dwd.dwd_prod_wide limit 10')
# cur.execute("create table test.testcoon(id int,name varchar)")
# rows = cur.fetchall()
# print(rows)

table_name = 'ods.s07_weimeng_user_member_list'

data_dic = pandas.read_csv('D:\Maven\YadeaSpider\WeiMengInfo\Data\member_list.csv',nrows=1)
df = pandas.DataFrame(data_dic)
resData = df.astype(object).where(pandas.notnull(df), '无')
print(resData)

res = ""
values = resData.values.tolist()[0]
print(values)
# 根据columns个数
for index in range(0,len(values)):
    if(index == len(values)-1):
        res = res + str(values[index])
    else :
        res = res + str(values[index])+","

print(res)
# executemany批量操作 插入数据 批量操作比逐个操作速度快很多
insert_sql = 'INSERT INTO {} VALUES ({})'.format(table_name, res)
print(insert_sql)
cur.execute('INSERT INTO ods.s07_weimeng_user_member_list VALUES (2020-04-06,无,0,0,无,无,无,0,无,0,无,1583220576000,无,无,无,无,无,无,610512223,无,无,无,无,0,3,1732946183)')
cur.execute('INSERT INTO test.testcoon1 select 1,2,3')