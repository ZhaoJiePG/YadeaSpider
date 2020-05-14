# Author:Aliex ZJ
# !/usr/bin/env python3
# -*- coding:utf-8 -*-
import datetime
import json
import os
from json import JSONDecodeError

import pandas
import requests

from WeiMengInfo.MySqlClient import MySqlClient

now_time = datetime.datetime.now().strftime('%Y-%m-%d')

# 微盟实列
class WeiMengInterface():
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        # option = webdriver.ChromeOptions()
        # self.driver = webdriver.Chrome(executable_path='./chromedriver.exe', chrome_options=option)

    def get_dict_value(self,dict,key):
        try:
            value = str(dict[key]).replace('\'','\"')
        except KeyError:
            value = ''
        return value

    def get_csv_line(self, file_name, add_time, line):
        resData = pandas.read_csv(file_name, encoding='utf-8', low_memory=False)
        # 去除空值
        resData = resData.astype(object).where(pandas.notnull(resData), None)
        resData = resData[resData['add_time'] == add_time]
        return resData[line].values

    def get_csv_line_only(self, file_name, line):
        resData = pandas.read_csv(file_name, encoding='utf-8', low_memory=False)
        # 去除空值
        resData = resData.astype(object).where(pandas.notnull(resData), None)
        return resData[line].values

    # 保存csv格式(插入不覆盖)
    def save_as_csv_insert(self, data, file_name):
        df = pandas.DataFrame(data).drop_duplicates()
        df.to_csv("{}.csv".format(file_name), sep=',', header=False, index=False, encoding='utf-8', mode='a')
        # print("{}.csv".format(file_name) + "保存成功")

    # 保存csv格式(删除并创建+表头)
    def save_as_csv_create(self, data, file_name):
        df = pandas.DataFrame(data).drop_duplicates()
        df.to_csv("{}.csv".format(file_name), sep=',', header=True, index=False, encoding='utf-8')
        # print("{}.csv".format(file_name) + "保存成功")

    # 获取文件的最后一条数据
    def get_file_last_line(self, file_name):
        with open(file_name, 'r') as fp:
            lines = fp.readlines()
        last_line = lines[-1]
        return last_line

    # 保存文件
    def save_as_file_insert(self, file_name, data):
        with open(file_name, 'a+') as fp:
            fp.write('\n')
            fp.write(data)
        print('游标' + data + '写入成功')

    # 登陆保存cookie
    # def login_save_cookiie(self):
    #     # 手动登陆
    #     login_url = "http://account.weimob.com/"
    #     self.driver.get(login_url)
    #     time.sleep(20)
    #     cookie = self.driver.get_cookies()
    #     self.driver.quit()
    #     # 保存cookie
    #     jsonCookies = json.dumps(cookie)
    #     with open('WeiMengCookie.json', 'w') as f:
    #         f.write(jsonCookies)

    # 获取code
    # def get_code(self):
    #     # 授权网站
    #     url = 'https://dopen.weimob.com/fuwu/b/oauth2/authorize?enter=wm&view=pc&response_type=code&scope=default&client_id=EDD3EAB6F807344E8AB5AE583A3E073C&redirect_uri=https://www.baidu.com'
    #     # 初始化，清空cookie
    #     self.driver.get(url)
    #     self.driver.delete_all_cookies()
    #     # 读入文件获取cookie
    #     fr = open('./Data/WeiMengCookie.json', 'r')
    #     cookielist = json.load(fr)
    #     print(cookielist)
    #     fr.close()
    #     for cookie in cookielist:
    #         if 'expiry' in cookie:
    #             del cookie['expiry']
    #         self.driver.add_cookie(cookie)
    #     # 授权网站
    #
    #     self.driver.get(url)
    #     time.sleep(1)
    #     # 模拟点击授权
    #     self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/form/div[2]/a').click()
    #     time.sleep(1)
    #     # 获取code
    #     print(self.driver.current_url)
    #     code = re.findall('code=(.*)', self.driver.current_url)[0]
    #     print("code获取成功：" + code)
    #     self.driver.quit()
    #     return code

    # 通过code，请求获取refresh_token
    def get_refresh_token(self, code):
        print("获取新的refresh_token")
        # https://dopen.weimob.com/fuwu/b/oauth2/authorize?enter=wm&view=pc&response_type=code&scope=default&client_id=EDD3EAB6F807344E8AB5AE583A3E073C&redirect_uri=https://www.baidu.com
        url = "https://dopen.weimob.com/fuwu/b/oauth2/token?code={0}&grant_type=authorization_code&client_id={1}&client_secret={2}&redirect_uri=https://www.baidu.com" \
            .format(code, self.client_id, self.client_secret)
        res = requests.post(url).json()
        refresh_token = res['refresh_token']
        with open('./Data/refresh_token', 'w') as f:
            f.write(refresh_token)
        print("新" + refresh_token + "写入成功")

    # 通过refresh_token请求获取access_token
    def get_access_token(self):
        with open('./Data/refresh_token', 'r') as f:
            refresh_token = f.read()
        url = "https://dopen.weimob.com/fuwu/b/oauth2/token?grant_type=refresh_token&client_id={0}&client_secret={1}&refresh_token={2}" \
            .format(self.client_id, self.client_secret, refresh_token)
        print(url)
        res = requests.post(url).json()
        access_token = res["access_token"]
        print("access_token 刷新成功：" + access_token)
        return access_token

    # 会员列表列(微商城)
    def get_member_list(self, access_token):
        # member_table = []
        url = 'https://dopen.weimob.com/api/1_0/mc/member/getMemberList?accesstoken={0}'.format(access_token)
        print("会员列表列接口url：" + url)
        # cursor  滚动游标
        # size    滚动数量
        cursor = self.get_file_last_line('./Data/member_list_cursor')
        data = {
            "cursor": cursor,
            "size": 1
        }
        i = 1
        # 循环获取
        while True:
            member_table = []
            json_data = json.dumps(data)
            res = requests.post(url=url, data=json_data).json()
            print(json_data)
            print("第" + str(i) + "次请求")
            print(res)
            # 获取新游标
            new_cursor = res['data']['cursor']
            int(new_cursor)
            self.save_as_file_insert('./Data/member_list_cursor', str(new_cursor))
            # 获取会员数据
            member_list = res['data']['items']
            for members in member_list:
                member_table.append({'wid':members['wid'],'name':members['name'],'phone':members['phone'],'add_time':now_time})
                # 游标为0创建，否则插入
            print("当前游标" + data["cursor"])
            if data["cursor"] == '0':
                self.save_as_csv_create(data=member_table, file_name='./Data/member_list')
            else:
                self.save_as_csv_insert(data=member_table, file_name='./Data/member_list')
            # 改变游标
            data["cursor"] = self.get_file_last_line('./Data/member_list_cursor')
            if data["cursor"] != 0:
                data["size"] = 500
            i = i + 1
            if (i == 500):
                break

    # 客户详情会员(微商城)
    def get_member_detail(self, access_token):
        url = 'https://dopen.weimob.com/api/1_0/mc/member/getMemberDetail?accesstoken={0}'.format(access_token)
        print("客户详情接口url：" + url)
        mc = MySqlClient(154, 'spider')
        wids = mc.query_sql_list(
            """SELECT
                wid
            from 
                spider.weimeng_user_member_list as a 
            where not exists (
                SELECT
                    wid 
                from 
                    spider.weimeng_user_member_detail as b 
                where a.wid=b.wid)limit 500""", 'wid')

        print("需要获取" + str(len(wids)) + "个用户信息")
        member_table = []
        # 读取非会员
        NoneMember = self.get_csv_line_only('./Data/NoneMember.csv', 'wid')
        wids = list(set(wids).difference(set(NoneMember)))
        i = 0
        for wid in wids:
            try:
                i = i + 1
                print("开始第" + str(i) + "次请求" + str(wid) + "用户的数据")
                data = json.dumps({
                    "type": 0,
                    "wid": "{}".format(wid)
                })
                res = requests.post(url, data).json()
                # 获取会员数据
                members = res['data']
                member = {}
                # 获取只需要的字段
                for item in dict(members).keys():
                    if item != "":
                        member[item] = str(members[item]).replace('\'','\"')
                member["add_time"] = now_time
                member_table.append(member)
                if i == 500: break
                # 判断文件是否存在,存在插入，不存在创建表头
                # if (not os.path.exists('./Data/member_detail.csv')):
                #     self.save_as_csv_create(data=member_table, file_name='./Data/member_detail')
                # else:
                #     self.save_as_csv_insert(data=member_table, file_name='./Data/member_detail')
            except requests.exceptions.SSLError:
                print('请求次数过多，重新请求')
                break
            except requests.exceptions.ConnectionError:
                print('链接异常，重新请求')
                break
            except TypeError:
                self.save_as_file_insert('./Data/NoneMember.csv', str(wid))
                print('不是会员，跳出')
                continue
        self.save_as_csv_create(data=member_table, file_name='./Data/member_detail')
        mc.insert_into_mysql_file_data('./Data/member_detail.csv', 'weimeng_user_member_detail', now_time)
        mc.conn.close()
        return member_table

    # 商城零售-查询客户详情（会员卡）
    def get_query_user_info(self, access_token):
        url = 'https://dopen.weimob.com/api/1_0/ec/membership/queryUserInfoOpen?accesstoken={0}'.format(access_token)
        print("客户详情接口url：" + url)
        mc = MySqlClient(154, 'spider')
        wids = mc.query_sql_list(
            """SELECT
                wid
            from 
                spider.weimeng_user_member_detail
            where rankId<>'None'""", 'wid')

        print("需要获取" + str(len(wids)) + "个用户信息")
        member_table = []
        # 读取非会员
        # NoneMember = self.get_csv_line_only('./Data/NoneMember_queryuserinfo.csv', 'wid')
        # wids = list(set(wids).difference(set(NoneMember)))
        i = 0
        for wid in wids:
            try:
                i = i + 1
                print("开始第" + str(i) + "次请求" + str(wid) + "用户的数据")
                data = json.dumps({
                    "wid": wid,
                    "storeId": "0"
                })
                res = requests.post(url, data).json()
                # 获取会员数据
                members = res['data']['memberCardInfoList'][0]
                # 获取只需要的字段
                member_table.append({'wid':wid,'add_time':now_time,'becomeMemberStoreId':self.get_dict_value(members,'becomeMemberStoreId'),'becomeMemberStoreName':self.get_dict_value(members,'becomeMemberStoreName')
                                        ,'becomeMemberTime':self.get_dict_value(members,'becomeMemberTime'),'cardName':self.get_dict_value(members,'cardName')
                                        ,'cardTemplateId':self.get_dict_value(members,'becomeMemberStoreId'),'cardType':self.get_dict_value(members,'cardType')
                                        ,'code':self.get_dict_value(members,'code'),'endDate':self.get_dict_value(members,'endDate')
                                        ,'getCardChannel':self.get_dict_value(members,'getCardChannel'),'getCardChannelName':self.get_dict_value(members,'getCardChannelName')
                                        ,'growth':self.get_dict_value(members,'growth'),'mid':self.get_dict_value(members,'mid')
                                        ,'rankId':self.get_dict_value(members,'rankId'),'rankName':self.get_dict_value(members,'rankName')
                                        ,'startDate':self.get_dict_value(members,'startDate'),'status':self.get_dict_value(members,'status')
                                        ,'statusName':self.get_dict_value(members,'statusName'),'wechatCardCode':self.get_dict_value(members,'wechatCardCode')
                                        ,'wechatCardStatus':self.get_dict_value(members,'wechatCardStatus')})
            except requests.exceptions.SSLError:
                print('请求次数过多，重新请求')
                continue
            except requests.exceptions.ConnectionError:
                print('链接异常，重新请求')
                continue
            except TypeError:
                # self.save_as_file_insert('./Data/NoneMember_queryuserinfo.csv', str(wid))
                print('不是会员，跳出')
                continue
            except JSONDecodeError:
                print('不是会员，跳出')
                continue
            except ValueError:
                print('没有数据，重新请求')
                continue
        self.save_as_csv_create(data=member_table, file_name='./Data/query_user_info')
        mc.truncate_table('weimeng_query_user_info')
        mc.get_create_sql('./Data/query_user_info.csv', 'weimeng_query_user_info')
        mc.insert_into_mysql_file_data('./Data/query_user_info.csv', 'weimeng_query_user_info', now_time)
        mc.conn.close()

    # 通过wid查询用户券码列表
    def get_coupon_page_by_wid(self, access_token):
        url = 'https://dopen.weimob.com/api/1_0/ec/coupon/getCouponPageByWid?accesstoken={0}'.format(access_token)
        print("客户详情接口url：" + url)
        mc = MySqlClient(154, 'spider')

        wids = mc.query_sql_list(
            """SELECT
                   wid
                from spider.weimeng_merchant_weike_list
                union 
                SELECT
                    wid
                from 
                    spider.weimeng_weike_invite_user_list
                """, 'wid')

        print("需要获取" + str(len(wids)) + "个用户信息")
        member_table = []
        # 读取非会员
        # NoneMember = self.get_csv_line_only('./Data/NoneMember_queryuserinfo.csv', 'wid')
        # wids = list(set(wids).difference(set(NoneMember)))
        i = 0
        for wid in wids:
            try:
                i = i + 1
                print("开始第" + str(i) + "次请求" + str(wid) + "用户的数据")
                for status in ['1','2','3','7']:
                    try:
                        data = json.dumps({
                            "wid": wid,
                            "pageSize": 100,
                            "pageNum": 1,
                            "queryParameter": {
                                "statusRange": [
                                    status
                                ]
                            }
                        })
                        res = requests.post(url, data).json()
                        # 获取会员数据
                        members = res['data']['pageList']
                        for member in members:
                            member_table.append({'wid':wid,'add_time':now_time
                                                ,'cardTemplateId':self.get_dict_value(member,'cardTemplateId'),'acceptGoodsType':self.get_dict_value(member,'acceptGoodsType')
                                                ,'cashTicketAmt':self.get_dict_value(member,'cashTicketAmt'),'cashTicketCondition':self.get_dict_value(member,'cashTicketCondition')
                                                ,'code':self.get_dict_value(member,'code'),'discount':self.get_dict_value(member,'discount')
                                                ,'expireDate':self.get_dict_value(member,'expireDate'),'isAvailable':self.get_dict_value(member,'isAvailable')
                                                ,'name':self.get_dict_value(member,'name'),'selectStoreType':self.get_dict_value(member,'selectStoreType')
                                                ,'startDate':self.get_dict_value(member,'startDate'),'status':self.get_dict_value(member,'status')
                                                ,'type':self.get_dict_value(member,'type'),'useNotice':self.get_dict_value(member,'useNotice')})
                    except TypeError:
                        print('券状态没有信息，跳出')
                        continue
            except requests.exceptions.SSLError:
                print('请求次数过多，重新请求')
                continue
            except requests.exceptions.ConnectionError:
                print('链接异常，重新请求')
                continue
            except TypeError:
                # self.save_as_file_insert('./Data/NoneMember_queryuserinfo.csv', str(wid))
                print('不是会员，跳出')
                continue
        self.save_as_csv_create(data=member_table, file_name='./Data/coupon_page_by_wid')
        mc.truncate_table('weimeng_coupon_page_by_wid')
        mc.get_create_sql('./Data/coupon_page_by_wid.csv','weimeng_coupon_page_by_wid')
        mc.insert_into_mysql_file_data('./Data/coupon_page_by_wid.csv', 'weimeng_coupon_page_by_wid', now_time)
        mc.conn.close()

    # 根据wid获取用户信息(unionid)
    def get_user_info(self, access_token):
        url = 'https://dopen.weimob.com/api/1_0/uc/user/getUserInfo?accesstoken={0}'.format(access_token)
        print("客户详情接口url：" + url)
        mc = MySqlClient(154, 'spider')
        wids = mc.query_sql_list(
            """SELECT
                   wid
                from spider.weimeng_merchant_weike_list
                union 
                SELECT
                    wid
                from 
                    spider.weimeng_weike_invite_user_list""", 'wid')

        print("需要获取" + str(len(wids)) + "个用户信息")
        member_table = []
        # 读取非会员
        # NoneMember = self.get_csv_line_only('./Data/NoneMember_queryuserinfo.csv', 'wid')
        # wids = list(set(wids).difference(set(NoneMember)))
        i = 0
        for wid in wids:
            try:
                i = i + 1
                print("开始第" + str(i) + "次请求" + str(wid) + "用户的数据")
                data = json.dumps({
                    "wid": wid
                })
                res = requests.post(url, data).json()
                # 获取会员数据
                members = res['data']
                # 获取只需要的字段
                member = members['sourceObjectList'][0]
                member_table.append({'wid':wid,'add_time':now_time,'superWid':self.get_dict_value(members,'superWid'),'pid':self.get_dict_value(members,'pid'),'sourceObjectList':self.get_dict_value(members,'sourceObjectList'),
                                     'sourceOpenid':self.get_dict_value(member,'sourceOpenid'),'sourceAppid':self.get_dict_value(member,'sourceAppid'),'subscribeTime':self.get_dict_value(member['sourceData'],'subscribeTime'),
                                     'unionid':self.get_dict_value(member['sourceData'],'unionid'),'nickname':self.get_dict_value(member['sourceData'],'nickname')})
            except requests.exceptions.SSLError:
                print('请求次数过多，重新请求')
                continue
            except requests.exceptions.ConnectionError:
                print('链接异常，重新请求')
                continue
            except TypeError:
                print('不是会员，跳出')
                continue
            except ValueError:
                print('没有数据，重新请求')
                continue
            except JSONDecodeError:
                print('没有数据，重新请求')
                continue
        self.save_as_csv_create(data=member_table, file_name='./Data/user_info')
        mc.truncate_table('weimeng_user_info')
        mc.get_create_sql('./Data/user_info.csv', 'weimeng_user_info')
        mc.insert_into_mysql_file_data('./Data/user_info.csv', 'weimeng_user_info', now_time)
        mc.conn.close()
        # return member_table

    # 获取订单列表(智慧零售)
    def get_order_list(self, access_token):
        sale_order_table = []
        i = 0
        while True:
            i = i + 1
            data = {
                "pageNum": i,
                "pageSize": 100
            }
            data_json = json.dumps(data)
            print(data_json)
            response = requests.post(
                'https://dopen.weimob.com/api/1_0/ec/order/queryOrderList?accesstoken={}'.format(access_token),
                data=data_json).json()
            sale_orders = response["data"]["pageList"]
            if sale_orders == []:
                print("数据全部请求完成")
                break
            for members in sale_orders:
                member = {'add_time':now_time,'orderNo': self.get_dict_value(members,'orderNo'),'pid': self.get_dict_value(members,'pid'),'wid': self.get_dict_value(members,'wid'),'userNickname': self.get_dict_value(members,'userNickname'),'existingInvoice': self.get_dict_value(members,'existingInvoice'),'guiderName': self.get_dict_value(members,'guiderName'),'orderStatus': self.get_dict_value(members,'orderStatus'),'orderStatusName': self.get_dict_value(members,'orderStatusName'),'deliveryType': self.get_dict_value(members,'deliveryType'),'bizType': self.get_dict_value(members,'bizType'),'subBizType': self.get_dict_value(members,'subBizType'),'bizOrderId': self.get_dict_value(members,'bizOrderId'),'confirmReceivedTime': self.get_dict_value(members,'confirmReceivedTime'),'deliveryTime': self.get_dict_value(members,'deliveryTime'),'enableDelivery': self.get_dict_value(members,'enableDelivery'),'deliveryTypeName': self.get_dict_value(members,'deliveryTypeName'),'paymentAmount': self.get_dict_value(members,'paymentAmount'),'deliveryAmount': self.get_dict_value(members,'deliveryAmount'),'channelType': self.get_dict_value(members,'channelType'),'channelTypeName': self.get_dict_value(members,'channelTypeName'),'paymentType': self.get_dict_value(members,'paymentType'),'paymentTypeName': self.get_dict_value(members,'paymentTypeName'),'paymentStatus': self.get_dict_value(members,'paymentStatus'),'paymentMethodName': self.get_dict_value(members,'paymentMethodName'),'createTime': self.get_dict_value(members,'createTime'),'updateTime': self.get_dict_value(members,'updateTime'),'paymentTime': self.get_dict_value(members,'paymentTime'),'totalPoint': self.get_dict_value(members,'totalPoint'),'transferType': self.get_dict_value(members,'transferType'),'transferStatus': self.get_dict_value(members,'transferStatus'),'transferFailReason': self.get_dict_value(members,'transferFailReason'),'selfPickupSiteName': self.get_dict_value(members,'selfPickupSiteName'),'processStoreTitle': self.get_dict_value(members,'processStoreTitle'),'processStoreId': self.get_dict_value(members,'processStoreId'),'storeId': self.get_dict_value(members,'storeId'),'storeTitle': self.get_dict_value(members,'storeTitle'),'flagRank': self.get_dict_value(members,'flagRank'),'flagContent': self.get_dict_value(members,'flagContent'),'itemList': self.get_dict_value(members,'itemList'),'buyerRemark': self.get_dict_value(members,'buyerRemark'),'receiverName': self.get_dict_value(members,'receiverName'),'receiverMobile': self.get_dict_value(members,'receiverMobile'),'receiverAddress': self.get_dict_value(members,'receiverAddress'),'expectDeliveryTime': self.get_dict_value(members,'expectDeliveryTime'),'deliveryOrderId': self.get_dict_value(members,'deliveryOrderId'),'errcode': self.get_dict_value(members,'errcode'),'errmsg': self.get_dict_value(members,'errmsg'),'goodsPromotionInfo': self.get_dict_value(members,'goodsPromotionInfo'),'bizSouceType': self.get_dict_value(members,'bizSouceType')}
                sale_order_table.append(member)
            print("请求" + str(i))
        self.save_as_csv_create(data=sale_order_table, file_name='./Data/order_list')

    # 获取订单详情(智慧零售)
    def get_order_detail(self, access_token):
        url = 'https://dopen.weimob.com/api/1_0/ec/order/queryOrderDetail?accesstoken={0}'.format(access_token)
        print("客户详情接口url：" + url)
        mc = MySqlClient(154, 'spider')
        orderNos = mc.query_sql_list(
            """	SELECT
                    orderNo
                from 
                    spider.weimeng_sale_order_list""", 'orderNo')

        print("需要获取" + str(len(orderNos)) + "个订单信息")
        print(orderNos)
        member_table = []
        i = 0
        for orderNo in orderNos:
            try:
                i = i + 1
                print("开始第" + str(i) + "次请求" + str(orderNo) + "订单的数据")
                data = json.dumps({
                    "orderNo": orderNo
                })
                res = requests.post(url, data).json()
                # 获取会员数据
                members = res['data']
                member = {'add_time':now_time,'orderNo':self.get_dict_value(members,'orderNo'),'enableDelivery':self.get_dict_value(members,'enableDelivery'),'orderStatus':self.get_dict_value(members,'orderStatus'),'orderStatusName':self.get_dict_value(members,'orderStatusName'),'transferType':self.get_dict_value(members,'transferType'),'transferStatus':self.get_dict_value(members,'transferStatus'),'transferTypeReality':self.get_dict_value(members,'transferTypeReality'),'createTime':self.get_dict_value(members,'createTime'),'confirmReceivedTime':self.get_dict_value(members,'confirmReceivedTime'),'autoCancelTime':self.get_dict_value(members,'autoCancelTime'),'autoConfirmReceivedTime':self.get_dict_value(members,'autoConfirmReceivedTime'),'goodsAmount':self.get_dict_value(members,'goodsAmount'),'totalAmount':self.get_dict_value(members,'totalAmount'),'deliveryAmount':self.get_dict_value(members,'deliveryAmount'),'deliveryPaymentAmount':self.get_dict_value(members,'deliveryPaymentAmount'),'deliveryDiscountAmount':self.get_dict_value(members,'deliveryDiscountAmount'),'shouldPaymentAmount':self.get_dict_value(members,'shouldPaymentAmount'),'paymentAmount':self.get_dict_value(members,'paymentAmount'),'channelTypeName':self.get_dict_value(members,'channelTypeName'),'buyerRemark':self.get_dict_value(members,'buyerRemark'),'buyerInfo':self.get_dict_value(members,'buyerInfo'),'invoiceInfo':self.get_dict_value(members,'invoiceInfo'),'invoiceTexAmount':self.get_dict_value(members,'invoiceTexAmount'),'invoiceTexPaymentAmount':self.get_dict_value(members,'invoiceTexPaymentAmount'),'invoiceTexDiscountAmount':self.get_dict_value(members,'invoiceTexDiscountAmount'),'guideInfo':self.get_dict_value(members,'guideInfo'),'merchantInfo':self.get_dict_value(members,'merchantInfo'),'paymentInfo':self.get_dict_value(members,'paymentInfo'),'itemList':self.get_dict_value(members,'itemList'),'discountInfo':self.get_dict_value(members,'discountInfo'),'bizInfo':self.get_dict_value(members,'bizInfo'),'deliveryDetail':self.get_dict_value(members,'deliveryDetail'),'flagRank':self.get_dict_value(members,'flagRank'),'flagContent':self.get_dict_value(members,'flagContent'),'deliveryTime':self.get_dict_value(members,'deliveryTime'),'cancelTime':self.get_dict_value(members,'cancelTime'),'cancelType':self.get_dict_value(members,'cancelType'),'customFieldList':self.get_dict_value(members,'customFieldList'),'refundInfo':self.get_dict_value(members,'refundInfo'),'memberDetailInfo':self.get_dict_value(members,'memberDetailInfo'),'errcode':self.get_dict_value(members,'errcode'),'errmsg':self.get_dict_value(members,'errmsg'),'goodsPromotionInfo':self.get_dict_value(members,'goodsPromotionInfo'),'goodsSellMode':self.get_dict_value(members,'goodsSellMode'),'updateTime':self.get_dict_value(members,'updateTime'),'finishTime':self.get_dict_value(members,'finishTime'),'bizSouceType':self.get_dict_value(members,'bizSouceType')}
                member_table.append(member)
            except requests.exceptions.SSLError:
                print('请求次数过多，重新请求')
                break
            except requests.exceptions.ConnectionError:
                print('链接异常，重新请求')
                break
        self.save_as_csv_create(data=member_table, file_name='./Data/order_detail')
        mc.conn.close()

    # 获取门店列表(智慧零售)
    def get_store_list(self, access_token):
        sale_order_table = []
        i = 0
        while True:
            i = i + 1
            data = {
                "pageNum": i,
                "pageSize": 100
            }
            data_json = json.dumps(data)
            print(data_json)
            response = requests.post(
                'https://dopen.weimob.com/api/1_0/ec/merchant/queryStoreList?accesstoken={}'.format(access_token),
                data=data_json).json()
            sale_orders = response["data"]["pageList"]
            if sale_orders == []:
                print("数据全部请求完成")
                break
            for sale_order in sale_orders:
                sale_order_dict = {}
                for item in dict(sale_order).keys():
                    if item != "":
                        sale_order_dict[item] = str(sale_order[item]).replace('\'','\"')
                sale_order_dict["add_time"] = now_time
                sale_order_table.append(sale_order_dict)
            print("请求" + str(i))
        self.save_as_csv_create(data=sale_order_table, file_name='./Data/store_list')

    # 获取门店详情(智慧零售)
    def get_store_detail(self, access_token):
        url = 'https://dopen.weimob.com/api/1_0/ec/merchant/getStoreInfo?accesstoken={0}'.format(access_token)
        print("客户详情接口url：" + url)
        mc = MySqlClient(154, 'spider')
        storeIds = mc.query_sql_list(
            """	SELECT
                    id
                from 
                    spider.weimeng_store_list""", 'id')

        print("需要获取" + str(len(storeIds)) + "个门店信息")
        member_table = []
        i = 0
        for storeId in storeIds:
            try:
                i = i + 1
                print("开始第" + str(i) + "次请求" + str(storeId) + "门店的数据")
                data = json.dumps({
                    "storeId": storeId
                })
                res = requests.post(url, data).json()
                # 获取会员数据
                members = res['data']
                member = {}
                # 获取只需要的字段
                for item in dict(members).keys():
                    if item != "":
                        member[item] = str(members[item]).replace('\'','\"')
                member["add_time"] = now_time
                member_table.append(member)
            except requests.exceptions.SSLError:
                print('请求次数过多，重新请求')
                break
            except requests.exceptions.ConnectionError:
                print('链接异常，重新请求')
                break
        self.save_as_csv_create(data=member_table, file_name='./Data/store_detail')
        mc.conn.close()

    # 查询导购列表(智慧零售)
    def get_store_guider_list(self, access_token):
        sale_order_table = []
        i = 0
        while True:
            i = i + 1
            data = {
                "pageNum": i,
                "pageSize": 100
            }
            data_json = json.dumps(data)
            print(data_json)
            response = requests.post(
                'https://dopen.weimob.com/api/1_0/ec/guide/findGuiderList?accesstoken={}'.format(access_token),
                data=data_json).json()
            sale_orders = response["data"]["pageList"]
            if sale_orders == []:
                print("数据全部请求完成")
                break
            for sale_order in sale_orders:
                sale_order_dict = {}
                for item in dict(sale_order).keys():
                    if item != "":
                        sale_order_dict[item] = str(sale_order[item]).replace('\'','\"')
                sale_order_dict["add_time"] = now_time
                sale_order_table.append(sale_order_dict)
            print("请求" + str(i))
        self.save_as_csv_create(data=sale_order_table, file_name='./Data/store_guider_list')

    # 获取导购目标列表(智慧零售)
    def get_store_guider_target_list(self, access_token):
        sale_order_table = []
        i = 0
        while True:
            i = i + 1
            data = {
                "fiscalYear": 2020,
                "pageNum": i,
                "pageSize": 100
            }
            data_json = json.dumps(data)
            print(data_json)
            try:
                response = requests.post(
                    'https://dopen.weimob.com/api/1_0/ec/guide/queryGuiderTargetList?accesstoken={}'.format(
                        access_token), data=data_json).json()
                sale_orders = response["data"]["pageList"]

                for sale_order in sale_orders:
                    sale_order_dict = {}
                    for item in dict(sale_order).keys():
                        if item != "":
                            sale_order_dict[item] = str(sale_order[item]).replace('\'','\"')
                    sale_order_dict["add_time"] = now_time
                    sale_order_table.append(sale_order_dict)
            except TypeError:
                print("数据全部请求完成")
                break
        self.save_as_csv_create(data=sale_order_table, file_name='./Data/store_guider_target_list')

    # 获取商户优惠券列表(智慧零售)
    def get_merchant_coupon_list(self, access_token):
        sale_order_table = []
        i = 0
        while True:
            i = i + 1
            data = {
                "pageSize": 20,
                "pageNum": i
            }
            data_json = json.dumps(data)
            print(data_json)
            response = requests.post(
                'https://dopen.weimob.com/api/1_0/ec/coupon/getMerchantCouponList?accesstoken={}'.format(access_token),
                data=data_json).json()
            sale_orders = response["data"]["pageList"]
            if sale_orders == []:
                print("数据全部请求完成")
                break
            for sale_order in sale_orders:
                sale_order_dict = {}
                for item in dict(sale_order).keys():
                    if item != "":
                        sale_order_dict[item] = str(sale_order[item]).replace('\'','\"')
                sale_order_dict["add_time"] = now_time
                sale_order_table.append(sale_order_dict)
        self.save_as_csv_create(data=sale_order_table, file_name='./Data/merchant_coupon_list')

    # 获取商户微客列表
    def get_merchant_weike_list(self, access_token):
        sale_order_table = []
        i = 0
        while True:
            i = i + 1
            data = {
                "pageSize": 50,
                "pageNum": i
            }
            data_json = json.dumps(data)
            print(data_json)
            response = requests.post(
                'https://dopen.weimob.com/api/1_0/newsdp/weike/getMerchantWeikeList?accesstoken={}'.format(
                    access_token), data=data_json).json()
            sale_orders = response["data"]["pageList"]
            if sale_orders == []:
                print("数据全部请求完成")
                break
            for sale_order in sale_orders:
                sale_order_table.append({'add_time':now_time,'inviter':self.get_dict_value(sale_order['inviter'],'wid'),'level':self.get_dict_value(sale_order,'level')
                                        ,'registerTime':self.get_dict_value(sale_order,'registerTime'),'scrollId':self.get_dict_value(sale_order,'scrollId')
                                        ,'state':self.get_dict_value(sale_order,'state'),'wid':self.get_dict_value(sale_order,'wid')})
        self.save_as_csv_create(data=sale_order_table, file_name='./Data/merchant_weike_list')

    # 获取微客的基本信息
    def get_weike_detail(self, access_token):
        url = 'https://dopen.weimob.com/api/1_0/newsdp/weike/getWeike?accesstoken={0}'.format(access_token)
        print("客户详情接口url：" + url)
        mc = MySqlClient(154, 'spider')
        orderNos = mc.query_sql_list(
            """	SELECT
                    wid
                from 
                    spider.weimeng_merchant_weike_list""", 'wid')

        print("需要获取" + str(len(orderNos)) + "个订单信息")
        print(orderNos)
        member_table = []
        i = 0
        for orderNo in orderNos:
            try:
                i = i + 1
                print("开始第" + str(i) + "次请求" + str(orderNo) + "微客的数据")
                data = json.dumps({
                    "wid": orderNo
                })
                res = requests.post(url, data).json()
                # 获取会员数据
                members = res['data']
                member = {}
                # 获取只需要的字段
                for item in dict(members).keys():
                    if item != "":
                        member[item] = str(members[item]).replace('\'','\"')
                member["add_time"] = now_time
                member_table.append(member)
            except requests.exceptions.SSLError:
                print('请求次数过多，重新请求')
                continue
            except requests.exceptions.ConnectionError:
                print('链接异常，重新请求')
                continue
            except TypeError:
                print('没有数据，重新请求')
                continue
            except ValueError:
                print('没有数据，重新请求')
                continue
        self.save_as_csv_create(data=member_table, file_name='./Data/weike_detail')
        mc.conn.close()

    # 获取商户分账记录列表
    def get_commission_record_list(self, access_token):
        url = 'https://dopen.weimob.com/api/1_0/newsdp/order/getCommissionRecordList?accesstoken={0}'.format(
            access_token)
        print("客户详情接口url：" + url)
        mc = MySqlClient(154, 'spider')
        orders = mc.query_sql_lists(
            """	SELECT
                merchantinfo,
                orderno
            from 
                weimeng_sale_order_detail""")

        for order in orders:
            storeid = eval(order['merchantinfo'])['storeId']
            orderid = order['orderno']
        member_table = []
        i = 0
        # for orderNo in orderNos:
        #     try:
        #         i = i + 1
        #         print("开始第"+str(i)+"次请求" + str(orderNo) + "订单的数据")
        #         data = json.dumps({
        #             "orderNo": orderNo
        #         })
        #         res = requests.post(url, data).json()
        #         # 获取会员数据
        #         members = res['data']
        #         member = {}
        #         # 获取只需要的字段
        #         for item in dict(members).keys():
        #             if item != "":
        #                 member[item] = str(members[item])
        #         member["add_time"] = now_time
        #         member_table.append(member)
        #     except requests.exceptions.SSLError:
        #         print('请求次数过多，重新请求')
        #         break
        #     except requests.exceptions.ConnectionError:
        #         print('链接异常，重新请求')
        #         break
        # self.save_as_csv_create(data=member_table, file_name='./Data/order_detail')
        # mc.conn.close()

    # 获取门店库存列表
    # http://yun.weimob.com/saas/word/detailApi.html?tag=282&menuId=1&id=550
    def get_store_stock_list(self, access_token):
        sale_order_table = []
        i = 0
        while True:
            i = i + 1
            data = {
                "pageNum": i,
                "pageSize": 500,
                "queryParameter": {
                    "searchType": 0,
                    "type": 1
                }
            }
            data_json = json.dumps(data)
            print(data_json)
            response = requests.post(
                'https://dopen.weimob.com/api/1_0/ec/stock/queryStoreStockListWithPage?accesstoken={}'.format(
                    access_token), data=data_json).json()
            sale_orders = response["data"]["pageList"]
            if sale_orders == []:
                print("数据全部请求完成")
                break
            for sale_order in sale_orders:
                sale_order_dict = {}
                for item in dict(sale_order).keys():
                    if item != "":
                        sale_order_dict[item] = str(sale_order[item]).replace('\'','\"')
                sale_order_dict["add_time"] = now_time
                sale_order_table.append(sale_order_dict)
        self.save_as_csv_create(data=sale_order_table, file_name='./Data/store_stock_list')

    # 获取微客的客户列表
    def get_weike_invite_user_list(self, access_token):
        url = 'https://dopen.weimob.com/api/1_0/newsdp/weike/getInvitedMemberList?accesstoken={0}'.format(access_token)
        print("客户详情接口url：" + url)
        mc = MySqlClient(154, 'spider')
        wids = mc.query_sql_list(
            """SELECT
                    wid
                from 
                    weimeng_merchant_weike_list;""", 'wid')

        print("需要获取" + str(len(wids)) + "个用户信息")
        member_table = []
        # 读取非会员
        for wid in wids:
            i = 0
            try:
                while True:
                    i = i + 1
                    # print("开始第" + str(i) + "次请求" + str(wid) + "用户的数据")
                    data = json.dumps({
                        "pageNum": i,
                        "pageSize": 20,
                        "queryParameter": {
                            "wid": wid
                        }
                    })
                    res = requests.post(url, data).json()
                    print(res)
                    # 获取会员数据
                    members = res['data']['pageList']
                    if members == []:
                        print("当前用户"+wid+"数据请求完成")
                        break
                    for member in members:
                        user_wid = member['wid']
                        applyTime = member['applyTime']
                        add_time = now_time
                        member_table.append({'wid':user_wid,'applyTime':applyTime,'add_time':add_time,'weike_wid':wid})
            except requests.exceptions.SSLError:
                print('请求次数过多，重新请求')
                continue
            except requests.exceptions.ConnectionError:
                print('链接异常，重新请求')
                continue
            except TypeError:
                print('没有数据，重新请求')
                continue
            except ValueError:
                print('没有数据，重新请求')
                continue
        self.save_as_csv_create(data=member_table, file_name='./Data/weike_invite_user_list')

    # 获取产品列表
    # http://yun.weimob.com/saas/word/detailApi.html?tag=281&menuId=1&id=347
    def get_goods_list(self, access_token):
        # member_table = []
        url = 'https://dopen.weimob.com/api/1_0/ec/goods/queryGoodsList?accesstoken={0}'.format(access_token)
        print("会员列表列接口url：" + url)
        i = 0
        # 循环获取
        table = []
        while True:
            i = i+1
            data = {
                "pageNum": i,
                "pageSize": 100
            }
            json_data = json.dumps(data)
            res = requests.post(url=url, data=json_data).json()
            print("第" + str(i) + "次请求")

            # 获取会员数据
            datas = res['data']['pageList']
            if datas == []:
                print("数据全部请求完成")
                break
            for data in datas:
                table.append({'add_time':now_time,'goodsId': self.get_dict_value(data,'goodsId'),'title': self.get_dict_value(data,'title'),'maxPrice': self.get_dict_value(data,'maxPrice'),'minPrice': self.get_dict_value(data,'minPrice'),'avaliableStockNum': self.get_dict_value(data,'avaliableStockNum'),'defaultImageUrl': self.get_dict_value(data,'defaultImageUrl'),'salesNum': self.get_dict_value(data,'salesNum'),'putAwayDate': self.get_dict_value(data,'putAwayDate'),'isPutAway': self.get_dict_value(data,'isPutAway'),'isMultiSku': self.get_dict_value(data,'isMultiSku'),'sortNum': self.get_dict_value(data,'sortNum'),'isExistEmptyStock': self.get_dict_value(data,'isExistEmptyStock'),'isAllStockEmpty': self.get_dict_value(data,'isAllStockEmpty'),'isCanSell': self.get_dict_value(data,'isCanSell'),'sellModelType': self.get_dict_value(data,'sellModelType'),'isPreSell': self.get_dict_value(data,'isPreSell')})
        self.save_as_csv_create(data=table, file_name='./Data/goods_list')

    # 获取产品明细
    # http://yun.weimob.com/saas/word/detailApi.html?tag=281&menuId=1&id=1274
    def get_goods_detail(self, access_token):
        url = 'https://dopen.weimob.com/api/1_0/ec/retailGoods/queryGoodsDetail?accesstoken={0}'.format(access_token)
        print("客户详情接口url：" + url)
        mc = MySqlClient(154, 'spider')
        items = mc.query_sql_list(
            """SELECT
                goodsId
            from weimeng_goods_list""", 'goodsId')

        print("需要获取" + str(len(items)) + "个信息")
        table = []
        i = 0
        for item in items:
            try:
                i = i + 1
                print("开始第" + str(i) + "次请求")
                data = json.dumps({
                    "goodsId": item
                })
                res = requests.post(url, data).json()
                data = res['data']['goods']
                table.append({'add_time':now_time,'storeId':res['data']['storeId'],'goodsId': self.get_dict_value(data,'goodsId'),'title': self.get_dict_value(data,'title'),'outerGoodsCode': self.get_dict_value(data,'outerGoodsCode'),'isMultiSku': self.get_dict_value(data,'isMultiSku'),'goodsImageUrl': self.get_dict_value(data,'goodsImageUrl'),'defaultImageUrl': self.get_dict_value(data,'defaultImageUrl'),'goodsDesc': self.get_dict_value(data,'goodsDesc'),'deductStockType': self.get_dict_value(data,'deductStockType'),'isPutAway': self.get_dict_value(data,'isPutAway'),'sort': self.get_dict_value(data,'sort'),'isMemberShipDiscount': self.get_dict_value(data,'isMemberShipDiscount'),'categoryList': self.get_dict_value(data,'categoryList'),'selectedSaleAttrList': self.get_dict_value(data,'selectedSaleAttrList'),'selectedGoodsAttrList': self.get_dict_value(data,'selectedGoodsAttrList'),'selectedSaleAttrIdList': self.get_dict_value(data,'selectedSaleAttrIdList'),'selectedClassifyList': self.get_dict_value(data,'selectedClassifyList'),'selectedTag': self.get_dict_value(data,'selectedTag'),'b2cGoods': self.get_dict_value(data,'b2cGoods'),'skuList': self.get_dict_value(data,'skuList'),'initialSales': self.get_dict_value(data,'initialSales'),'isCanSell': self.get_dict_value(data,'isCanSell'),'sellModelType': self.get_dict_value(data,'sellModelType'),'isPreSell': self.get_dict_value(data,'isPreSell')})
            except requests.exceptions.SSLError:
                print('请求次数过多，重新请求')
                continue
            except requests.exceptions.ConnectionError:
                print('链接异常，重新请求')
                continue
        self.save_as_csv_create(data=table, file_name='./Data/goods_detail')
        mc.conn.close()

    # 获取售后订单列表
    # http://yun.weimob.com/saas/word/detailApi.html?tag=290&menuId=1&id=378
    def get_rights_order_list(self, access_token):
        # member_table = []
        url = 'https://dopen.weimob.com/api/1_0/ec/rights/searchRightsOrderList?accesstoken={0}'.format(access_token)
        print("会员列表列接口url：" + url)
        i = 0
        # 循环获取
        table = []
        while True:
            try:
                i = i+1
                data = {
                    "pageNum": i,
                    "pageSize": 100
                }
                json_data = json.dumps(data)
                res = requests.post(url=url, data=json_data).json()
                print("第" + str(i) + "次请求")
                # 获取会员数据
                print(res)
                datas = res['data']['pageList']
                for data in datas:
                    print(data)
                    table.append({'add_time':now_time,'ecBizStoreId': self.get_dict_value(data,'ecBizStoreId'),'rightsStatusList': self.get_dict_value(data,'rightsStatusList'),'rightsType': self.get_dict_value(data,'rightsType'),'createTime': self.get_dict_value(data,'createTime'),'endTime': self.get_dict_value(data,'endTime'),'id': self.get_dict_value(data,'id'),'orderNo': self.get_dict_value(data,'orderNo'),'pageNum': self.get_dict_value(data,'pageNum'),'pageSize': self.get_dict_value(data,'pageSize'),'updateStartTime': self.get_dict_value(data,'updateStartTime'),'updateEndTime': self.get_dict_value(data,'updateEndTime')})
            except KeyError:
                print("数据全部请求完成")
                break
        self.save_as_csv_create(data=table, file_name='./Data/rights_order_list')

    # 获取售后订单详情
    # http://yun.weimob.com/saas/word/detailApi.html?tag=290&menuId=1&id=379
    def get_rights_order_detail(self, access_token):
        url = 'https://dopen.weimob.com/api/1_0/ec/rights/getRightsOrderDetail?accesstoken={0}'.format(access_token)
        print("客户详情接口url：" + url)
        mc = MySqlClient(154, 'spider')
        items = mc.query_sql_list(
            """SELECT
                id
            from weimeng_rights_order_list""", 'id')

        print("需要获取" + str(len(items)) + "个信息")
        table = []
        i = 0
        for item in items:
            try:
                i = i + 1
                print("开始第" + str(i) + "次请求")
                data = json.dumps({
                    "id": item
                })
                res = requests.post(url, data).json()
                data = res['data']['rightsInfo']
                table.append({'add_time':now_time,'pid': self.get_dict_value(data,'pid'),'wid': self.get_dict_value(data,'wid'),'deliveryInfo': self.get_dict_value(data,'deliveryInfo'),'refundAmount': self.get_dict_value(data,'refundAmount'),'refundBalance': self.get_dict_value(data,'refundBalance'),'refundPoints': self.get_dict_value(data,'refundPoints'),'rightsType': self.get_dict_value(data,'rightsType'),'rightsReason': self.get_dict_value(data,'rightsReason'),'goods': self.get_dict_value(data,'goods'),'id': self.get_dict_value(data,'id'),'paymentAmount': self.get_dict_value(data,'paymentAmount'),'refundAccountInfo': self.get_dict_value(data,'refundAccountInfo'),'refundMethod': self.get_dict_value(data,'refundMethod'),'refundPaySuccessTime': self.get_dict_value(data,'refundPaySuccessTime'),'deliveryAmount': self.get_dict_value(data,'deliveryAmount'),'orderInfo': self.get_dict_value(data,'orderInfo'),'rightsStatus': self.get_dict_value(data,'rightsStatus'),'rightsStatusName': self.get_dict_value(data,'rightsStatusName'),'channelType': self.get_dict_value(data,'channelType'),'channelTypeName': self.get_dict_value(data,'channelTypeName'),'aotuConfrimReceivedTime': self.get_dict_value(data,'aotuConfrimReceivedTime'),'autoRefundPayTime': self.get_dict_value(data,'autoRefundPayTime'),'createTime': self.get_dict_value(data,'createTime'),'flagContent': self.get_dict_value(data,'flagContent'),'paymentType': self.get_dict_value(data,'paymentType'),'paymentTypeName': self.get_dict_value(data,'paymentTypeName'),'updateTime': self.get_dict_value(data,'updateTime'),'flagRank': self.get_dict_value(data,'flagRank'),'defaultAddressType': self.get_dict_value(data,'defaultAddressType'),'defaultReturnAddress': self.get_dict_value(data,'defaultReturnAddress'),'autoHandleTime': self.get_dict_value(data,'autoHandleTime'),'usedMemberPoints': self.get_dict_value(data,'usedMemberPoints'),'balanceDeductionAmount': self.get_dict_value(data,'balanceDeductionAmount'),'pointsDiscountAmount': self.get_dict_value(data,'pointsDiscountAmount'),'autoHandleText': self.get_dict_value(data,'autoHandleText'),'agreeRightsTime': self.get_dict_value(data,'agreeRightsTime'),'returnGoodsTime': self.get_dict_value(data,'returnGoodsTime'),'confirmReceivedTime': self.get_dict_value(data,'confirmReceivedTime'),'finishTime': self.get_dict_value(data,'finishTime'),'applyAmount': self.get_dict_value(data,'applyAmount'),'storeId': self.get_dict_value(data,'storeId'),'storeTitle': self.get_dict_value(data,'storeTitle'),'processStoreId': self.get_dict_value(data,'processStoreId'),'processStoreTitle': self.get_dict_value(data,'processStoreTitle'),'headStoreId': self.get_dict_value(data,'headStoreId'),'customRightsReason': self.get_dict_value(data,'customRightsReason'),'reasonImageUrlList': self.get_dict_value(data,'reasonImageUrlList'),'refusedReason': self.get_dict_value(data,'refusedReason')})
            except requests.exceptions.SSLError:
                print('请求次数过多，重新请求')
                continue
            except requests.exceptions.ConnectionError:
                print('链接异常，重新请求')
                continue
        self.save_as_csv_create(data=table, file_name='./Data/rights_order_detail')
        mc.conn.close()

    # 获取进销存单据列表（出入库）
    # http://yun.weimob.com/saas/word/detailApi.html?tag=282&menuId=1&id=562
    def get_inventory_order_list(self, access_token):
        url = 'https://dopen.weimob.com/api/1_0/ec/stock/queryInventoryOrderListWithPage?accesstoken={0}'.format(access_token)
        print("会员列表列接口url：" + url)
        # 循环获取
        table = []
        for parentInventoryType in ['1','2']:
            i = 0
            print('============================'+parentInventoryType)
            try:
                while True:
                    i = i+1
                    data = {
                        "pageNum": i,
                        "pageSize": 20,
                        "queryParameter": {
                            "parentInventoryType": parentInventoryType
                        }
                    }
                    json_data = json.dumps(data)
                    res = requests.post(url=url, data=json_data).json()
                    print("第" + str(i) + "次请求")
                    # 获取会员数据
                    print(res)
                    datas = res['data']['pageList']
                    for data in datas:
                        print(data)
                        table.append({'add_time':now_time,'pageNum': self.get_dict_value(data,'pageNum'),'pageSize': self.get_dict_value(data,'pageSize'),'totalCount': self.get_dict_value(data,'totalCount'),'pageList': self.get_dict_value(data,'pageList'),'id': self.get_dict_value(data,'id'),'storageType': self.get_dict_value(data,'storageType'),'storageTypeName': self.get_dict_value(data,'storageTypeName'),'createTime': self.get_dict_value(data,'createTime'),'remark': self.get_dict_value(data,'remark'),'referId': self.get_dict_value(data,'referId'),'manager': self.get_dict_value(data,'manager'),'inventoryType': self.get_dict_value(data,'inventoryType')})
            except KeyError:
                print("数据全部请求完成")
                continue
            except TypeError:
                print("数据全部请求完成")
                continue
        self.save_as_csv_create(data=table, file_name='./Data/inventory_order_list')

if __name__ == '__main__':
    pass