#coding:utf-8
import copy
import hashlib
from multiprocessing import Process
import random
import re
from datetime import datetime
from pprint import pprint
from time import time, sleep
from threading import Thread
import psycopg2
import requests
import json
from redis import Redis
from proxy import abuyun,taiyang_proxy
import logging
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

logging.basicConfig(level=logging.ERROR,
                    format="%(asctime)s %(name)s %(levelname)s %(message)s",
                    datefmt = '%Y-%m-%d  %H:%M:%S %a',    #注意月份和天数不要搞乱了，这里的格式化符与time模块相同
                    filename='wm_spider.log',
                    filemode='a'
                    )

# 线上
# redis_name = 'wm_redis'
# 本地
redis_name = 'wm_site2'
redis_filter_name = 'filter_poi'
# 线上
# conn = psycopg2.connect(database="crawler", user="root", password="9TTjkHY^Y#UeLORZ", host="10.101.0.90", port="8635")
# 本地
conn = psycopg2.connect(database="mt_wm_test", user="postgres", password="postgres", host="localhost", port="8635")

cur = conn.cursor()
# 线上
# redis = Redis(host='10.101.0.239',password='abc123',decode_responses=True)
# 本地
redis = Redis(decode_responses=True)
class WM_Spider:
    def __init__(self,lat,lng,city_id='30'):
        self.page = 1
        self.city = city_id
        self.lat = lat
        self.lng = lng
        self.proxy = taiyang_proxy()
        self.index_url = 'https://i.waimai.meituan.com/openh5'
        self.headers = {
            'Host': 'i.waimai.meituan.com',
            'Accept': 'application/json',
            'Origin': 'https://h5.waimai.meituan.com',
            # 'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; Redmi Note 3 Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.91 Mobile Safari/537.36 TitansX/11.19.6 KNB/1.2.0 android/6.0.1 mt/com.sankuai.meituan/10.0.202 App/10120/10.0.202 MeituanGroup/10.0.202',
            'User-Agent': 'AiMeiTuan /Meizu-5.1-MX4-1920x1152-480-10.8.404-1000080404-862095026057122-meizu4',
            'Referer': 'https://h5.waimai.meituan.com/waimai/mindex/menu?dpShopId=&mtShopId=1112840116809435&utm_source=wandoujia&channel=mtjj&source=shoplist&initialLat=22.544568&initialLng=113.949059&actualLat=22.544568&actualLng=113.949059',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,en-US;q=0.9',
            'Cookie':f'cityid={city_id}; network=wifi; utm_source=meizu4; utm_medium=android; utm_term=1000000202; utm_content=862095026057122; utm_campaign=AgroupBgroupC0E0Ghomepage_category1_394__a1__c-1024__e84675; wm_order_channel=mtjj; au_trace_key_net=default; openh5_uuid=E1BD0ABE0A4A8F012F3E7C3D393E13D4598E05C2BFE038A1F57A72FD44F391FC; uuid=E1BD0ABE0A4A8F012F3E7C3D393E13D4598E05C2BFE038A1F57A72FD44F391FC; service-off=0; terminal=i; w_actual_lat={self.lat}; w_actual_lng={self.lng}; openh5_uuid=E1BD0ABE0A4A8F012F3E7C3D393E13D4598E05C2BFE038A1F57A72FD44F391FC',
            'X-Requested-With': 'com.sankuai.meituan',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Connection': 'keep-alive',
        }

    # 'https://i.waimai.meituan.com/openh5/channel/kingkongshoplist?_=1589286163907'
    def request_list_from_category(self,firstCategoryId,secondCategoryId,page,last_url='/channel/kingkongshoplist'):

        kwargs = {
            'startIndex': str(int(page) - 1),
            'firstCategoryId':firstCategoryId,
            'secondCategoryId':secondCategoryId,
            'wm_actual_latitude':self.lat,
            'wm_actual_longitude':self.lng
        }
        payload = 'startIndex={startIndex}&sortId=&navigateType=910&firstCategoryId={firstCategoryId}&secondCategoryId={secondCategoryId}&geoType=2&rankTraceId=&uuid=E1BD0ABE0A4A8F012F3E7C3D393E13D4598E05C2BFE038A1F57A72FD44F391FC&platform=3&partner=4&riskLevel=71&optimusCode=10&wm_actual_latitude={wm_actual_latitude}&wm_actual_longitude={wm_actual_longitude}&openh5_uuid=E1BD0ABE0A4A8F012F3E7C3D393E13D4598E05C2BFE038A1F57A72FD44F391FC'.format_map(kwargs)

        url = self.index_url + last_url + '?_=' + str(int(time() * 1000))
        # print('列表页----')
        # print(url)
        # print(self.headers['Cookie'])
        # print(payload)
        response_json = self.post_request(url,self.headers,payload)
        return response_json

    # 'https://i.waimai.meituan.com/openh5/poi/food?_=1589277696918'
    def request_detail_food(self,poi_id,last_url='/poi/food'):
        headers = copy.deepcopy(self.headers)
        headers['Cookie'] = f'cityid={self.city}; network=wifi; utm_source=meizu4; utm_medium=android; utm_term=1000000202; utm_content=862095026057122; utm_campaign=AgroupBgroupC0E0Ghomepage_category1_394__a1__c-1024; wm_order_channel=mtjj; au_trace_key_net=default; _lx_utm=utm_source%3D60374%26utm_medium%3Dandroid%26utm_term%3D1000000202%26utm_content%3D862095026057122%26utm_campaign%3DAgroupBgroupC0E0Ghomepage_category1_394__a1__c-1024; _lxsdk_cuid=1725440c0da2-08336aca1-5a10162d-3c000-1725440c0dc62; _lxsdk_s=1725440c0e0-f28-0db-5e0%7C-1%7CNaN; _lxsdk=E1BD0ABE0A4A8F012F3E7C3D393E13D4598E05C2BFE038A1F57A72FD44F391FC; _lxsdk_unoinid=0ca77ead48c848dd9d41d6adeff492950000000000000960801; openh5_uuid=E1BD0ABE0A4A8F012F3E7C3D393E13D4598E05C2BFE038A1F57A72FD44F391FC; uuid=E1BD0ABE0A4A8F012F3E7C3D393E13D4598E05C2BFE038A1F57A72FD44F391FC; w_visitid=5c32fc19-675b-4a73-bdcd-8ea5f2d22df7; logan_session_token=o31gam4i2v9no6zlkqpg; logan_custom_report=; service-off=0; terminal=i; w_utmz="utm_campaign=(direct)&utm_source=5000&utm_medium=(none)&utm_content=(none)&utm_term=(none)"; w_latlng=0,0; w_actual_lat={self.lat}; w_actual_lng={self.lng}; openh5_uuid=E1BD0ABE0A4A8F012F3E7C3D393E13D4598E05C2BFE038A1F57A72FD44F391FC'
        payload = f'geoType=2&mtWmPoiId={poi_id}&dpShopId=-1&source=shoplist&skuId=&uuid=E1BD0ABE0A4A8F012F3E7C3D393E13D4598E05C2BFE038A1F57A72FD44F391FC&platform=3&partner=4&riskLevel=71&optimusCode=10&wm_actual_latitude={self.lat}&wm_actual_longitude={self.lng}&openh5_uuid=E1BD0ABE0A4A8F012F3E7C3D393E13D4598E05C2BFE038A1F57A72FD44F391FC'

        url = self.index_url + last_url + '?_=' + str(int(time() * 1000))
        # print('食品页-----')
        # print(url)
        # print(headers['Cookie'])
        # print(payload)
        response_json = self.post_request(url,self.headers,payload)
        try:
            food_category_list = response_json['data']['categoryList']
        except:
            response_json = self.post_request(url, self.headers, payload)
            try:
                food_category_list = response_json['data']['categoryList']
            except Exception as TypeError:
                return ''

        hot_foods = []
        for food_category in food_category_list:
            if '热销' in food_category['categoryName']:
                hot_foods.append(food_category)
        return json.dumps(hot_foods).replace("'",'')
    # 'https://i.waimai.meituan.com/openh5/poi/info?_=1589277696918'
    def request_detail_info(self,poi_id,last_url='/poi/info'):
        headers = copy.deepcopy(self.headers)
        headers['Cookie'] = f'cityid={self.city}; network=wifi; utm_source=meizu4; utm_medium=android; utm_term=1000000202; utm_content=862095026057122; utm_campaign=AgroupBgroupC0E0Ghomepage_category1_394__a1__c-1024; wm_order_channel=mtjj; au_trace_key_net=default; _lx_utm=utm_source%3D60374%26utm_medium%3Dandroid%26utm_term%3D1000000202%26utm_content%3D862095026057122%26utm_campaign%3DAgroupBgroupC0E0Ghomepage_category1_394__a1__c-1024; _lxsdk_cuid=1725440c0da2-08336aca1-5a10162d-3c000-1725440c0dc62; _lxsdk_s=1725440c0e0-f28-0db-5e0%7C-1%7CNaN; _lxsdk=E1BD0ABE0A4A8F012F3E7C3D393E13D4598E05C2BFE038A1F57A72FD44F391FC; _lxsdk_unoinid=0ca77ead48c848dd9d41d6adeff492950000000000000960801; openh5_uuid=E1BD0ABE0A4A8F012F3E7C3D393E13D4598E05C2BFE038A1F57A72FD44F391FC; uuid=E1BD0ABE0A4A8F012F3E7C3D393E13D4598E05C2BFE038A1F57A72FD44F391FC; w_visitid=5c32fc19-675b-4a73-bdcd-8ea5f2d22df7; logan_session_token=o31gam4i2v9no6zlkqpg; logan_custom_report=; service-off=0; terminal=i; w_utmz="utm_campaign=(direct)&utm_source=5000&utm_medium=(none)&utm_content=(none)&utm_term=(none)"; w_latlng=0,0; w_actual_lat={self.lat}; w_actual_lng={self.lng}; openh5_uuid=E1BD0ABE0A4A8F012F3E7C3D393E13D4598E05C2BFE038A1F57A72FD44F391FC'

        payload = f'shopId=0&mtWmPoiId={poi_id}&source=shoplist&channel=6&uuid=E1BD0ABE0A4A8F012F3E7C3D393E13D4598E05C2BFE038A1F57A72FD44F391FC&platform=3&partner=4&riskLevel=71&optimusCode=10&wm_actual_latitude={self.lat}&wm_actual_longitude={self.lng}&openh5_uuid=E1BD0ABE0A4A8F012F3E7C3D393E13D4598E05C2BFE038A1F57A72FD44F391FC'
        url = self.index_url + last_url + '?_=' + str(int(time() * 1000))
        # print('商店详情页----')
        # print(url)
        # print(headers['Cookie'])
        # print(payload)
        response_json = self.post_request(url,self.headers,payload)
        kwargs = {}
        try:
            # 商家服务
            kwargs['mark'] = response_json['data']['brandMsg'] if 'brandMsg' in response_json['data'].keys() else ''
            # 营业时间
            try:
                kwargs['business_time'] = response_json['data']['serTime']
            except:
                kwargs['business_time'] = ['']
            kwargs['address'] = response_json['data']['shopAddress'].replace("'",'')
            #经纬度
            kwargs['address_gps_long'] = response_json['data']['shopLng']
            kwargs['address_gps_lat'] = response_json['data']['shopLat']
        except:
            response_json = self.post_request(url, self.headers, payload)
            # 商家服务
            try:
                kwargs['mark'] = response_json['data']['brandMsg'] if 'brandMsg' in response_json['data'].keys() else ''
            except:
                kwargs['mark'] = ''
            # 营业时间
            try:
                kwargs['business_time'] = response_json['data']['serTime']
            except:
                kwargs['business_time'] = ['']
            try:
                kwargs['address'] = response_json['data']['shopAddress'].replace("'",'')
            except:
                kwargs['address'] = ''
            # 经纬度
            try:
                kwargs['address_gps_long'] = response_json['data']['shopLng']
                kwargs['address_gps_lat'] = response_json['data']['shopLat']
            except:
                kwargs['address_gps_long'] = 0
                kwargs['address_gps_lat'] = 0
        return kwargs



    # 'https://i.waimai.meituan.com/openh5/poi/comments?_=1589353892512'
    def request_detail_comments(self,poi_id,last_url='/poi/comments'):
        # 如果有问题把 " w_actual_lat=22544568; w_actual_lng=113949059" 拼接到cookie
        headers = copy.deepcopy(self.headers)
        headers['Cookie'] = f'cityid={self.city}; network=wifi; utm_source=meizu4; utm_medium=android; utm_term=1000000202; utm_content=862095026057122; utm_campaign=AgroupBgroupC0E0Ghomepage_category1_394__a1__c-1024; wm_order_channel=mtjj; au_trace_key_net=default; _lx_utm=utm_source%3D60374%26utm_medium%3Dandroid%26utm_term%3D1000000202%26utm_content%3D862095026057122%26utm_campaign%3DAgroupBgroupC0E0Ghomepage_category1_394__a1__c-1024; _lxsdk_cuid=1725440c0da2-08336aca1-5a10162d-3c000-1725440c0dc62; _lxsdk_s=1725440c0e0-f28-0db-5e0%7C-1%7CNaN; _lxsdk=E1BD0ABE0A4A8F012F3E7C3D393E13D4598E05C2BFE038A1F57A72FD44F391FC; _lxsdk_unoinid=0ca77ead48c848dd9d41d6adeff492950000000000000960801; openh5_uuid=E1BD0ABE0A4A8F012F3E7C3D393E13D4598E05C2BFE038A1F57A72FD44F391FC; uuid=E1BD0ABE0A4A8F012F3E7C3D393E13D4598E05C2BFE038A1F57A72FD44F391FC; w_visitid=5c32fc19-675b-4a73-bdcd-8ea5f2d22df7; logan_session_token=o31gam4i2v9no6zlkqpg; logan_custom_report=; service-off=0; terminal=i; w_utmz="utm_campaign=(direct)&utm_source=5000&utm_medium=(none)&utm_content=(none)&utm_term=(none)"; w_latlng=0,0; w_actual_lat={self.lat}; w_actual_lng={self.lng}; openh5_uuid=E1BD0ABE0A4A8F012F3E7C3D393E13D4598E05C2BFE038A1F57A72FD44F391FC'

        payload = f'shopId=0&mtWmPoiId={poi_id}&startIndex=0&labelId=0&scoreType=0&uuid=E1BD0ABE0A4A8F012F3E7C3D393E13D4598E05C2BFE038A1F57A72FD44F391FC&platform=3&partner=4&riskLevel=71&optimusCode=10&wm_latitude={self.lat}&wm_longitude={self.lng}&openh5_uuid=E1BD0ABE0A4A8F012F3E7C3D393E13D4598E05C2BFE038A1F57A72FD44F391FC'

        url = self.index_url + last_url + '?_=' + str(int(time() * 1000))
        # print('评论页-----')
        # print(url)
        # print(headers['Cookie'])
        # print(payload)
        response_json = self.post_request(url,headers=headers,payload=payload)
        kwargs = {}
        # 配送评分
        try:
            kwargs['delivery_score'] = float('%.2f' % response_json['data']['deliveryScore'])
        except Exception as KeyError:
            kwargs['delivery_score'] = 0
        # 包装评分
        try:
            kwargs['pack_score'] = float('%.2f' % response_json['data']['packScore'])
        except Exception as KeyError:
            kwargs['pack_score'] = 0
        # 口味评分
        try:
            kwargs['taste_score'] = float('%.2f' % response_json['data']['qualityScore'])
        except:
            kwargs['taste_score'] = 0
        # 评论
        try:
            kwargs['comments'] = json.dumps(response_json['data']['list']).replace("'",'')
        except Exception as KeyError:
            kwargs['comments'] = ''
        return kwargs


    def post_request(self,url,headers,payload):
        # headers['Cookie'] = 'cityid={}; network=wifi; uuid=450940DF938B12BD8AAC598D8CF4678D69BDD48C75BE2CD34A3C20CA525B3490; utm_source=wandoujia; utm_medium=android; utm_term=1000000202; utm_content=861735030994726; wm_order_channel=mtjj; au_trace_key_net=default; openh5_uuid=450940DF938B12BD8AAC598D8CF4678D69BDD48C75BE2CD34A3C20CA525B3490; terminal=i; w_utmz="utm_campaign=(direct)&utm_source=5000&utm_medium=(none)&utm_content=(none)&utm_term=(none)"; openh5_uuid=450940DF938B12BD8AAC598D8CF4678D69BDD48C75BE2CD34A3C20CA525B3490; service-off=0; utm_campaign=AgroupBgroupC0E0Ghomepage_category1_394__a1__c-1024;'.format(self.city)+' channelType={%22mtjj%22:%220%22}; '+'w_actual_lat={lat}; w_actual_lng={lng}'.format(lat=self.lat,lng=self.lng)

        try:
            response = requests.post(url=url, headers=headers, data=payload,proxies=self.proxy,timeout=10)
            if '登录' in response.content.decode():
                self.proxy = taiyang_proxy()
        except:
            self.proxy = taiyang_proxy()
            response = requests.post(url=url, headers=headers, data=payload)
        try:
            json_response = json.loads(response.content.decode())
        except Exception as e:
            logging.error(e)
            return {}
        return json_response

    def work(self,firstCategoryId='910',secondCategoryId='101792'):
        # print('当前抓取经纬度-----------:',self.city + '&'+self.lat + '&' + self.lng)
        # print('当前抓取第二分类：',secondCategoryId)
        has_next_page = True
        while has_next_page:
            # print('当前页数------:',self.page)
            data = self.request_list_from_category(page=self.page,firstCategoryId=firstCategoryId,secondCategoryId=secondCategoryId)
            category_tags_l2_name,category_tags_l3_name = self.get_category(firstCategoryId,secondCategoryId)
            # 是否有下一页
            try:
                has_next_page = data['data']['poiHasNextPage']
            except Exception as KeyError:
                # print('当前分类完成--------------：',secondCategoryId)
                break
            # 店铺列表
            for shop in data['data']['shopList']:
                # 去重过滤
                if self.filter_poiId(shop['mtWmPoiId']):
                    # print('这家店铺已存在-------：',shop['shopName'])
                    continue
                # print('抓取店铺--------:',shop['shopName'],'$$$$',shop['mtWmPoiId'])
                cur_kwargs = {}
                cur_kwargs['source_data'] = '美团'
                cur_kwargs['category_tags_l1_name'] = '美食'
                cur_kwargs['category_tags_l2_name'] = category_tags_l2_name
                # 快餐便当
                cur_kwargs['category_tags_l3_name'] = category_tags_l3_name
                shop_kwargs = self.process_shop_data(shop)
                cur_kwargs.update(shop_kwargs)
                # 获取商品信息 返回字符串 热销

                hot_foods = self.request_detail_food(poi_id=cur_kwargs['shopid'])
                cur_kwargs['popular_dishes'] = hot_foods
                # # 获取商铺信息

                info_kwargs = self.request_detail_info(poi_id=cur_kwargs['shopid'])
                cur_kwargs.update(info_kwargs)
                # # 获取商铺评论

                comment_kwargs = self.request_detail_comments(poi_id=cur_kwargs['shopid'])
                cur_kwargs.update(comment_kwargs)
                self.process_save_data(**cur_kwargs)
                sleep(random.uniform(0.2,0.4))
            self.page += 1
            # sleep(random.uniform(0.3,0.8))
        self.page = 1


    def process_shop_data(self,shop):
        # 所需数据
        kwargs = {}
        kwargs['shopname'] = shop['shopName'].replace("'","’")
        kwargs['shopid'] = shop['mtWmPoiId']
        kwargs['shop_score'] = shop['wmPoiScore']
        # 构造商铺url
        kwargs['url'] = 'https://i.waimai.meituan.com/external/poi/{}?utm_source=5913&amp;wmi_from=cpoiinfo&amp;user_id=0'.format(kwargs['shopid'])
        kwargs['cityname'] = self.get_cityname()
        # 起送价
        kwargs['minimum_charge'] = shop['minPriceTip']
        # 月售
        kwargs['mon_sales'] = shop['monthSalesTip']  # 有疑虑
        # 人均消费
        kwargs['avg_speed'] = shop['averagePriceTip']
        # 优惠活动
        try:
            kwargs['special_offer'] = []
            for special_offer in shop['discounts2']:
                kwargs['special_offer'].append(special_offer['info'])
        except Exception as KeyError:
            kwargs['special_offer'] = ''
        return kwargs

    def process_save_data(self,**kwargs):
        # 行政区

        if '市' in kwargs['address'] and '区' in kwargs['address'] and '市场' not in kwargs['address'] and '城市' not in kwargs['address']:
            try:
                unuse_city,kwargs['region'] = re.findall(r'(?!.*省)(\w+市)(\w+?区)',kwargs['address'])[0]
            except:
                kwargs['region'] = ''
        elif '区' in kwargs['address'] and '社区' not in kwargs['address']:
            try:
                kwargs['region'] = re.findall(r'(\w+区)',kwargs['address'])[0]
            except:
                kwargs['region'] = ''
        else:
            kwargs['region'] = ''
        if len(kwargs['region']) >= 10:
            kwargs['region'] = ''
        kwargs['cityname'] = kwargs['cityname'] if '市' in kwargs['cityname'] else kwargs['cityname'] + '市'
        # 分数
        kwargs['shop_score'] = float('%.2f' % (int(kwargs['shop_score']) / 10))
        # 经纬度
        if kwargs['address_gps_lat'] != 0 and kwargs['address_gps_long'] != 0:
            kwargs['address_gps_lat'] = str(float('%.7f' % kwargs['address_gps_lat']) / 1000000)
            kwargs['address_gps_long'] = str(float('%.7f' % kwargs['address_gps_long']) / 1000000)

        # 人均
        try:
            kwargs['avg_speed'] = float('%.2f' % float(kwargs['avg_speed'].replace('人均 ¥','')))
        except:
            kwargs['avg_speed'] = 0
        # 营业时间
        kwargs['business_time'] = json.dumps(kwargs['business_time'])
        # 起送
        kwargs['minimum_charge'] = float('%.2f' % float(kwargs['minimum_charge'].replace('起送 ¥','')))
        # 月售
        kwargs['mon_sales'] = int(kwargs['mon_sales'].replace('月售','').replace('+',''))
        kwargs['special_offer'] = json.dumps(kwargs['special_offer']).replace("'",'')
        # print(kwargs)
        # 构造id
        kwargs['id'] = self.get_unique_id(**kwargs)
        #添加时间
        kwargs['update_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # 插入数据
        if kwargs['shopname'] and kwargs['address'] and kwargs['address_gps_long'] and kwargs['address_gps_lat']:
            self.insert_data(**kwargs)


    def insert_data(self,**kwargs):

        sql = """
        insert into mt_wm (source_data,shopname,shopid,category_tags_l1_name,category_tags_l2_name,category_tags_l3_name,
        cityname,region,address,address_gps_long,address_gps_lat,shop_score,taste_score,pack_score,delivery_score,comments,popular_dishes,minimum_charge,mon_sales,avg_speed,business_time,
        special_offer,mark,id,update_time,url) values ('%(source_data)s','%(shopname)s','%(shopid)s','%(category_tags_l1_name)s','%(category_tags_l2_name)s',
        '%(category_tags_l3_name)s','%(cityname)s','%(region)s','%(address)s','%(address_gps_long)s','%(address_gps_lat)s','%(shop_score)f',
        %(taste_score)f,%(pack_score)f,%(delivery_score)f,'%(comments)s','%(popular_dishes)s',
        '%(minimum_charge)f','%(mon_sales)d','%(avg_speed)f','%(business_time)s','%(special_offer)s','%(mark)s','%(id)s','%(update_time)s','%(url)s')
        ON CONFLICT (id)
        DO UPDATE SET cityname='%(cityname)s',region='%(region)s',shop_score='%(shop_score)f',taste_score='%(taste_score)f',pack_score='%(pack_score)f',delivery_score='%(delivery_score)f',minimum_charge='%(minimum_charge)f',mon_sales='%(mon_sales)d',avg_speed='%(avg_speed)f',business_time='%(business_time)s',special_offer='%(special_offer)s',mark='%(mark)s',update_time='%(update_time)s',url='%(url)s';
        """ % kwargs

        sql2 = """insert into mt_wm (source_data,shopname,shopid,category_tags_l1_name,category_tags_l2_name,category_tags_l3_name,
        cityname,region,address,address_gps_long,address_gps_lat,shop_score,taste_score,pack_score,delivery_score,comments,popular_dishes,minimum_charge,mon_sales,avg_speed,business_time,
        special_offer,mark,id,update_time,url) values ('%(source_data)s','%(shopname)s','%(shopid)s','%(category_tags_l1_name)s','%(category_tags_l2_name)s',
        '%(category_tags_l3_name)s','%(cityname)s','%(region)s','%(address)s','%(address_gps_long)s','%(address_gps_lat)s','%(shop_score)f',
        %(taste_score)f,%(pack_score)f,%(delivery_score)f,'%(comments)s','%(popular_dishes)s',
        '%(minimum_charge)f','%(mon_sales)d','%(avg_speed)f','%(business_time)s','%(special_offer)s','%(mark)s','%(id)s','%(update_time)s','%(url)s')""" % kwargs
        try:
            cur.execute(sql2)
            conn.commit()
            self.filter_add(kwargs['shopid'])
            print('插入成功----:', kwargs['shopname'] + '$$$$' + kwargs['shopid'])
        except Exception as e:
            print('已存在----:', kwargs['shopname'] + '$$$$' + kwargs['shopid'])



    def get_category(self,firstcategoryId,secondcategoryId):
        with open('cate_id.json','r',encoding='utf-8') as f:
            data = json.loads(f.read())
        firstcategoryname = data[firstcategoryId]
        secondcategoryname = data[secondcategoryId]
        return firstcategoryname,secondcategoryname

    def get_region(self,address):
        address = address.split('路')[0] + '路' if '路' in address else address.split('街')[0] + '街'
        url = 'https://map.baidu.com/su?wd={}&cid=340&type=0&t=1589457215631'.format(address)
        headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Host': 'map.baidu.com',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
        }
        try:
            resp = requests.get(url,headers,proxies=self.proxy).content.decode()
        except:
            self.proxy = taiyang_proxy()
            resp = requests.get(url,headers,proxies=self.proxy).content.decode()
        ret = json.loads(resp)
        region = ret['s'][0].split('$')[1]
        city = ret['s'][0].split('$')[0]
        return city,region

    def filter_poiId(self,poiId):
        return redis.sismember(redis_filter_name,poiId)

    def filter_add(self,poiId):
        redis.sadd(redis_filter_name,poiId)

    def get_unique_id(self,**kwargs):
        hash_str = kwargs['source_data'] + '$' + kwargs['shopname'] + '$' + kwargs['address'] + '$' + str(kwargs['address_gps_long']) + '$' + str(kwargs['address_gps_lat'])

        return hashlib.md5(hash_str.encode('utf-8')).hexdigest()

    def get_cityname(self):
        with open('city_id.json','r',encoding='utf-8') as f:
            data = json.loads(f.read())
        return data[self.city]

def run():
    while True:
        wm_args = redis.spop(redis_name)
        city_id = wm_args.split(',')[0]
        lat = wm_args.split(',')[2]
        lng = wm_args.split(',')[1]
        mt_wm = WM_Spider(lat=lat, lng=lng,city_id=city_id)
        cateli = ['101792', '100839', '100840', '101785', '101786',
                  '100842', '101615', '101791', '100841', '101979',
                  '100944', '103728', '101790', '101980', '100843',
                  '101788', '100845', '101789', '100844', '102145',
                  '102463', '102464']
        for cate in cateli:
            mt_wm.work(firstCategoryId='910', secondCategoryId=cate)
        yinpin_cateli = ['100837', '1044', '1042', '100000', '100838']
        for cate in yinpin_cateli:
            mt_wm.work(firstCategoryId='19', secondCategoryId=cate)

if __name__ == '__main__':
    for i in range(1):
        t = Thread(target=run)
        t.start()
        sleep(2)
    # latlng_list = [('22515737','114069273'),('22595087','114513254'),('22629908','114425497'),('22564938','114050546'),('22695350','114216918'),('22555461','114151070'),('22539352','114494500'),('22490830','114580954'),('22689812','114348183'),('22681653','113939385'),('22771264','113844243'),('22563406','114111295'),('22567280','114130052'),('22557001','114236739'),('22544675','114570276')]
    # for lat,lng in latlng_list:
    #     mt_wm = WM_Spider(lat=lat,lng=lng)
    #     cateli = ['100035','100040','100044','100038','100041','102479','100042','102481',
    #               '101179','100209','100213','100856','100857','100953','100858','101110',
    #               '100191','100849','100850','100904','100180','100238','100906','100369',
    #               '100240','100244','100946','100905','100325','100966','100969','100967',
    #               '100968','100321','102513','100852','100853','102515','102514','101792',
    #               '100839','100840','101785','101786','100842','101615','101791','100841',
    #               '101979','100944','103728','101790','101980','100843','101788','100845',
    #               '101789','100844','102145','102463','102464']
    #     cateli = ['101792', '100839', '100840', '101785', '101786',
    #               '100842', '101615', '101791', '100841', '101979',
    #               '100944', '103728', '101790', '101980', '100843',
    #               '101788', '100845', '101789', '100844', '102145',
    #               '102463', '102464']
    #     for cate in cateli[8:]:
    #         mt_wm.work(firstCategoryId='910',secondCategoryId=cate)
    #     yinpin_cateli = ['100837','1044','1042','100000','100838']
    #     for cate in yinpin_cateli:
    #         mt_wm.work(firstCategoryId='19',secondCategoryId=cate)





# beijing_latlng_list = [
#     "117073221,40493866","116322056,39894910","116435806,39908501","116195142,40224933","116557351,39912182",
#     "116429172,39510561","116277505,39910506","116458855,39909863","116542574,40073242","116657851,39907872",
#     "116382590,39942143","116670334,40354822","116494776,39867730","116328344,40078096","116454982,39878934",
#     "116381729,39968002","116843177,40376834","117119254,40147761","116398353,39900558","116455294,39937492",
#     "116280902,40168114","116306750,40041730","116603039,40080525","116738741,40142258","116412557,39912742",
#     "116466485,39995197","116375121,39908342","116353714,39939588","116408027,39991761","115981383,40464504",
#     "116488382,39878439","116481835,39800184","116404000,39873135","116319802,39982940","116277687,39866858"
# ]


