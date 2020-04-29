# Author:Aliex ZJ
# !/usr/bin/env python3
# -*- coding:utf-8 -*-
import datetime
import json
import time

import requests
from selenium import webdriver


data = json.dumps({
    "type": 0,
    "wid": 1733396477
})
print(requests.post('https://dopen.weimob.com/api/1_0/mc/member/getMemberDetail?accesstoken=b91b451f-49a9-4751-88e3-5e4baa646564',data).json())

timeStamp = 1583283345
dateArray = datetime.datetime.fromtimestamp(timeStamp)
otherStyleTime = dateArray.strftime("%Y--%m--%d %H:%M:%S")
print(otherStyleTime)   # 2013--10--10 23:40:00