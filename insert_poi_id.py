import json

import pandas as pd
import psycopg2
from sqlalchemy import create_engine
from io import StringIO
conn = psycopg2.connect(database="mt_wm_test", user="postgres", password="mc930816", host="127.0.0.1", port="5432")
cur = conn.cursor()
# db_url = "postgresql://postgres:mc930816@localhost:5432/mt_wm_test"
# engine = create_engine(db_url)
# types = {'source_data':str,'shopname':str,'url':str,'shopid':str}
# dataframe = pd.read_csv('D:/work/wm_mt.csv',encoding='gbk',dtype=types)
# # dataframe['source_data'] = ''
# # dataframe['shopid'] = dataframe['shopid'].map(lambda x:str(x))
# # dataframe = dataframe.iloc[1]
# print(dataframe)
# # # dataframe类型转换为IO缓冲区中的str类型
# # output = StringIO()
# # dataframe.to_csv(output, sep='\t', index=False, header=False)
# # output1 = output.getvalue()
#
# cur = conn.cursor()
# cur.copy_from(StringIO(output1), 'mt_wm')

# dataframe.to_sql('mt_wm', engine, index = False, if_exists='append')#增量入库



import csv
with open('D:/work/wm_mt2.csv','r') as f:
    reader = csv.reader(f)
    num = 0
    for i in reader:
        if num == 0:
            num += 1
            continue
        try:
            kwargs = {}
            kwargs['source_data'] = '美团'
            kwargs['shopname'] = i[1].replace("'",'‘')
            kwargs['url'] = i[2]
            kwargs['shopid'] = str(i[3]).replace(' ','')
            kwargs['category_tags_l1_name'] = '美食'
            kwargs['category_tags_l2_name'] = eval(i[5])[0] if i[5] != '' else '美食'
            kwargs['category_tags_l3_name'] = eval(i[6])[0] if i[6] != '' else '美食'
            kwargs['cityname'] = i[7]
            kwargs['region'] = i[8]
            kwargs['address'] = i[9].replace("'",'')
            kwargs['address_gps_long'] = eval(i[-1])['lon'] if i[-1] != '' else 0
            kwargs['address_gps_lat'] = eval(i[-1])['lat'] if i[-1] != '' else 0
            kwargs['shop_score'] = float(i[12]) if i[12] != '' else 0
            kwargs['taste_score'] = float(i[13]) if i[13] != '' else 0
            kwargs['pack_score'] = 0
            kwargs['delivery_score'] = 0
            kwargs['comments'] = ''
            kwargs['popular_dishes'] = ''
            kwargs['minimum_charge'] = float(i[18]) if i[18] != '' else 0
            kwargs['mon_sales'] = float(i[19]) if i[19] != '' else 0
            kwargs['avg_speed'] = float(i[20]) if i[20] != '' else 0
            kwargs['business_time'] = json.dumps(i[21].replace("'",""))
            kwargs['special_offer'] = json.dumps(i[22].replace("'",''))
            kwargs['mark'] = ''
        except:
            continue



        sql = """insert into mt_wm (source_data,shopname,shopid,category_tags_l1_name,category_tags_l2_name,category_tags_l3_name,
        cityname,region,address,address_gps_long,address_gps_lat,shop_score,taste_score,pack_score,delivery_score,comments,popular_dishes,minimum_charge,mon_sales,avg_speed,business_time,
        special_offer,mark) values ('%(source_data)s','%(shopname)s','%(shopid)s','%(category_tags_l1_name)s','%(category_tags_l2_name)s',
        '%(category_tags_l3_name)s','%(cityname)s','%(region)s','%(address)s','%(address_gps_long)s','%(address_gps_lat)s','%(shop_score)f',
        %(taste_score)f,%(pack_score)f,%(delivery_score)f,'%(comments)s','%(popular_dishes)s',
        '%(minimum_charge)f','%(mon_sales)d','%(avg_speed)f','%(business_time)s','%(special_offer)s','%(mark)s')
        ON CONFLICT (shopid)
        DO UPDATE SET cityname='%(cityname)s',region='%(region)s',shop_score='%(shop_score)f',taste_score='%(taste_score)f',pack_score='%(pack_score)f',delivery_score='%(delivery_score)f',minimum_charge='%(minimum_charge)f',mon_sales='%(mon_sales)d',avg_speed='%(avg_speed)f',business_time='%(business_time)s',special_offer='%(special_offer)s',mark='%(mark)s';
        """ % kwargs
        print(sql)
        cur.execute(sql)
        conn.commit()
