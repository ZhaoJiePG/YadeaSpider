# Author:Aliex ZJ
#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import prestodb
conn = prestodb.dbapi.connect(
    host='10.149.1.202',
    port=8090,
    user='the-user',
    catalog='hive',
    schema='dm',
)
cur = conn.cursor()
cur.execute('SELECT * FROM hive.dwd.dwd_sale_store_ecommerce_dtl limit 10')
rows = cur.fetchone()
print(rows)