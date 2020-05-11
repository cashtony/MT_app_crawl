# -*- coding: UTF-8 -*-
import base64
import hashlib
import json
import random
import string
import time
import uuid
import zlib

from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from urllib.parse import quote, unquote

import requests


class meituan_encrypt:
    """
    美团外卖加密逆向
    """
    referer_url = 'https://h5.waimai.meituan.com/waimai/mindex/kingkong?navigateType=910&firstCategoryId=910&secondCategoryId=910&title=%E7%BE%8E%E9%A3%9F'

    def __init__(self, UID=None, new_param=None, debug=False):
        self.uid = UID if UID else ''.join(random.sample("%s%s" % (string.ascii_uppercase, string.digits), 32)) + \
                                   ''.join(random.sample("%s%s" % (string.ascii_uppercase, string.digits), 32))
        self.new_param = self.new_param = new_param if new_param else {}
        self.debug = debug
        self.all_param = dict()


    def waimai_param(self):
        """
        美团外卖所需要的的参数构成
        :return: dict
        """
        userAgent = self.user_agent()
        # 目前写死
        utm_content = "861735030994726" #IMEI
        kwargs = dict()
        kwargs["__skck"] = hashlib.md5(str(time.time() - random.randint(0, 999)).encode()).hexdigest()
        kwargs["__skua"] = hashlib.md5(userAgent[1].encode()).hexdigest()
        kwargs["push_token"] = "dpsh" + hashlib.md5(
            str(time.time() - random.randint(0, 999)).encode()).hexdigest() + "atpu"
        kwargs["ci"] = random.randint(1, 64)
        kwargs["request_id"] = str(uuid.uuid4()).upper()
        kwargs["wm_mac"] = "%20".join([
            "%3A".join(["%.2x" % random.randint(17,254) for _ in range(6)])
            for _ in range(1)])
        kwargs["utm_source"] = str(random.randint(1009, 1040))
        kwargs["utm_content"] = utm_content  # IMEI
        kwargs["req_time"] = str(int(time.time() * 1000) - random.randint(20, 60))
        kwargs["__skts"] = str(int(time.time() * 1000))
        kwargs["wm_visitid"] = str(uuid.uuid4())
        kwargs["wm_dtype"] = userAgent[0]
        kwargs["uuid"] = self.uid
        kwargs["seq_id"] = random.randint(200, 1000)
        kwargs["header_agent"] = userAgent[1]
        kwargs["req_time"] = str(int(time.time() * 1000) - random.randint(20, 60))
        kwargs["__skts"] = str(int(time.time() * 1000))
        kwargs["wm_seq"] = random.randint(3, 30)
        kwargs["__skno"] = str(uuid.uuid4())
        return kwargs


    @staticmethod
    def user_agent():
        """
        随机UA
        :return:
        """
        return random.choice([
            ("MI%204S", "AiMeiTuan /Xiaomi-5.1.1-MI 4S-1280x720-240-10.0.202-642-{}-wandoujia"),
            ("MI%20NOTE%20LTE", "AiMeiTuan /Xiaomi-5.1.1-MI NOTE LTE-1280x720-240-10.0.202-642-{}-wandoujia"),
            ("SM-N9108V", "AiMeiTuan /SAMSUNG-5.1.1-SM-N9108V-1280x720-240-9.4.10.0.202-{}-wandoujia"),
            ("SM-J5008", "AiMeiTuan /SAMSUNG-5.1.1-SM-J5008-1280x720-240-10.0.202-642-{}-wandoujia"),
            # ("R11", "Dalvik/1.6.0 (Linux; U; Android 4.4.2; R11 Build/LMY47V)"),
            # ("3007", "Dalvik/1.6.0 (Linux; U; Android 4.4.2; 3007 Build/LMY47V)"),
            # ("A51", "Dalvik/1.6.0 (Linux; U; Android 4.4.2; A51 Build/LMY47V)"),
            # ("Coolpad%208720L", "Dalvik/1.6.0 (Linux; U; Android 4.4.2; Coolpad 8720L Build/LMY47V)"),
            # ("G621-TL00", "Dalvik/1.6.0 (Linux; U; Android 4.4.2; G621-TL00 Build/LMY47V)"),
            # ("GT-I9508", "Dalvik/1.6.0 (Linux; U; Android 4.4.2; GT-I9508 Build/LMY47V)"),
            # ("GT-I9508V", "Dalvik/1.6.0 (Linux; U; Android 4.4.2; GT-I9508V Build/LMY47V)"),
            # ("vivo%20Y913", "Dalvik/1.6.0 (Linux; U; Android 4.4.2; vivo Y913 Build/LMY47V)"),
            # ("vivo%20Y28L", "Dalvik/1.6.0 (Linux; U; Android 4.4.2; vivo Y28L Build/LMY47V)"),
            # ("vivo%20X3L", "Dalvik/1.6.0 (Linux; U; Android 4.4.2; vivo X3L Build/LMY47V)"),
            # ("vivo%20V3Max", "Dalvik/1.6.0 (Linux; U; Android 4.4.2; vivo V3Max Build/LMY47V)"),
            # ("SM-G5308W", "Dalvik/1.6.0 (Linux; U; Android 4.4.2; SM-G5308W Build/LMY47V)"),
            # ("SM-G3518", "Dalvik/1.6.0 (Linux; U; Android 4.4.2; SM-G3518 Build/LMY47V)"),
            ("Redmi%20Note%203", "AiMeiTuan /Xiaomi-5.1.1-Redmi Note 3-1280x720-240-10.0.202-642-{}-wandoujia"),
            # ("N5207", "Dalvik/1.6.0 (Linux; U; Android 4.4.2; N5207 Build/LMY47V)"),
            # ("R8207", "Dalvik/1.6.0 (Linux; U; Android 4.4.2; R8207 Build/LMY47V)"),
            # ("LG-H818", "Dalvik/1.6.0 (Linux; U; Android 4.4.2; LG-H818 Build/LMY47V)"),
            # ("C199s", "Dalvik/1.6.0 (Linux; U; Android 4.4.2; C199s Build/LMY47V)"),
            ("MI%202", "AiMeiTuan /Xiaomi-5.1.1-MI 2-1280x720-240-10.0.202-642-{}-wandoujia"),
            # ("L39h", "Dalvik/1.6.0 (Linux; U; Android 4.4.2; L39h Build/LMY47V)"),
            # ("LG-H819", "Dalvik/1.6.0 (Linux; U; Android 4.4.2; LG-H819 Build/LMY47V)"),
            # ("LG-H961N", "Dalvik/1.6.0 (Linux; U; Android 4.4.2; LG-H961N Build/LMY47V)"),
            # ("Lenovo%20S60-t", "Dalvik/1.6.0 (Linux; U; Android 4.4.2; Lenovo S60-t Build/LMY47V)"),
            ("MI%204LTE", "AiMeiTuan /Xiaomi-5.1.1-MI 4LTE-1280x720-240-10.0.202-642-{}-wandoujia"),
            # ("SM-N9008S", "Dalvik/1.6.0 (Linux; U; Android 4.4.2; SM-N9008S Build/LMY47V)"),
            # ("vivo%20Y27", "Dalvik/1.6.0 (Linux; U; Android 4.4.2; vivo Y27 Build/LMY47V)"),
        ])
    @staticmethod
    def get_xforwith(ctime):
        ts = str(int(ctime) - random.randint(2333, 66666))
        cts = str(int(ctime))
        xforwith = '{"ts":%s,"cts":%s,"brVD":[360,518],"brR":[[360,640],[360,640],24,24],"aM":""}' % (ts, cts)
        padding_num = 16 - (len(xforwith) % 16)
        real_data = xforwith + chr(padding_num) * padding_num
        return base64.b64encode(
            AES.new(b"jvzempodf8f9anyt", mode=AES.MODE_CBC, IV=b"jvzempodf8f9anyt").encrypt(
                real_data.encode())).decode()

    @staticmethod
    def get_token(data):
        return base64.b64encode(zlib.compress(data.encode())).decode()

    @staticmethod
    def get__token(request_param, refer_url):
        sign = meituan_encrypt.get_token('"%s"' % "&".join([unquote(value) for value in sorted(request_param.split('&'))]))
        ts = str(int(1000 * time.time()) - random.randint(2333, 66666))
        cts = str(int(1000 * time.time()))
        tmp_dict = {"ts": ts, "cts": cts, "sign": sign, "referer": refer_url}
        # tmp_dict.update(self.get_locus(_type))
        # mt ，at, tT 先写死
        # token = '{"rId":101701,"ver":"1.0.6","ts":{ts},"cts":{cts},' \
        #         '"brVD":[360,518],"brR":[[360,640],[360,640],24,24],' \
        #         '"bI":[{referer},""],"mT":["46,100"],"kT":[],"aT":["46,100,IMG"],"tT":%(tT)s,"aM":"",' \
        #         '"sign":{sign}}'.format_map(tmp_dict)
        token = '{"rId":101701,"ver":"1.0.6","ts":%(ts)s,"cts":%(cts)s,' \
                '"brVD":[360,518],"brR":[[360,640],[360,640],24,24],' \
                '"bI":["%(referer)s",""],"mT":["46,100"],"kT":[],"aT":["46,100,IMG"],"tT":[],"aM":"",' \
                '"sign":"%(sign)s"}' % tmp_dict
        # _token = quote(meituan_encrypt.get_token(token))
        return token
        # return "&_token={_token}".format(_token=_token)

    @staticmethod  # 生成记录轨迹的
    def get_locus(_type):
        '''

        :param _type: 1:geo搜索; 2:id获取菜品; 3:id获取店铺信息
        :return:
        '''
        if int(_type) == 3:
            return {
                "mT": '["310,109"]',
                "aT": '["310,109,DIV"]',
                "tT": '[]',
            }
        elif int(_type) == 2:
            return {
                "mT": '[]',
                "aT": '[]',
                "tT": '[]',
            }
        else:
            float_nums = [
                "66668701171875", "33333587646484", "6666717529297", "333251953125", "33334350585938",
                "666748046875", "3333435058594", "33349609375"
            ]
            first = '%d.%s,%d,%s,1' % (
                random.randint(300, 345), random.choice(float_nums), random.randint(70, 90), random.choice(float_nums)
            )
            second = '%d.%s,%d,%s,1' % (
                random.randint(200, 250), random.choice(float_nums), random.randint(300, 400), random.choice(float_nums)
            )
            return {
                "mT": '[]',
                "aT": '[]',
                "tT": '["%s","%s"]' % (first, second),
            }





class meituan_request:
    def __init__(self):
        self.list_url = 'https://i.waimai.meituan.com/openh5/channel/kingkongshoplist?'
        self.detail_url = 'https://i.waimai.meituan.com/openh5/poi/food?'
        # 基础头信息 改动
        self.headers = {
        'Host': 'i.waimai.meituan.com',
        'Connection': 'keep-alive',
        'Content-Length': '2685', # 变
        'Accept': 'application/json',
        'Origin':'https://h5.waimai.meituan.com',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; Redmi Note 3 Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.91 Mobile Safari/537.36 TitansX/11.19.6 KNB/1.2.0 android/6.0.1 mt/com.sankuai.meituan/10.0.202 App/10120/10.0.202 MeituanGroup/10.0.202',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': 'https://h5.waimai.meituan.com/waimai/mindex/kingkong?navigateType=910&firstCategoryId=910&secondCategoryId=910&title=%E7%BE%8E%E9%A3%9F',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,en-US;q=0.9',
        'Cookie': 'cityid=30; network=wifi; uuid=450940DF938B12BD8AAC598D8CF4678D69BDD48C75BE2CD34A3C20CA525B3490; utm_source=wandoujia; utm_medium=android; utm_term=1000000202; utm_content=861735030994726; wm_order_channel=mtjj; au_trace_key_net=default; _lxsdk_cuid=171f918eca2c8-0a4e8cc73bc7e7-7452c56-38400-171f918eca5c8; _lxsdk=450940DF938B12BD8AAC598D8CF4678D69BDD48C75BE2CD34A3C20CA525B3490; _lxsdk_unoinid=c149dc0316864b619f0662e6ebdd144e0000000000001415762; openh5_uuid=450940DF938B12BD8AAC598D8CF4678D69BDD48C75BE2CD34A3C20CA525B3490; terminal=i; w_utmz="utm_campaign=(direct)&utm_source=5000&utm_medium=(none)&utm_content=(none)&utm_term=(none)"; openh5_uuid=450940DF938B12BD8AAC598D8CF4678D69BDD48C75BE2CD34A3C20CA525B3490; service-off=0; utm_campaign=AgroupBgroupC0E0Ghomepage_category1_394__a1__c-1024; w_latlng=0,0; cssVersion=f6c6d196; _lx_utm=utm_source%3D60374%26utm_medium%3Dandroid%26utm_term%3D1000000202%26utm_content%3D861735030994726%26utm_campaign%3DAgroupBgroupC0E0Ghomepage_category1_394__a1__c-1024; channelType={%22mtjj%22:%220%22}; channelConfig={%22channel%22:%22mtjj%22%2C%22type%22:0%2C%22fixedReservation%22:{%22reservationTimeStatus%22:0%2C%22startReservationTime%22:0%2C%22endReservationTime%22:0}%2C%22homepageBannerTips%22:%22%E5%9B%A0%E7%89%88%E6%9C%AC%E8%BF%87%E4%BD%8E%EF%BC%8C%E6%82%A8%E6%AD%A3%E5%9C%A8%E4%BD%BF%E7%94%A8%E7%AE%80%E5%8C%96%E7%89%88%E9%A1%B5%E9%9D%A2%EF%BC%8C%E8%AF%B7%E5%8D%87%E7%BA%A7%E5%88%B0%E6%9C%80%E6%96%B0%E7%89%88%E6%9C%AC%22}; w_actual_lat=22546510; w_actual_lng=113948770',
        'X-Requested-With': 'com.sankuai.meituan'
        }
        self.request_params = None


    def request_secondCategory_list(self):
        cts = str(int((time.time() * 1000)))
        self.request_params = '_='+ cts + '&' + 'X-FOR-WITH=' + meituan_encrypt.get_xforwith(cts)
        real_url = self.list_url + self.request_params
        # 参数需要改动
        payload = self.get_data_params()
        headers = self.get_headers(payload)
        response = requests.post(real_url,headers=headers,data=payload)
        print('url:  ' + real_url)
        print(headers)
        print('payload:  ' + payload)
        print(response.text)


    def get_headers(self,payload):
        headers = self.headers
        headers['Content-Length'] = str(len(payload))
        # cityid , lat, lng
        headers['Cookie'] = self.get_cookie()
        return headers


    def get_cookie(self,city_id=30,lat='22.54651',lng='113.94877'):
        uuid = '450940DF938B12BD8AAC598D8CF4678D69BDD48C75BE2CD34A3C20CA525B3490'
        cookie = dict()
        cookie['cityid'] = str(city_id)
        cookie['network'] = 'wifi'
        cookie['uuid'] = uuid
        cookie['utm_source'] = 'wandoujia'
        cookie['utm_medium'] = 'android'
        cookie['utm_term'] = '1000000202' #版本信息
        cookie['utm_content'] = '861735030994726' # IMEI
        cookie['wm_order_channel'] = 'mtjj'
        cookie['au_trace_key_net'] = 'default'
        cookie['_lxsdk_cuid'] = '171f918eca2c8-0a4e8cc73bc7e7-7452c56-38400-171f918eca5c8'
        cookie['_lxsdk'] = uuid
        cookie['_lxsdk_unoinid'] = 'c149dc0316864b619f0662e6ebdd144e0000000000001415762'
        cookie['openh5_uuid'] = uuid
        cookie['terminal'] = 'i'
        cookie['w_utmz'] = 'utm_campaign=(direct)&utm_source=5000&utm_medium=(none)&utm_content=(none)&utm_term=(none)'
        cookie['openh5_uuid'] = uuid
        cookie['service-off'] = '0'
        cookie['utm_campaign'] = 'AgroupBgroupC0E0Ghomepage_category1_394__a1__c-1024'
        cookie['cssVersion'] = 'f6c6d196'
        cookie['_lx_utm'] = 'utm_source=60374&utm_medium='+ cookie['utm_medium'] +'&utm_term='+ cookie['utm_term'] +'&utm_content=' + cookie['utm_content'] + '&utm_campaign=' + cookie['utm_campaign']
        cookie['w_actual_lat'] = str(int(float(lat) * 1000000))
        cookie['w_actual_lng'] = str(int(float(lng) * 1000000))
        cookie['w_latlng'] = str(int(float(lat) * 1000000)) + ',' + str(int(float(lng) * 1000000))
        cookie['w_visitid'] = 'eb15bab3-77ac-4ef1-a894-cc0595f699c4'
        cookie['channelType'] = '{"mtjj":"0"}'
        cookie_list = list()
        for ck in cookie:
            cookie_list.append(ck + '=' + cookie[ck])
        cookies = '&'.join(cookie_list)
        return quote(cookies)
        """
        cityid	30
        network	wifi
        uuid	450940DF938B12BD8AAC598D8CF4678D69BDD48C75BE2CD34A3C20CA525B3490
        utm_source	wandoujia
        utm_medium	android
        utm_term	1000000202
        utm_content	861735030994726
        wm_order_channel	mtjj
        au_trace_key_net	default
        _lxsdk_cuid	171f918eca2c8-0a4e8cc73bc7e7-7452c56-38400-171f918eca5c8
        _lxsdk	450940DF938B12BD8AAC598D8CF4678D69BDD48C75BE2CD34A3C20CA525B3490
        _lxsdk_unoinid	c149dc0316864b619f0662e6ebdd144e0000000000001415762
        openh5_uuid	450940DF938B12BD8AAC598D8CF4678D69BDD48C75BE2CD34A3C20CA525B3490
        terminal	i
        w_utmz	"utm_campaign=(direct)&utm_source=5000&utm_medium=(none)&utm_content=(none)&utm_term=(none)"
        openh5_uuid	450940DF938B12BD8AAC598D8CF4678D69BDD48C75BE2CD34A3C20CA525B3490
        service-off	0
        utm_campaign	AgroupBgroupC0E0Ghomepage_category1_394__a1__c-1024
        cssVersion	f6c6d196
        _lx_utm	utm_source%3D60374%26utm_medium%3Dandroid%26utm_term%3D1000000202%26utm_content%3D861735030994726%26utm_campaign%3DAgroupBgroupC0E0Ghomepage_category1_394__a1__c-1024
        w_actual_lat	22546510
        w_actual_lng	113948770
        w_latlng	22546510,113948770
        w_visitid	eb15bab3-77ac-4ef1-a894-cc0595f699c4
        channelType	{%22mtjj%22:%220%22}

        """

    def get_data_params(self,page='0',secondCid='910',lat='22.54651',lng='113.94877',uuid ='450940DF938B12BD8AAC598D8CF4678D69BDD48C75BE2CD34A3C20CA525B3490'):
        params = {}
        params['startIndex'] = str(page) # 页数
        params['sortId'] = ''
        params['navigateType'] = '910'
        params['firstCategoryId'] = '910' # 一级分类id
        params['secondCategoryId'] = secondCid # 二级分类id
        params['multiFilterIds'] = ''
        params['sliderSelectCode'] = ''
        params['sliderSelectMin'] = ''
        params['sliderSelectMax'] = ''
        params['actualLat'] = lat
        params['actualLng'] = lng
        params['initialLat'] = lat
        params['initialLng'] = lng
        params['geoType'] = '2'
        params['rankTraceId'] = ''
        params['uuid'] = uuid
        params['platform'] = '3'
        params['partner'] = '4'
        params['originUrl'] = 'https://h5.waimai.meituan.com/waimai/mindex/kingkong?navigateType=910&firstCategoryId=910&secondCategoryId=910&title=%E7%BE%8E%E9%A3%9F'
        params['riskLevel'] = '71'
        params['optimusCode'] = '10'
        params['wm_latitude'] = str(int(float(lat) * 1000000))
        params['wm_longitude'] = str(int(float(lng) * 1000000))
        params['wm_actual_latitude'] = str(int(float(lat) * 1000000))
        params['wm_actual_longitude'] = str(int(float(lng) * 1000000))
        params['openh5_uuid'] = uuid
        params['_token'] = meituan_encrypt.get__token(self.request_params,refer_url='https://h5.waimai.meituan.com/waimai/mindex/kingkong?navigateType=910&firstCategoryId=910&secondCategoryId=910&title=%E7%BE%8E%E9%A3%9F')
        payload_list = list()
        for param in params:
            payload_list.append(param + '=' + params[param])
        payload = '&'.join(payload_list)
        return quote(payload)
        """
        startIndex	0
        sortId	
        navigateType	910
        firstCategoryId	910
        secondCategoryId	910
        multiFilterIds	
        sliderSelectCode	
        sliderSelectMin	
        sliderSelectMax	
        actualLat	22.54651
        actualLng	113.94877
        initialLat	22.54651
        initialLng	113.94877
        geoType	2
        rankTraceId	
        uuid	450940DF938B12BD8AAC598D8CF4678D69BDD48C75BE2CD34A3C20CA525B3490
        platform	3
        partner	4
        originUrl	https://h5.waimai.meituan.com/waimai/mindex/kingkong?navigateType=910&firstCategoryId=910&secondCategoryId=910&title=%E7%BE%8E%E9%A3%9F
        riskLevel	71
        optimusCode	10
        wm_latitude	22546510
        wm_longitude	113948770
        wm_actual_latitude	22546510
        wm_actual_longitude	113948770
        openh5_uuid	450940DF938B12BD8AAC598D8CF4678D69BDD48C75BE2CD34A3C20CA525B3490
        _token	eJztVtlu6kgQ/RceeIlvp/clEhqBHQgEsgCBhNEVcsDBLLbBNiRkNP8+ZZsl907e52VQBNVV1ae206X8VYqb09IVwURhYpV2Xly6KhGEkSxZpTQBi9CGSK45l4RapclJpySmHAvQvcYDp3T1J5PYEor+zBRdOOcKyfFP6yxRDn+ZRxMcSn6arpOry0tfoHd3HrhzFHjzdOuGaBIFl4XqMpiHU+/jj3S/9ipwDsdrd+aVJ74bht6qEqSLRXmbBuMk2sYTryIxU7z8VnHDaRzNp+WVm1YoRYIbQTkYOaQsWHkVziqEMGQ404ZhrDQ3NMcJvOl8G5zuZ6rUi4MKwfmHYlqGJiXzKByHbuCBHpqVaTPPSRSmXphWtCSKCcywMVxRWdjcYO3OZ2GlOouj7bqWf9v4Gjf8KPCyosAl9WZRvCdjZvh47JLxePKDQJvLk3mF4XKQzKe/Y+ezECDDQEh5uwUPLrDh2KkbpmuE1hxdrdrCaEfbdS6VdqSpOQ7XthK1a2o7jFeZTbFdFVTUGDe4vE28GHB+EODAcUbR2gvd9fy7QWUmX1xC4bEbTrz/R/WfjApeVdDPXhXRliCGw+yotATFLJMIAdEIEIkBkWGViYxaAJKN2XALUisEqeGXSwv6mKEuM1T4dY/olFpOc1DgM2I1D/iEsoM+C0GYOJ4gCgG/4lQEOh+kttrNUzyr2WlkMdM8FmUaaS0V0UpYQkiDJBVWli4QBGHDMjXsJZQ75HohEdUGZ36CqYxN1MizVaDiElMEHXUcGSqY4Biz00WFMDcM9h4+R9SIMciIAoNItg8hNCXIGCk0NJmc/BTKkhUKGQFUlUWaR5MWROQxhFSIck6+RNAY0s2TFRy4+p0aG3QEgxyF1FwTzkUePb8EfFJSnCAVRgyqxphrTfXJizDY6Zic/aSG93WAYYYhoQCbiXPqWqBjlYJgjr5VwyOVApr0pRv/ukeAJpifR6IZglI0++pEjdFffWDwSmuWP/6vTr8OCGrA0G3CsC4SFzjrMZOsqLxoiEGHlnOdLRupmP5qlkiqgjC5nZ8akKErbKA8aTKEg10e2VY4ZexjWnEos2Ath3WFmBGYGHHuCrDvkAS8T/Rbq8GIDwPPzeqbQgt3MAOQVr80NBv5gWS5nWpFvnDwFzPQCSKIQ1sLcGBHYYXK0LdaK182bgf+UwBbAosSJK+1T5fL9OH9s/roP+j2U/jZeVeN10ZnZXuD4WZwrarb12ZvKdWGtm4W1QfG7u3lZBjGy/t4p9zhBDuyRRJSU7y/aDR7T6/BpvrWe5vo3vT2cdn/bGNn97IfPNv7qXqBtbBoN1fdtmaxN3qcNI0z483X/YYQ318tBW229ngr5bzXSR82DiOt4WengyMzuvaEv5T9YNHp1T92w9Hm2e6peGfPNvtdU8ZqtFxePBN/PSD9t+YmokNn8xmtuoPY39pRtA4Gt7TaAqyP/qgft+rKrd/seq+Dt8+IOTPTTRtdf63t2uzGh2X2SoI6XJzNu48PUT8U9ZZxzN5bXMjJxc583o5GjRRP9x05uY73USewk1m4bwX+y9PtY43KVnd4663EY++uF/vs5d3zmvMdltPh7WC3jkeNa6m84c3A+WirpBPWRhS3SbtFNuQ+Ft1QPz8tZg+unQyl39f8MqmnifYXpn/hvr1f3PRCfseE80Ac2tB329ZGzO6NcwMPMdgkWCXhlL287WaNdpIqv/T3P1leong=
        """


if __name__ == '__main__':
    # params = '_=1589176024065&X-FOR-WITH=KG1%2B%2B%2BtoHANKNAZ44gHD0nhXFdhDmkXwTsc8u5yC6uXz7p2rhbl%2FTyQXmdm7A0vCgYIego6niozQqNd7CFDSHlIMvdjzsmBEFrKf5%2Bbf%2Br%2Bvuz8uNARNbfmoBjFi9QLYPAo9jTrOEid7YaxWJ9PAHK8MhBaGD3NzlnFirbuOZCm%2FftkAUxtTnxCcVPk1do5FzWNYKdgSNkbYbBINO%2Bfhlw%3D%3D'
    # refer = 'https://h5.waimai.meituan.com/waimai/mindex/kingkong?navigateType=910&firstCategoryId=910&secondCategoryId=910&title=%E7%BE%8E%E9%A3%9F'
    # token = meituan_encrypt.get__token(params,refer)
    # print(token)
    mt = meituan_request()
    mt.request_secondCategory_list()