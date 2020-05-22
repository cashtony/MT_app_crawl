import json

import psycopg2
import pandas as pd

conn = psycopg2.connect(database="mt_wm_test", user="postgres", password="postgres", host="127.0.0.1", port="5432")
cur = conn.cursor()

def read_sql():
    sql = """SELECT * FROM mt_wm WHERE cityname = '深圳市' and id is not null ORDER BY update_time desc"""
    df = pd.read_sql(sql=sql,con=conn)
    return df

def pro_data(dataframe):
    for index,row in dataframe.iterrows():
        # row['comments'] = json.loads(row['comments'])
        dataframe.iloc[index,15] = str(json.loads(row['comments']))
        print(dataframe.iloc[index,15])
        break
df = read_sql()
pro_data(df)