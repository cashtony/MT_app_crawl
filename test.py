import base64
import json
import random
import re
import string
import time
import uuid
import zlib
from datetime import datetime
from pprint import pprint

import psycopg2
import requests
from sign import rest_sign

list_url = 'https://sz.meituan.com/meishi/api/poi/getPoiList?cityName=%E6%B7%B1%E5%9C%B3&cateId=11&areaId=0&sort=&dinnerCountAttrId=&page=1&userId=&uuid={uuid}&platform=1&partner=126&originUrl=https%3A%2F%2Fsz.meituan.com%2Fmeishi%2Fc11%2F&riskLevel=1&optimusCode=10&_token={token}'

# uuid = '0f0502af-a9f9-46f1-9ca7-418a1f34bb39'
_token = 'eJztVtmO4lYQ/RceeGnmcvelJRRhszRLQ0MDvUQRMmDANF7G2A3tKP+eMuvMJO95CUL4uuq4btU5Vdf8WYhbi8I9wURhUip8unHhvkAQRrJQKiQ78AhtiOSac0loqTC/2TSlVBFVKsziSa1w/zuTuCQU/SM3DOH+aJAc/1G6rSiHb45oAaCwTpJod18urwXaO57veMh3vSR1AjQP/fLJVPa9YOEefku+IrcC98E0clZucb52gsDdVvxksymmiT/dhWk8dysSM8WLy4oTLOLQWxS3TlKhFAluBOXg5BwLwYrbYFUhhCHDmTYMY6W5occ4vrvwUv/6fG5K3NivEHz8UEyLQNLOC4Np4Pgu2IGs3Joj52GQuEFS0ZIoJjDDxnBF5cnn+JHjrYJKdRWHaWQdf21cx8116Lt5UQBJ3FUYf5EpM3w6dch0Ov9GMOXFuVdhuOjvvMWvsY9aCFgTJUkxTQHBBTYc1xqGaYtQq6arVVsYXdN2g0ula9JYtRrXthJWndo1xqvMptiuCiosxg0upjs3hjjfCPTARaMwcgMn8v5NqNy1FmUoPHaCufu/VP+JVDBV/iifKsNLUoNyXJaAidz+kdvh6tz8pW7rCim1Hps5LDm6KeGIC0aoKHEtUH7N++AXMzNGEUOZpvpHhORUYKIZwYIrAHJEJGOGgIA/AzXmUqs8FgVlpaRcCaEF5HZBmBuEoOPi5BFIMk6EoIpxdnRjdGyLW3iJGCXGYCOlMlLrElcaYeBME6UVwdddJJKKY9CDHzfLgRKBOooqaqDNiDkDFaJSyLx2BSUBlGIsNbvlq5DCSoG02hxZAiCFtKi5xL7mD5lwxeSZDy4N0hyqwZiYE70XGMeYMzg1CYN8AKgQgxuuDRU/FmsQpmcmJEeKQRrsHxChGHyg1hwKZUqCuCJEYq21VJcyKQYrI+S0J8n5EJAu0ZxB94LhUgQliDCNQWaci5ZHFNAeilIBw0vyt8UVqCk3Gt4WF14EBpPGkpn8rcKuISniMOJYQ16gGjQPF0hLwwSnRwbPOTKJlKZGG3EmrMQZg6kGCyh+ZuKEVOhKPWCuRigHEjUYM4Ml/dlFJKhqYEZl3iR5ZHlhkeXCQxFGs5yz075QuzCKE3prKioRhteiurQnoBiM/qXJLlRzJOC4EMccAEWhwzAwT5hQ/Np3VKBbnwsoU1z3gFYjDE4Tcu5wQc8uDSPHT0EFQTd+FcpPIQh/yo0flbh6NaQjLg/hU9H5ifEIfwcAsIPTEFZu+ysZJ8n3g10dl9sLe/mYNaT99hL1n+muaxnnM9XPzU62zsbOpumrJbkbbVsT9+Ez9eciO2Q1i4XBSzauL9f9x7d1e5Q6oW1aJju0cWQPnx4/Bx2zaU/m3TZLNnHoPu68Sf0zW/bI1tpvcN9ajZW/eBri3o519tbdy8fT62A0JN/1wDWNSRJ6b2MnysoDnBnrMPB7TR7ETzg+PM4bQTCcNIbbZCGSZ1d1O4bFnUP8sZ2/d4fJnDx/RHgVP0zG9UN38mQ3NvWHfXaYRFFP49lssGLy4EV3i6Zcqk4tHukGq7bs6rz94D31/axXb5JBr1VLRX2Bqwuy3PT5cpkyOdk/j2Ytli7Daj9ot7TT7axmrY62h+FLoxlUjb8aE38b9cfNTT1VE9pqBl/VyLgzx9u+y163/vUasq+R5y/bs3L9Y7TpNLHzvPoov7c7iS+Ju2ei0dDlqlV1tfWWsP2+PyvX3l4fOm/lQXk300+RxIc2LXcOd+HrPlgnOHbfMzaY3W07STD5HvR0RNOMdlTGrYdtBo9VKoW//gb5QaNm'

app_waimai_sign = 'LN8U+Xv593P4s0z53Vr7a/vwvV+MymLlMK5nyERLRwGui17L6A7Lh3/AnIMwEBprBZHF2TLScn/ukfPjCF3p87/VAqsVtcJn17BaP3/yAK3JMASPEKkSnPXEqkeKnvQH07ITgyCISe5L+vSgvRJnudyTiBcFUQhirMYkPwnsDzM='

list_headers = {
'Accept': 'application/json',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'zh-CN,zh;q=0.9',
'Connection': 'keep-alive',
'Host': 'sz.meituan.com',
'Referer': 'https://sz.meituan.com/meishi/c17/',
'Sec-Fetch-Dest': 'empty',
'Sec-Fetch-Mode': 'cors',
'Sec-Fetch-Site': 'same-origin',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
}




def decode_token(token):
    print(len(token))
    # base64解码
    token_decode = base64.b64decode(token.encode())
    # 二进制解压
    token_string = zlib.decompress(token_decode)
    return token_string

token = decode_token(_token)
print(token.decode())
print(int(time.time() * 1000))

def encode_token():
    sign = rest_sign()
    ts = int(datetime.now().timestamp() * 1000)
    token_dict = {
        'rId': 100900,
        'ver': '1.0.6',
        'ts': ts,
        'cts': ts + 100 * 1000,
        'brVD': [1010, 750],
        'brR': [[1920, 1080], [1920, 1040], 24, 24],
        'bI': ['https://gz.meituan.com/meishi/c11/', ''],
        'mT': [],
        'kT': [],
        'aT': [],
        'tT': [],
        'aM': '',
        'sign': sign
    }
    # 二进制编码

    encode = str(token_dict).encode()
    # 二进制压缩
    compress = zlib.compress(encode)
    # base64编码
    b_encode = base64.b64encode(compress)
    # 转为字符串
    token = str(b_encode, encoding='utf-8')
    return token

# token = encode_token()
# print(token)
#
# response = requests.get(url=list_url.format(uuid=uuid,token=token),headers=list_headers)
# print(response.text)


# TODO  "98390690" 看会不会变
region = re.findall(r'(\w{2}区)','大冲新城花园社区97号')
print(region)

# category_dict = {}
# with open('Category.json', 'r', encoding='utf-8') as f:
#     data = f.read()
# json_data = json.loads(data)
# categories = json_data['data']['categories']
# for category in categories[1:-2]:
#     print(category)
#     first_categoryId = str(category['cateId'])
#     first_catename = category['name']
#     category_dict[first_categoryId] = first_catename
#     for subcate in category['subCate'][1:]:
#         second_categoryId = str(subcate['cateId'])
#         second_categoryname = subcate['name']
#         category_dict[second_categoryId] = second_categoryname
#         with open('cate_id.json', 'w', encoding='utf-8') as f:
#             f.write(str(category_dict))


s = '48'

s = float('%.2f' % (int(s) / 10))
print(s)

# sql = """insert into mt_wm (source_data,shopname,shopid,category_tags_l1_name,category_tags_l2_name,category_tags_l3_name,
# cityname,region,address,address_gps_long,address_gps_lat,shop_score,taste_score,pack_score,delivery_score,comments,popular_dishes,minimum_charge,mon_sales,avg_speed,business_time,
# special_offer,mark) values ('%(source_data)s','%(shopname)s','%(shopid)s','%(category_tags_l1_name)s','%(category_tags_l2_name)s',
# '%(category_tags_l3_name)s','%(cityname)s','%(region)s','%(address)s','%(address_gps_long)s','%(address_gps_lat)s','%(shop_score)f',
# %(taste_score)f,%(pack_score)f,%(delivery_score)f,'%(comments)s','%(popular_dishes)s',
# '%(minimum_charge)f','%(mon_sales)d','%(avg_speed)f','%(business_time)s','%(special_offer)s','%(mark)s')""" % kwargs

# sql2 = """
# insert into mt_wm (source_data,shopname,shopid,category_tags_l1_name,category_tags_l2_name,category_tags_l3_name,
# cityname,region,address,address_gps_long,address_gps_lat,shop_score,taste_score,pack_score,delivery_score,comments,popular_dishes,minimum_charge,mon_sales,avg_speed,business_time,
# special_offer,mark) values ('%(source_data)s','%(shopname)s','%(shopid)s','%(category_tags_l1_name)s','%(category_tags_l2_name)s',
# '%(category_tags_l3_name)s','%(cityname)s','%(region)s','%(address)s','%(address_gps_long)s','%(address_gps_lat)s','%(shop_score)f',
# %(taste_score)f,%(pack_score)f,%(delivery_score)f,'%(comments)s','%(popular_dishes)s',
# '%(minimum_charge)f','%(mon_sales)d','%(avg_speed)f','%(business_time)s','%(special_offer)s','%(mark)s')
# ON CONFLICT (shopid)
# DO UPDATE SET shop_score='%(shop_score)f',taste_score='%(taste_score)f',pack_score='%(pack_score)f',delivery_score='%(delivery_score)f',minimum_charge='%(minimum_charge)f',mon_sales='%(mon_sales)d',avg_speed='%(avg_speed)f',business_time='%(business_time)s',special_offer='%(special_offer)s',mark='%(mark)s' where shopid='%(shopid)s';
# """

conn = psycopg2.connect(database="mt_wm_test", user="postgres", password="mc930816", host="127.0.0.1", port="5432")
cur = conn.cursor()

sql = """select comments from mt_wm where shopid='856847181222725'"""
cur.execute(sql)
ret = cur.fetchone()[0]
print(json.loads(ret))