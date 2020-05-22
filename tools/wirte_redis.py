#coding:utf-8
import pandas as pd
from redis import Redis
redis_cli = Redis(host='10.101.0.239',password='abc123',decode_responses=True)

def csv_to_redis():
    filepath = 'D:/work/geohash1.csv'
    df = pd.read_csv(filepath,encoding='gbk')
    for ind,row in df.iterrows():
        if row['city'] == "昆明市":
            row['city'] = "114"
        elif row['city'] == "广州市":
            row['city'] = "20"
        elif row['city'] == "北京市":
            row['city'] = "1"
        elif row['city'] == "上海市":
            row['city'] = "10"
        elif row['city'] == "杭州市":
            row['city'] = "50"
        elif row['city'] == "成都市":
            row['city'] = "59"
        elif row['city'] == "南京市":
            row['city'] = "55"
        elif row['city'] == "郑州市":
            row['city'] = "73"
        elif row['city'] == "西安市":
            row['city'] = "42"
        elif row['city'] == "苏州市":
            row['city'] = "80"
        elif row['city'] == "青岛市":
            row['city'] = "60"
        elif row['city'] == "宁波市":
            row['city'] = "51"
        elif row['city'] == "武汉市":
            row['city'] = "57"
        elif row['city'] == "长沙市":
            row['city'] = "70"
        elif row['city'] == "沈阳市":
            row['city'] = "66"
        elif row['city'] == "重庆市":
            row['city'] = "45"
        elif row['city'] == "东莞市":
            row['city'] = "91"
        elif row['city'] == "天津市":
            row['city'] = "40"
        elif row['city'] == "深圳市":
            row['city'] = "30"
        if row['city'] == "40" or row['city'] == "1" or row['city'] == "10":
            row['longtitude'] = int(float(row['longtitude']) * 1000000)
            row['latitude'] = int(float(row['latitude']) * 1000000)
            print(row['city'], row['longtitude'], row['latitude'])
            redis_str = row['city'] + ',' + str(row['longtitude']) + ',' + str(row['latitude'])
            # redis_cli.sadd('wm_site2', redis_str)
            with open('wm_redis.txt','a',encoding='utf-8') as f:
                f.write(redis_str + '\n')

def redis_to_txt():
    while redis_cli.scard('filter_poi') > 0:
        redis_str = redis_cli.spop('filter_poi')
        with open('filter_poi.txt', 'a', encoding='utf-8') as f: #17447
            f.write(redis_str + '\n')
        redis_cli.sadd('filter_poi2',redis_str)
        print(redis_str)

# redis_to_txt()

# print(type(redis_cli.scard('wm_site')))

def txt_to_redis(filename):
    redis_name = filename
    with open(filename + '.txt','r',encoding='utf-8') as f:
        content = f.read().split('\n')
    for i in content:
        print(i)
        redis_cli.sadd(redis_name,i)

txt_to_redis('filter_poi')