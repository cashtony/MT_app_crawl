import copy
from time import time

import requests
import json
from redis import Redis
class WM_Spider:
    def __init__(self,lat,lng,city_id='30'):
        self.redis = Redis(decode_responses=True)
        self.city = city_id
        self.lat = lat
        self.lng = lng
        self.proxy = None
        self.index_url = 'https://i.waimai.meituan.com/openh5'
        self.headers = {
            'Host': 'i.waimai.meituan.com',
            'Accept': 'application/json',
            'Origin': 'https://h5.waimai.meituan.com',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; Redmi Note 3 Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.91 Mobile Safari/537.36 TitansX/11.19.6 KNB/1.2.0 android/6.0.1 mt/com.sankuai.meituan/10.0.202 App/10120/10.0.202 MeituanGroup/10.0.202',
            'Referer': 'https://h5.waimai.meituan.com/waimai/mindex/menu?dpShopId=&mtShopId=1112840116809435&utm_source=wandoujia&channel=mtjj&source=shoplist&initialLat=22.544568&initialLng=113.949059&actualLat=22.544568&actualLng=113.949059',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,en-US;q=0.9',
            'Cookie': 'cityid={city_id}; uuid=450940DF938B12BD8AAC598D8CF4678D69BDD48C75BE2CD34A3C20CA525B3490; utm_medium=android; utm_term=1000000202; utm_content=861735030994726; w_actual_lat={w_actual_lat}; w_actual_lng={w_actual_lng}'.format(city_id=city_id,w_actual_lat=self.lat,w_actual_lng=self.lng),
            'X-Requested-With': 'com.sankuai.meituan',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Connection': 'keep-alive',
        }

    # 'https://i.waimai.meituan.com/openh5/channel/kingkongshoplist?_=1589286163907'
    def request_list_from_category(self,firstCategoryId,secondCategoryId,page='0',last_url='/channel/kingkongshoplist'):
        payload = 'startIndex={startIndex}&navigateType=910&firstCategoryId={firstCategoryId}&secondCategoryId={secondCategoryId}&geoType=2&platform=3&partner=4&originUrl=https://h5.waimai.meituan.com/waimai/mindex/kingkong?navigateType=910&firstCategoryId={firstCategoryId}&secondCategoryId={secondCategoryId}&title=%E7%BE%8E%E9%A3%9F&riskLevel=71&optimusCode=10&wm_actual_latitude={wm_actual_latitude}&wm_actual_longitude={wm_actual_longitude}&openh5_uuid=450940DF938B12BD8AAC598D8CF4678D69BDD48C75BE2CD34A3C20CA525B3490'
        kwargs = {
            'startIndex': str(int(page) - 1),
            'firstCategoryId':firstCategoryId,
            'secondCategoryId':secondCategoryId,
            'wm_actual_latitude':self.lat,
            'wm_actual_longitude':self.lng
        }

        url = self.index_url + last_url + '?_=' + str(int(time() * 1000))

        response_json = self.post_request(url,self.headers,payload.format_map(kwargs))
        return response_json

    # 'https://i.waimai.meituan.com/openh5/poi/food?_=1589277696918'
    def request_detail_food(self,poi_id,last_url='/poi/food'):
        payload = 'mtWmPoiId={mtWmPoiId}&openh5_uuid=450940DF938B12BD8AAC598D8CF4678D69BDD48C75BE2CD34A3C20CA525B3490'.format(mtWmPoiId=poi_id)
        url = self.index_url + last_url + '?_=' + str(int(time() * 1000))
        response_json = self.post_request(url,self.headers,payload)

    # 'https://i.waimai.meituan.com/openh5/poi/info?_=1589277696918'
    def request_detail_info(self,poi_id,last_url='/poi/info'):
        payload = 'mtWmPoiId={mtWmPoiId}&openh5_uuid=450940DF938B12BD8AAC598D8CF4678D69BDD48C75BE2CD34A3C20CA525B3490'.format(mtWmPoiId=poi_id)
        url = self.index_url + last_url + '?_=' + str(int(time() * 1000))
        response_json = self.post_request(url,self.headers,payload)

    # 'https://i.waimai.meituan.com/openh5/poi/comments?_=1589353892512'
    def request_detail_comments(self,poi_id,last_url='/poi/comments'):
        # 如果有问题把 " w_actual_lat=22544568; w_actual_lng=113949059" 拼接到cookie
        headers = copy.deepcopy(self.headers)
        headers['Cookie'] = 'cityid={city_id}; network=wifi; utm_medium=android; utm_term=1000000202; utm_content=861735030994726; _lxsdk_cuid=171f918eca2c8-0a4e8cc73bc7e7-7452c56-38400-171f918eca5c8; _lxsdk=450940DF938B12BD8AAC598D8CF4678D69BDD48C75BE2CD34A3C20CA525B3490; _lxsdk_s=1720cdf3bd3-4f6-026-814%7C-1%7CNaN;'.format(city_id=self.city)

        payload = 'mtWmPoiId={mtWmPoiId}&startIndex=0&platform=3&partner=4&originUrl=https%3A%2F%2Fh5.waimai.meituan.com%2Fwaimai%2Fmindex%2Fmenu%3FdpShopId%3D%26mtShopId%3D891876934366856%26utm_source%3Dwandoujia%26channel%3Dmtjj%26source%3Dshoplist%26initialLat%3D%26initialLng%3D%26actualLat%3D22.544568%26actualLng%3D113.949059&riskLevel=71&optimusCode=10&openh5_uuid=450940DF938B12BD8AAC598D8CF4678D69BDD48C75BE2CD34A3C20CA525B3490'

        url = self.index_url + last_url + '?_=' + str(int(time() * 1000))
        response_json = self.post_request(url,headers=headers,payload=payload.format(mtWmPoiId=poi_id))

    def post_request(self,url,headers,payload):
        response = requests.post(url=url,headers=headers,data=payload)
        return json.loads(response.content.decode())

    def process_list_data(self,data):
