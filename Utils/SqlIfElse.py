# Author:Aliex ZJ
#!/usr/bin/env python3
# -*- coding:utf-8 -*-

str_list=[
    'a.battery_code_hy',
    'a.battery_name_hy',
    'a.charge_code_hy',
    'a.charge_name_hy'
]
res_list = ""
for str in str_list:
    res = "if({0} is null or {1}='','其它',{2})as {3},\n".format(str,str,str,str[2:])
    res_list=res_list+res


print(res_list)
