# Author:Aliex ZJ
#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from Utils.fileUtils import fileUtils

datas = fileUtils().getCsvFile('D:\Maven\YadeaSpider\MapStoreAddress\Data\Baidu_cityCode.csv')
print(datas)