# Author:Aliex ZJ
#!/usr/bin/env python3
# -*- coding:utf-8 -*-

str_list=[
    'b.dealer_code',
    'b.dealer_name',
    'b.store_code',
    'b.store_name',
    'b.store_grade',
    'b.store_province',
    'b.store_city'
]
res_list = ""
for str in str_list:
    res = "if({0} is null or {1}='','其它',{2})as {3},\n".format(str,str,str,str[2:])
    res_list=res_list+res


print(res_list)
