# Author:Aliex ZJ
#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os

import pandas as pd


class fileUtils():
    # 保存csv格式
    def saveAsCsv(self,data, name):
        df = pd.DataFrame(data).drop_duplicates()
        df.to_csv("{}.csv".format(name), sep=',', header=True, index=False, encoding='utf-8')
        print("{}.csv".format(name)+"保存成功")

    # 获取csv格式
    def getCsvFile(self,fileName):
        # 读取csv文件
        csv_file = open(fileName, 'rb').read().decode('utf-8')
        # 保存地区和url
        url_list = []
        for x in csv_file.split('\r\n'):
            url_info = x.split(',')
            url_list.append([url_info[0],url_info[1]])

        return url_list

    # 读取文件内容
    def getFileData(self,filename):
        with open(filename,'r',encoding='utf-8') as f:
            data = f.readlines()
        count = 0
        for i in data:
            count = count+1
        return [count,str(data)]

    # 获取文件夹下的所有文件名称
    def eachFile(self,filepath):
        list = []
        pathDir =  os.listdir(filepath)
        for allDir in pathDir:
            child = os.path.join('%s%s' % (filepath, allDir))
            list.append(child)
        return list

# a = fileUtils().getCsvFile("D:\Maven\PyScrapy\Yadea\CompetitiveBrandStoreArea\Datas\XingRi\新日.csv")
# print(a)