# 跳转商品url，获取详细信息
import re

import requests
from lxml import etree

# prod_url = 'https://detail.tmall.com/item.htm?id=549336345697&skuId=4420505890561&user_id=2089984249&cat_id=2&is_b=1&rn=9887b9e2481fde30c5996be4174c070d'
# shop_response = requests.get(prod_url).text
# selector = etree.HTML(shop_response)
# shop_items = selector.xpath('//*[@id="J_AttrUL"]/li')
# # 详细信息
# shop_list = []
# for shop_item in shop_items:
#     shop_list.append(shop_item.xpath('./text()')[0].replace('\xa0', ''))
# print("产品信息：" + str(shop_list))

