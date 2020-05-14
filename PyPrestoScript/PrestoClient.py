# Author:Aliex ZJ
#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import prestodb
from pyhive import hive


class PrestoClient():
    def __init__(self,port):
        self.conn=prestodb.dbapi.connect(
            host='10.149.1.{}'.format(port),
            port=8090,
            user='root',
            catalog='hive',
            schema='ods',
        )
        self.cur = self.conn.cursor()

    def queryBySql(self,sql):
        self.cur.execute(sql)
        result = self.cur.fetchall()
        return result

if __name__ == '__main__':
    pass
    # presto202 = PrestoClient('202')
    # sql = '''
    # select
    #     count(six)
    # from
    #     (SELECT
    #         a.wid as one,
    #         b.wid as two,
    #         c.wid as three,
    #         d.wid as four,
    #         e.wid as five,
    #         f.wid as six
    #     --	,g.wid as seven
    #     from
    #         (select
    #             wid,
    #             inviter
    #         from
    #             ods.s07_spider_weimeng_merchant_weike_list
    #         where inviter='0'
    #         ) as a
    #     left join
    #         ods.s07_spider_weimeng_merchant_weike_list as b
    #     on b.inviter=a.wid
    #     left join
    #         ods.s07_spider_weimeng_merchant_weike_list as c
    #     on c.inviter=b.wid
    #     left join
    #         ods.s07_spider_weimeng_merchant_weike_list as d
    #     on d.inviter=c.wid
    #     left join
    #         ods.s07_spider_weimeng_merchant_weike_list as e
    #     on e.inviter=d.wid
    #     left join
    #         ods.s07_spider_weimeng_merchant_weike_list as f
    #     on f.inviter=e.wid
    #     )'''
    # print(presto202.queryBySql(sql)[0][0])
    #
    # sql = sql.replace('''count(six)''','*')
    #
    # presto202.queryBySql('create table test.weimeng as '+sql)


