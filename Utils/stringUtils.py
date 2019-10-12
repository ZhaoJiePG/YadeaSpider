# Author:Aliex ZJ
#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import re


class stringUtils():
    def __init__(self):
        pass

    # 字符串%unicode解码中文
    def unicode2str(self,str):
        res = eval(repr(str.replace('%u', '\\u')).replace('\\\\','\\')).encode('unicode_escape').decode('unicode_escape')
        # 过滤北京
        resBeiJing = res.replace('%28', '').replace('(', '').replace(')', '').replace(' ', '').replace('（', '').replace('）', '').replace('-', '').replace('%20','').replace('A','').replace('姜海燕','').replace('、','')
        # 过滤天津
        resTianJing = resBeiJing.replace('%0','').replace('：','')
        return (resBeiJing,resTianJing)



