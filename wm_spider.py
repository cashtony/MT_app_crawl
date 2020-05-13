import requests
import json
from redis import Redis
class WM_Spider:
    def __init__(self,lat,lng):
        self.redis = Redis(decode_responses=True)
        self.lat = lat
        self.lng = lng
        self.proxy = None
        self.index_url = 'https://i.waimai.meituan.com/openh5'

    # 'https://i.waimai.meituan.com/openh5/channel/kingkongshoplist?_=1589286163907'
    def request_list_from_category(self,last_url='/channel/kingkongshoplist'):

