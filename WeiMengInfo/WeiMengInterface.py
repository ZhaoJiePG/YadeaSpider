# Author:Aliex ZJ
# !/usr/bin/env python3
# -*- coding:utf-8 -*-
import pandas
import requests
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class WeiMengInterface():
    def __init__(self, code, client_id, client_secret):
        self.code = code
        self.client_id = client_id
        self.client_secret = client_secret

    # 保存csv格式
    def saveAsCsv(self,data, file_name):
        df = pandas.DataFrame(data).drop_duplicates()
        df.to_csv("{}.csv".format(file_name), sep=',', header=True, index=False, encoding='utf-8')
        print("{}.csv".format(file_name)+"保存成功")

    # 通过code，请求获取refresh_token
    def get_refresh_token(self):
        # https://dopen.weimob.com/fuwu/b/oauth2/authorize?enter=wm&view=pc&response_type=code&scope=default&client_id=EDD3EAB6F807344E8AB5AE583A3E073C&redirect_uri=https://www.baidu.com
        url = "https://dopen.weimob.com/fuwu/b/oauth2/token?code={0}&grant_type=authorization_code&client_id={1}&client_secret={2}&redirect_uri=https://www.baidu.com" \
            .format(self.code, self.client_id, self.client_secret)
        res = requests.post(url).json()
        refresh_token = res['refresh_token']
        with open('./refresh_token', 'w') as f:
            f.write(refresh_token)
        print(refresh_token + "写入成功")

    # 通过refresh_token请求获取access_token
    def get_access_token(self):
        with open('./refresh_token', 'r') as f:
            refresh_token = f.read()
        url = "https://dopen.weimob.com/fuwu/b/oauth2/token?grant_type=refresh_token&client_id={0}&client_secret={1}&refresh_token={2}" \
            .format(self.client_id, self.client_secret, refresh_token)
        res = requests.post(url).json()
        access_token = res["access_token"]
        print("access_token 刷新成功：" + access_token)
        return access_token

    # 会员列表列
    def get_member_list(self, access_token):
        member_table = []
        url = 'https://dopen.weimob.com/api/1_0/mc/member/getMemberList?accesstoken={0}'.format(access_token)
        print("会员列表列接口url："+url)
        # cursor  滚动游标
        # size    滚动数量
        data = {
            "cursor": 12344,
            "size": 1000
        }
        res = requests.post(url=url,data=data).json()
        # 获取会员数据
        member_list = res['data']['items']
        for member in member_list:
            print("获取用户 "+str(member['name'])+" 的数据：wid为"+str(member['wid']))
            member_table.append(member)

        self.saveAsCsv(data=member_table,file_name='member_list')



if __name__ == '__main__':
    # 新建微盟实例
    code = 'ZrW3Q8'
    client_id = 'EDD3EAB6F807344E8AB5AE583A3E073C'
    client_secret = '9B659BC31EF571D38DFA73DDAA61CC1B'
    wm = WeiMengInterface(code, client_id, client_secret)

    # 获取refresh_token(一周获取一次)
    # wm.get_refresh_token()

    # 刷新access_token(2小时一次)
    print("********刷新access_token(2小时一次)********")
    access_token = wm.get_access_token()
    print()

    # 获取会员列表列
    print("********获取会员列表列********")
    wm.get_member_list(access_token=access_token)

