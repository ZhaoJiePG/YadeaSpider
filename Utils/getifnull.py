# Author:Aliex ZJ
#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# 自动生成ifelse

def get(str_list):
    res_list=""
    for str in str_list:
        res = ""
        try:
            res = ("if({} is null or {}='','其它',{})as {}".format(str,str,str,str[str.index('.')+1:]))
        except BaseException:
            res = ("if({} is null or {}='','其它',{})as {}".format(str,str,str,str))

        res_list=res_list+res+',\n'
    return res_list

print(get(['f.pic1',
           'f.pic1_status',
           'f.pic2',
           'f.pic2_status',
           'f.pic3',
           'f.pic3_status']))