# Author:Aliex ZJ
#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import cx_Oracle

conn=cx_Oracle.connect('v3xuser','v3xuser','10.149.1.18:1521/ORCL')  #连接数据库
c=conn.cursor()                                                 #获取cursor
x=c.execute('show databases;')                         #使用cursor进行各种操作
print(x.fetchone())
c.close()                                                       #关闭cursor
conn.close()