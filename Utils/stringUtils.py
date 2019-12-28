# Author:Aliex ZJ
#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import re
# from pypinyin import lazy_pinyin, pinyin

# 字符串%unicode解码中文
def unicode2str(str):
    res = eval(repr(str.replace('%u', '\\u')).replace('\\\\','\\')).encode('unicode_escape').decode('unicode_escape')
    # 过滤北京
    resBeiJing = res.replace('%28', '').replace('(', '').replace(')', '').replace(' ', '').replace('（', '').replace('）', '').replace('-', '').replace('%20','').replace('A','').replace('姜海燕','').replace('、','')
    # 过滤天津
    resTianJing = resBeiJing.replace('%0','').replace('：','')
    return (resBeiJing,resTianJing)

# 去除换行符和空格
def delSpecialChars(str):
    return str.replace('\n','').replace(' ','').replace('(','').replace(')','').replace('\xa0', '')

# 中文转拼音
def str2pinyon(str):
    res = ''
    py_list=lazy_pinyin(str)
    for py in py_list:
        res=res+py

    return res
