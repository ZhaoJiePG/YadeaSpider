# Author:Aliex ZJ
#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import requests

access_token='c1d71ede-d0e8-41ea-af3d-c44362b0a050'
url = 'https://dopen.weimob.com/api/1_0/mc/member/getMemberList?accesstoken={0}'.format(access_token)

data={
    "cursor": 12344,
    "size": 100
}
response = requests.post(
    url=url,
    data=data)

user_list = list(response.json()['data']['items'])
for user in user_list:
    wid = user['wid']
    print(user)
    res = requests.post('https://dopen.weimob.com/api/1_0/uc/user/getUserInfo?accesstoken={0}'.format(access_token),
                  data={
                      "wid": wid
                  }).text
    print(res)

    print()
