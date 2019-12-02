# Author:Aliex ZJ
# -*- coding:utf-8 -*-
import datetime
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import pandas as pd
import pymysql
from lxml import etree
import requests

now_time = datetime.datetime.now().strftime('%Y-%m-%d')


# 获取csv网址
def getUrlList(csv_path, url_name):
    # 读取csv文件
    csv_file = open(csv_path, 'rb').read().decode('utf-8')
    # 保存地区和url
    url_list = []
    for x in csv_file.split('\r\n'):
        url_info = x.split(',')
        # 判断需要的网址
        if url_info[1] == url_name:
            url_list.append({url_info[1]: [url_info[0], url_info[2]]})

    return url_list

# 解析中国商务网1  日期-产品-规格-价格
def praseChinaBusiness1(url_list):
    table = []
    # 定义请求头
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        'cookie': 'CompNew=0; UserCount=50F+zk6pYMYaLB9DEbsmQVXIH7avJgZdFCNIlVNWP2mRuhYcc9jRJu8VOgNG54oSUkPk6IFXC90fKrXa/Ytnw0U67INIqgVL; Hm_lvt_8c905ec8d12584debce091e1b8c39fc3=1559366230,1559446331,1559693340; ASP.NET_SessionId=dktbkt55q4hhlu55tzkyky55; Hm_lvt_55f4388cb1206cf827c03a4f9ff5cbd0=1559706263,1559780001,1560042660,1560127522; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; CustInfo=50F+zk6pYMasBvSZvR0fH4yeunqew1exUNl6etVB1vPXhK00v20l/rtSxJld2EVWSE71m086t5a3wNPQWY76X+8MPmeWI1OZLCSevsnvuSBAmmuQWULJ23imk3vLCe2KkVnuiOJLNLl4Qmnctq90qBB8Z5cx6lzgkuenq2JmvYQ=; Hm_lpvt_55f4388cb1206cf827c03a4f9ff5cbd0=1560151284'
    }

    for i in range(0, len(url_list)):
        url = url_list[i]['中华商务网1'][1]
        # session接受调用cookie
        response = requests.get(url=url, headers=headers)
        context = response.text

        # 解析
        selector = etree.HTML(context)
        date = selector.xpath('//tr[@class="dmain_right_tab_list"][1]/td[1]/text()')
        name = selector.xpath('//tr[@class="dmain_right_tab_list"][1]/td[2]/text()')
        num = selector.xpath('//tr[@class="dmain_right_tab_list"][1]/td[3]/text()')
        res_name = str(name[0]) + '(' + str(num[0]) + ')'
        price = selector.xpath('//tr[@class="dmain_right_tab_list"][1]/td[4]/text()')
        table.append({'name': res_name, 'area': str(url_list[i]['中华商务网1'][0]), 'date': date[0], 'price': price[0],
                      'add_time': now_time})

    return table

# 解析中国商务网2  产品-规格-日期-价格
def praseChinaBusiness2(url_list):
    table = []
    # 定义请求头
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        'cookie': 'CompNew=0; UserCount=50F+zk6pYMYaLB9DEbsmQVXIH7avJgZdFCNIlVNWP2mRuhYcc9jRJu8VOgNG54oSUkPk6IFXC90fKrXa/Ytnw0U67INIqgVL; Hm_lvt_8c905ec8d12584debce091e1b8c39fc3=1559366230,1559446331,1559693340; ASP.NET_SessionId=dktbkt55q4hhlu55tzkyky55; Hm_lvt_55f4388cb1206cf827c03a4f9ff5cbd0=1559706263,1559780001,1560042660,1560127522; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; CustInfo=50F+zk6pYMasBvSZvR0fH4yeunqew1exUNl6etVB1vPXhK00v20l/rtSxJld2EVWSE71m086t5a3wNPQWY76X+8MPmeWI1OZLCSevsnvuSBAmmuQWULJ23imk3vLCe2KkVnuiOJLNLl4Qmnctq90qBB8Z5cx6lzgkuenq2JmvYQ=; Hm_lpvt_55f4388cb1206cf827c03a4f9ff5cbd0=1560151284'
    }

    for i in range(0, len(url_list)):
        url = url_list[i]['中华商务网2'][1]
        # session接受调用cookie
        response = requests.get(url=url, headers=headers)
        context = response.text

        # 解析
        selector = etree.HTML(context)
        date = selector.xpath('//tr[@class="dmain_right_tab_list"][1]/td[3]/text()')
        name = selector.xpath('//tr[@class="dmain_right_tab_list"][1]/td[1]/text()')
        num = selector.xpath('//tr[@class="dmain_right_tab_list"][1]/td[2]/text()')
        res_name = str(name[0]) + '(' + str(num[0]) + ')'
        price = selector.xpath('//tr[@class="dmain_right_tab_list"][1]/td[4]/text()')
        table.append({'name': res_name, 'area': str(url_list[i]['中华商务网2'][0]), 'date': date[0], 'price': price[0],
                      'add_time': now_time})

    return table

# 解析中国商务网3  产品-日期-地区-规格-价格(判断)
def praseChinaBusiness3(url_list):
    table = []
    # 定义请求头
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        'cookie': 'CompNew=0; UserCount=50F+zk6pYMYaLB9DEbsmQVXIH7avJgZdFCNIlVNWP2mRuhYcc9jRJu8VOgNG54oSUkPk6IFXC90fKrXa/Ytnw0U67INIqgVL; Hm_lvt_8c905ec8d12584debce091e1b8c39fc3=1559366230,1559446331,1559693340; ASP.NET_SessionId=dktbkt55q4hhlu55tzkyky55; Hm_lvt_55f4388cb1206cf827c03a4f9ff5cbd0=1559706263,1559780001,1560042660,1560127522; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; CustInfo=50F+zk6pYMasBvSZvR0fH4yeunqew1exUNl6etVB1vPXhK00v20l/rtSxJld2EVWSE71m086t5a3wNPQWY76X+8MPmeWI1OZLCSevsnvuSBAmmuQWULJ23imk3vLCe2KkVnuiOJLNLl4Qmnctq90qBB8Z5cx6lzgkuenq2JmvYQ=; Hm_lpvt_55f4388cb1206cf827c03a4f9ff5cbd0=1560151284'
    }

    for i in range(0, len(url_list)):
        url = url_list[i]['中华商务网3'][1]
        # session接受调用cookie
        response = requests.get(url=url, headers=headers)
        context = response.text
        selector = etree.HTML(context)
        # 解析
        for j in range(1, 3):

            date = selector.xpath('//tr[@class="dmain_right_tab_list"][{0}]/td[2]/text()'.format(j))
            name = selector.xpath('//tr[@class="dmain_right_tab_list"][{0}]/td[1]/text()'.format(j))
            num = selector.xpath('//tr[@class="dmain_right_tab_list"][{0}]/td[4]/text()'.format(j))
            area = selector.xpath('//tr[@class="dmain_right_tab_list"][{0}]/td[3]/text()'.format(j))
            res_name = str(name[0]) + '(' + str(num[0]) + ')'
            price = selector.xpath('//tr[@class="dmain_right_tab_list"][{0}]/td[5]/text()'.format(j))
            # 判断是否重复城市存在
            if area[0] == str(url_list[i]['中华商务网3'][0]):
                print(area[0])
                area_list = []
                for x in table:
                    area_list.append(x['area'])
                # print(area_list)
                # 判断是否重复城市存在
                if area[0] not in area_list:
                    table.append(
                        {'name': res_name, 'area': str(url_list[i]['中华商务网3'][0]), 'date': date[0], 'price': price[0],
                         'add_time': now_time})
            else:
                continue

    return table

# 解析中国商务网4  日期-产品-规格-地区-价格(判断)
def praseChinaBusiness4(url_list):
    table = []
    # 定义请求头
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        'cookie': 'CompNew=0; UserCount=50F+zk6pYMYaLB9DEbsmQVXIH7avJgZdFCNIlVNWP2mRuhYcc9jRJu8VOgNG54oSUkPk6IFXC90fKrXa/Ytnw0U67INIqgVL; Hm_lvt_8c905ec8d12584debce091e1b8c39fc3=1559366230,1559446331,1559693340; ASP.NET_SessionId=dktbkt55q4hhlu55tzkyky55; Hm_lvt_55f4388cb1206cf827c03a4f9ff5cbd0=1559706263,1559780001,1560042660,1560127522; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; CustInfo=50F+zk6pYMasBvSZvR0fH4yeunqew1exUNl6etVB1vPXhK00v20l/rtSxJld2EVWSE71m086t5a3wNPQWY76X+8MPmeWI1OZLCSevsnvuSBAmmuQWULJ23imk3vLCe2KkVnuiOJLNLl4Qmnctq90qBB8Z5cx6lzgkuenq2JmvYQ=; Hm_lpvt_55f4388cb1206cf827c03a4f9ff5cbd0=1560151284'
    }

    for i in range(0, len(url_list)):
        url = url_list[i]['中华商务网4'][1]
        # session接受调用cookie
        response = requests.get(url=url, headers=headers)
        context = response.text
        selector = etree.HTML(context)
        # 解析
        for j in range(1, 3):

            date = selector.xpath('//tr[@class="dmain_right_tab_list"][{0}]/td[1]/text()'.format(j))
            name = selector.xpath('//tr[@class="dmain_right_tab_list"][{0}]/td[2]/text()'.format(j))
            num = selector.xpath('//tr[@class="dmain_right_tab_list"][{0}]/td[3]/text()'.format(j))
            area = selector.xpath('//tr[@class="dmain_right_tab_list"][{0}]/td[4]/text()'.format(j))
            res_name = str(name[0]) + '(' + str(num[0]) + ')'
            price = selector.xpath('//tr[@class="dmain_right_tab_list"][{0}]/td[5]/text()'.format(j))
            if area[0][0:2] == str(url_list[i]['中华商务网4'][0]):
                table.append(
                    {'name': res_name, 'area': str(url_list[i]['中华商务网4'][0]), 'date': date[0], 'price': price[0],
                     'add_time': now_time})
            else:
                continue

    return table

# 解析中国商务网5  产品-规格-日期-价格(取第二个)
def praseChinaBusiness5(url_list):
    table = []
    # 定义请求头
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        'cookie': 'CompNew=0; UserCount=50F+zk6pYMYaLB9DEbsmQVXIH7avJgZdFCNIlVNWP2mRuhYcc9jRJu8VOgNG54oSUkPk6IFXC90fKrXa/Ytnw0U67INIqgVL; Hm_lvt_8c905ec8d12584debce091e1b8c39fc3=1559366230,1559446331,1559693340; ASP.NET_SessionId=dktbkt55q4hhlu55tzkyky55; Hm_lvt_55f4388cb1206cf827c03a4f9ff5cbd0=1559706263,1559780001,1560042660,1560127522; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; CustInfo=50F+zk6pYMasBvSZvR0fH4yeunqew1exUNl6etVB1vPXhK00v20l/rtSxJld2EVWSE71m086t5a3wNPQWY76X+8MPmeWI1OZLCSevsnvuSBAmmuQWULJ23imk3vLCe2KkVnuiOJLNLl4Qmnctq90qBB8Z5cx6lzgkuenq2JmvYQ=; Hm_lpvt_55f4388cb1206cf827c03a4f9ff5cbd0=1560151284'
    }

    for i in range(0, len(url_list)):
        url = url_list[i]['中华商务网5'][1]
        # session接受调用cookie
        response = requests.get(url=url, headers=headers)
        context = response.text

        # 解析
        selector = etree.HTML(context)
        date = selector.xpath('//tr[@class="dmain_right_tab_list"][2]/td[3]/text()')
        name = selector.xpath('//tr[@class="dmain_right_tab_list"][2]/td[1]/text()')
        num = selector.xpath('//tr[@class="dmain_right_tab_list"][2]/td[2]/text()')
        res_name = str(name[0]) + '(' + str(num[0]) + ')'
        price = selector.xpath('//tr[@class="dmain_right_tab_list"][2]/td[4]/text()')
        table.append({'name': res_name, 'area': str(url_list[i]['中华商务网5'][0]), 'date': date[0], 'price': price[0],
                      'add_time': now_time})

    return table

# 解析上海有色网
def praseShangHaiYouSe(url_list):
    # 保存表数据
    table = []

    # 定义请求头
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0',
        'cookie': 'SMM_device_id=223c8667-1512-582b-87ff-eb162aa2e3e4; SMM_session_id=e24de27d-b7dc-559f-9dfb-8f0892bd9934; SMM_session_start_timestamp=1566432783777; Hm_lvt_9734b08ecbd8cf54011e088b00686939=1566432784; Hm_lpvt_9734b08ecbd8cf54011e088b00686939=1566433111; SMM_auth_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjZWxscGhvbmUiOiIxMzYxNjY4MzM1MCIsImNvbXBhbnlfaWQiOjAsImNvbXBhbnlfc3RhdHVzIjowLCJjcmVhdGVfYXQiOjE1NjY0MzMwOTksImVtYWlsIjoia2FpamlhbmcudGFvQGNoaW5heGluemhpLmNvbSIsImVuX2VuZF90aW1lIjowLCJlbl9yZWdpc3Rlcl9zdGVwIjoxLCJlbl9yZWdpc3Rlcl90aW1lIjowLCJlbl9zdGFydF90aW1lIjowLCJlbl91c2VyX3R5cGUiOjAsImVuZF90aW1lIjoxNTgyNzMyNzk5LCJpc19tYWlsIjowLCJpc19waG9uZSI6MSwibGFuZ3VhZ2UiOiIiLCJseV9lbmRfdGltZSI6MCwibHlfc3RhcnRfdGltZSI6MCwibHlfdXNlcl90eXBlIjowLCJyZWdpc3Rlcl90aW1lIjoxMzYyMDE5NTYyLCJzdGFydF90aW1lIjoxNTE5NTc0NDAwLCJ1c2VyX2lkIjo0MTE1OTcsInVzZXJfbmFtZSI6InhpbnpoaWRpYW5qaTAyIiwidXNlcl90eXBlIjoyLCJ1dWlkX3NoYTI1NiI6ImNkZjRhMDA3ZTJiMDJhMGM0OWZjOWI3Y2NmYmI4YTEwYzY0NGY2MzVlMTc2NWRjZjJhN2FiNzk0ZGRjN2VkYWMiLCJ6eF9lbmRfdGltZSI6MCwienhfc3RhcnRfdGltZSI6MCwienhfdXNlcl90eXBlIjowfQ.QA9Zhr8sezkTSLerMIcLEstV0LEE_esnHlrDz_wOpeA; referer_code=https%3A%2F%2Fhq.smm.cn%2Ftong%2Fcategory%2F201102250376'
    }

    for i in range(0, len(url_list)):
        # 请求的网址
        url = url_list[i]['上海有色网'][1]

        # session接受调用cookie
        response = requests.get(url=url, headers=headers)
        context = response.text

        # 解析
        selector = etree.HTML(context)
        name = selector.xpath('/html/body/div[1]/div[2]/div[1]/div/div[1]/div/div[1]/div/p[1]/text()')[0]
        name = name.replace('\r','').replace('\n','').replace(' ','')
        date = selector.xpath('/html/body/div[1]/div[2]/div[1]/div/div[3]/div[2]/ul/table/tbody/tr[1]/td[1]/text()')
        price = selector.xpath('/html/body/div[1]/div[2]/div[1]/div/div[3]/div[2]/ul/table/tbody/tr[1]/td[3]/text()')
        price = (str(price[0]).replace('\n','').replace('\r','').replace(' ',''))

        # 保存数据
        table.append({'name': name, 'area': str(url_list[i]['上海有色网'][0]), 'date': date[0], 'price':price,
                      'add_time': now_time})

    return table

# 解析微信买塑网
def praseMaiSu():
    # 保存表数据
    table = []
    timeout=2
    option = webdriver.ChromeOptions()
    # option.add_argument('headless')
    # 要换成适应自己操作系统的chromedriver
    driver = webdriver.Chrome(executable_path='../chromedriver.exe',chrome_options=option)
    # option.add_argument('headless')

    index = 250
    while True :
        url = 'https://weixin.sogou.com/weixin?type=2&s_from=input&query=买塑观察 第{}期'.format(index)
        driver.get(url)
        index = index-1

        # 模拟点击“搜索”
        try:
            search_button = WebDriverWait(driver, timeout).until(
                lambda d: d.find_element_by_xpath('//a[@id="sogou_vr_11002601_title_0"]'))
            search_button.click()
        except BaseException:
            print('当前网页数据不匹配')
            continue

        driver.close()

        # 切换页面右边
        window_handles = driver.window_handles
        driver.switch_to.window(window_handles[-1])
        # print(driver.page_source)
        xpath_date = etree.HTML(driver.page_source)

        print('当前的期数为：'+str(index+1))
        qi_key = ''
        try:
            qi_key = xpath_date.xpath('//div[@id="js_content"]/section[1]/section/section/p[2]/strong/span[1]/text()')[0]
        except IndexError:
            print('当前网页数据不匹配')
            continue

        print('实际期数：'+qi_key)
        if int(index+1) == int(qi_key):
            xpath_date = etree.HTML(driver.page_source)
            name = 'ABS'+'('+str(xpath_date.xpath('//div[@id="js_content"]/table[14]/tbody/tr/td[1]/span/strong/text()')[0])+')'
            area = xpath_date.xpath('//*[@id="js_content"]/table[14]/tbody/tr/td[2]/span/text()')[0]
            price = xpath_date.xpath('//*[@id="js_content"]/table[14]/tbody/tr/td[3]/span/text()')[0]
            price = price.replace(',','')
            table.append({'name': name, 'area': area, 'date': now_time, 'price': price,'add_time': now_time})

            xpath_date = etree.HTML(driver.page_source)
            name = 'PC'+'('+str(xpath_date.xpath('//*[@id="js_content"]/table[23]/tbody/tr/td[1]/span/strong/text()')[0])+')'
            area = xpath_date.xpath('//*[@id="js_content"]/table[23]/tbody/tr/td[2]/span/text()')[0]
            price = xpath_date.xpath('//*[@id="js_content"]/table[23]/tbody/tr/td[3]/span/text()')[0]
            price = price.replace(',', '')
            table.append({'name': name, 'area': area, 'date': now_time, 'price': price,'add_time': now_time})

            driver.quit()
            break
        else:
            print('当前网页数据不匹配')
            continue
    return table


# 保存csv格式
def saveAsCsv(data, name):
    df = pd.DataFrame(data)
    df.to_csv('./Data/{0}.csv'.format(name), sep=',', header=True, index=False, encoding='utf-8')
    print('{0}.csv'.format(name)+"保存成功")

# 保存数据到mysql
def saveToMysql(data):
    config = dict(host='10.149.1.154', user='root', password='root',
                  cursorclass=pymysql.cursors.DictCursor)
    # 建立连接
    conn = pymysql.Connect(**config)
    print(conn)
    # 自动确认commit True
    conn.autocommit(1)
    # 设置光标
    cursor = conn.cursor()

    def make_table_sql(df):
        columns = df.columns.tolist()
        types = df.ftypes
        # 添加id 制动递增主键模式
        make_table = []
        for item in columns:
            if 'int' in types[item]:
                char = item + ' BIGINT'
            elif 'float' in types[item]:
                char = item + ' FLOAT'
            elif 'object' in types[item]:
                char = item + ' VARCHAR(255)'
            elif 'datetime' in types[item]:
                char = item + ' DATETIME'
            make_table.append(char)
        return ','.join(make_table)

    def csv2mysql(db_name, table_name, df):
        # 创建database
        # cursor.execute('CREATE DATABASE IF NOT EXISTS {}'.format(db_name))
        # 选择连接database
        conn.select_db(db_name)
        # 创建table
        # cursor.execute('DROP TABLE IF EXISTS {}'.format(table_name))
        # cursor.execute('CREATE TABLE {}({})'.format(table_name,make_table_sql(df)))
        # 删除今日数据
        truncate_sql = 'DELETE FROM {0} where add_time={1}'.format(table_name, "\"" + now_time + "\"")
        cursor.execute(truncate_sql)
        # 提取数据转list 这里有与pandas时间模式无法写入因此换成str 此时mysql上格式已经设置完成
        # df['日期'] = df['日期'].astype('str')
        values = df.values.tolist()
        # 根据columns个数
        s = ','.join(['%s' for _ in range(len(df.columns))])
        # executemany批量操作 插入数据 批量操作比逐个操作速度快很多
        cursor.executemany('INSERT INTO {} VALUES ({})'.format(table_name, s), values)

    csv2mysql('test', 'RawPrice', data)
    conn.close()


if __name__ == '__main__':
    # 获取中华商务网1
    chinaBusinessUrl = getUrlList('./Data/RawUrl.csv', '中华商务网1')
    try:
        chinaBusinessUrlData1 = praseChinaBusiness1(chinaBusinessUrl)
    except IndexError:
        print("Error: 没有找到网页内容")
    else:
        saveAsCsv(praseChinaBusiness1(chinaBusinessUrl), '1')
        print("网页正常")

    # 获取中华商务网2
    chinaBusinessUrl = getUrlList('./Data/RawUrl.csv', '中华商务网2')
    try:
        chinaBusinessUrlData2 = praseChinaBusiness2(chinaBusinessUrl)
    except IndexError:
        print("Error: 没有找到网页内容")
    else:
        saveAsCsv(praseChinaBusiness2(chinaBusinessUrl), '2')
        print("网页正常")

    # 获取中华商务网3
    chinaBusinessUrl = getUrlList('./Data/RawUrl.csv', '中华商务网3')
    try:
        chinaBusinessUrlData3 = praseChinaBusiness3(chinaBusinessUrl)
    except IndexError:
        print("Error: 没有找到网页内容")
    else:
        saveAsCsv(praseChinaBusiness3(chinaBusinessUrl), '3')
        print("网页正常")

    # 获取中华商务网4
    chinaBusinessUrl = getUrlList('./Data/RawUrl.csv', '中华商务网4')
    try:
        chinaBusinessUrlData4 = praseChinaBusiness4(chinaBusinessUrl)
    except IndexError:
        print("Error: 没有找到网页内容")
    else:
        saveAsCsv(praseChinaBusiness4(chinaBusinessUrl), '4')
        print("网页正常")

    # 获取中华商务网5
    chinaBusinessUrl = getUrlList('./Data/RawUrl.csv', '中华商务网5')
    try:
        chinaBusinessUrlData5 = praseChinaBusiness5(chinaBusinessUrl)
    except IndexError:
        print("Error: 没有找到网页内容")
    else:
        saveAsCsv(praseChinaBusiness5(chinaBusinessUrl), '5')
        print("网页正常")

    # 获取微信买塑网
    saveAsCsv(praseMaiSu(), '6')

    # 获取上海有色网url
    shangHaiYouSeUrl = getUrlList('./Data/RawUrl.csv', '上海有色网')
    shangHaiYouSeData = praseShangHaiYouSe(shangHaiYouSeUrl)
    saveAsCsv(shangHaiYouSeData, '7')

    data1 = pd.read_csv('./Data/1.csv')
    data2 = pd.read_csv('./Data/2.csv')
    data3 = pd.read_csv('./Data/3.csv')
    data4 = pd.read_csv('./Data/4.csv')
    data5 = pd.read_csv('./Data/5.csv')
    data6 = pd.read_csv('./Data/6.csv')
    data7 = pd.read_csv('./Data/7.csv')

    # 取数据交集
    data_1 = pd.merge(data1, data2, how='outer')
    data_2 = pd.merge(data_1, data3, how='outer')
    data_3 = pd.merge(data_2, data4, how='outer')
    data_4 = pd.merge(data_3, data5, how='outer')
    data_5 = pd.merge(data_4, data6, how='outer')
    data_6 = pd.merge(data_5, data7, how='outer')

    print(data_6)
    # 保存mysql
    saveToMysql(data_6)
