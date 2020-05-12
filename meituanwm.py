import copy

from Api.nanqizhang.common.func import genMassImei, genMassImsi, random_str
from tornado import httpclient
from Crypto.Cipher import AES
from tornado.escape import url_escape, url_unescape
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from urllib.parse import quote, unquote
import base64

import re
import datetime
import hashlib
import hmac
import zlib
import random
import uuid
import time
import string


def user_agent():
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


msid = str(int(time.time() * 1000))


class meituan_encrypt:

    def __init__(self, UID=None, new_param=None, debug=False):
        self.uid = UID if UID else ''.join(random.sample("%s%s" % (string.ascii_uppercase, string.digits), 32)) + \
                                   ''.join(random.sample("%s%s" % (string.ascii_uppercase, string.digits), 32))
        self.new_param = self.new_param = new_param if new_param else {}
        self.debug = debug
        self.all_param = dict()

    @staticmethod
    def get_search_id(string):
        uid_hash = str(abs(hash_code().get(string)))
        timestamp = str(int(time.time()*1000))[4:]
        return timestamp+uid_hash

    @staticmethod
    def get_meituan_request(url, body, lat, lon, encrypt_class, param, header, proxy=False, old=False, **kwargs):

        if old:
            lat = int(lat) - random.randint(1960, 9960)
            lon = int(lon) - random.randint(17522, 97522)

        kwargs["wm_latitude"] = lat
        kwargs["latitude"] = lat
        kwargs["wm_longitude"] = lon
        kwargs["longitude"] = lon

        kwargs.update(encrypt_class.meituan_param())
        encrypt_class.all_param.update(kwargs)

        encrypt_body = encrypt_class.get_encrypt_body(url, body, paratem_type=param, index_key='/mtapi', **kwargs)
        raw_url = url + "?" + encrypt_body[0] + '&__skcy={0}'.format(encrypt_body[2])
        kwargs["__skcy"] = encrypt_body[2]
        if type(header) == dict:
            headers = copy.copy(header)
            headers["User-Agent"] = kwargs["header_agent"].format(kwargs["utm_content"])
            headers["Content-Length"] = str(len(encrypt_body[1]))
            headers["siua"] = encrypt_class.get_siua(**kwargs)
            headers["pragma-mtid"] = kwargs["utm_content"]
            headers["pragma-os"] = kwargs["pragma-os"]
            headers["mtgdid"] = "AAAAAAAAAAAAA{}-{}".format(random_str(50), random_str(35)) \
                if not kwargs.get("mtgdid") else kwargs["mtgdid"]

            headers["M-SHARK-TRACEID"] = "101" + encrypt_class.uid + str(uuid.uuid4()).replace("-", "")[:6] + str(
                int(time.time() * 1000)) + str(uuid.uuid4()).replace("-", "")[:6]
        else:
            headers = header
        if proxy:
            return raw_url, encrypt_body[1], headers

        return httpclient.HTTPRequest(raw_url, method='POST', body=encrypt_body[1], headers=headers)

    @staticmethod
    def get_waimai_sign(url, imei, timestamp, count, index_key='/api'):
        rsa_key = int('''12083981869016806625904160907021092817445343978719657636691758456108571763332438804479335640035355
                         12215860668516972633211372985530120569151471217981967569519070010305215906205405249960933023944218
                         52427157555311661120915880014829628140915206376203479818468758857955965652575963285609268917035335
                         146444958477161'''.replace('\n', '').replace(' ', ''))
        sign_string = "/".join([url[url.index(index_key):], imei, str(timestamp), str(count)])
        encrypt_result = b''
        length = len(sign_string)
        i2 = 0
        i = 0
        while length - i2 > 0:
            Pkey = RSA.construct((rsa_key, 65537))
            if length - i2:
                encrypt_result += PKCS1_v1_5.new(Pkey).encrypt(sign_string[i2:117].encode())
            else:
                encrypt_result += PKCS1_v1_5.new(Pkey).encrypt(sign_string[i2:(length - i2)].encode())
            i2 = i + 1
            i3 = i2
            i2 *= 117
            i = i3
        return url_escape(base64.b64encode(encrypt_result)) + "%0A"

    @staticmethod
    def get_skcy(url, param, method='POST'):
        sha1_key = b'83c96b209eb9731bab61dd03dc34e1afY4yBJhR5whBO3j8lGOkXJQ=='  # 9.4.2
        sha1_key = b'Tb6yTwgSEvbLgLtguw21Q80dR8atTLZ9gbOyX3m9FB0FMGWI60SALA=='  # 10.0.202
        param += "&__sksc=http"
        raw_string = "&".join(sorted([
            "%s=%s" % (s.split("=")[0], s.split("=")[1] if len(s.split("=")) > 1 else "")
            for s in param.split("&")]))
        before = " ".join([method, url, raw_string]).encode()
        return url_escape(base64.b64encode(hmac.new(sha1_key, before, hashlib.sha1).digest()).rstrip())

    # @classmethod
    def get_siua(self, **kwargs):
        # wifi_name = "LIEbao-" + str(random.randint(23333, 66666))
        kwargs["wifi_name"] = random_str(random.randint(6, 7))
        kwargs["wifi_mac"] = ":".join(["%.2x" % random.randint(66, 233) for _ in range(6)])
        kwargs["brand_name"] = random.choice(
            ["ALCATEL", "ERICSSON", "PHILIPS", "MOTOROLA", "NOKIA", "SIEMENS", "LG", "NEC", "MITSUBISHI", "SAMSUNG",
             "SANYO", "PANASONIC", "SONY", "SONYERICSSON", "CECT", "TCL", "BIRD", "EASTCOM", "HAIER", "HISENSE",
             "KONKA", "KEJIAN", "LEGEND", "SOUTEC", "SHOUXIN", "STARCOM", "TOP", "XOCECO", "AMOISONIC", "PANDA", "ZTE"])
        kwargs["brand_num"] = str(random.randint(1, 2))
        kwargs["unkown"] = str(random.randint(20500, 20690))
        kwargs["wmac"] = url_unescape(kwargs["wm_mac"]).upper()
        kwargs["jidai"] = "MOLY.LR%d.W%d.MD.MP.V%d.%d.P%d" % (
            random.randint(10, 20),
            random.randint(1333, 2333),
            random.randint(10, 20),
            random.randint(10, 20),
            random.randint(23, 66),
            # random.randint(2002, 2018), random.randint(1, 12), random.randint(1, 27), random.randint(0, 24), random.randint(0, 60),
        )
        chuliqi = random.choice(["apq", "msm"])
        kwargs["chuliqi"] = chuliqi + "8" + str(random.randint(799, 999))
        kwargs["unkown1"] = chuliqi.upper() + str(random.randint(8056, 9956))
        kwargs["phone_name"] = ''.join(random.sample("%s" % string.ascii_lowercase, 7))
        kwargs["unknow123"] = ''.join(random.sample("%s" % string.ascii_uppercase, 4))+str(random.randint(23,66))
        # kwargs["unknow123"] = "MRA%dK" % random.randint(10, 95)
        kwargs["unknow1234"] = random_str(4)
        kwargs["unknow12345"] = random_str(random.randint(4, 5))
        kwargs["batteryLevel"] = str(random.randint(10, 100))

        kwargs["suiji"] = 'mt' + str(random.randint(6666, 9999))
        kwargs["suiji"] = "mt6797"
        kwargs["suiji_upper"] = kwargs["suiji"].upper()+"M"
        if not self.new_param or not self.new_param.get("siua"):
            siua_raw_string = '1.0}}unknown|Xiaomi|%(phone_name)s|%(phone_name)s|%(unknow123)s|zh|CN|Xiaomi|Redmi Note 4|6.0|23|release-keys|Xiaomi/nikel/nikel:6.0/%(unknow123)s/8.4.15:user/release-keys|mt6797|c3-miui-ota-bd04.bj|user|%(phone_name)s|arm64-v8a||%(phone_name)s-user 6.0 %(unknow123)s 8.4.15 release-keys|1|0|}}' \
                          'none|mtp|mtp|%(jidai)s|android reference-ril 1.0|wlan0|READY||1|1|1|1|1|1|1|1|1|1|1|1}}' \
                          'AArch64 Processor rev 4 (aarch64)|Qualcomm Technologies, Inc MSM%(unkown1)s|8|ICM%(unkown)s Accelerometer|InvenSense|Gravity|QTI}}' \
                          '%(utm_content)s|-|-|%(height_width)s||%(phone_memory)sGB|%(wmac)s||wifi}}' \
                          '-|70|1|0|0|-|%(random_uuid1)s}}' \
                          '0|0|0|AAAA}}' \
                          'Android|%(package_name)s|%(version)s|%(sdk)s|-|%(now_time)s}}' \
                          '0.0|0.0|%(wifi_name)s|%(wifi_mac)s|1|%(rssi)s||-|-|}}'
#             siua_raw_string = '''1.0}}
# msm8916|Xiaomi|gucci|gucci|KTU84P|zh|CN|Xiaomi|gucci|4.4.4|19|release-keys|Xiaomi/gucci/gucci:4.4.4/KTU84P/V6.3.6.0.KHKCNBL:user/release-keys|qcom|zc-miui-ota-bd27.bj|user|gucci|armeabi-v7a|armeabi|gucci-user 4.4.4 KTU84P V6.3.6.0.KHKCNBL release-keys|1|0|}}
# none|mtp|mtp|%(jidai)s|android reference-ril 1.0|wlan0|READY||1|1|1|1|1|1|1|1|1|1|1|1}}
# AArch64 Processor rev 4 (aarch64)|Qualcomm Technologies, Inc %(unkown1)s|8|ICM%(unkown)s Accelerometer|InvenSense|Gravity|QTI}}
# %(utm_content)s|46001%(h0123abcd)s|-|%(height)s*%(width)s|%(phone_memory)sGB|%(phone_memory)sGB|%(wmac)s|46001|wifi}}
# -|%(batteryLevel)s|1.0|0|0|%(random_uuid)s|%(random_uuid1)s}}
# 0|0|0|AAAA}}
# Android|%(package_name)s|%(version)s|%(sdk)s|-|%(now_time)s}}
# 0.0|0.0|%(wifi_name)s|%(wifi_mac)s|1|%(rssi)s|460|01|-|}}'''.replace('\n', '')
        else:
            siua_raw_string = self.aesDecrypt(self.new_param["siua"])
            siua_raw_string = re.sub('\w{8}-\w{4}-\w{4}-\w{4}-\w{12}\}', kwargs["random_uuid1"]+"}", siua_raw_string)
            siua_raw_string = re.sub('\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}:\d{3}', kwargs["now_time"], siua_raw_string)
            # siua_raw_string = re.sub('-\|\d+\*\d+\|.*?\|\d+GB\|', '-|%(height_width)s||%(phone_memory)sGB|'%kwargs, siua_raw_string)
            # siua_raw_string = re.sub('\w+:\w+:\w+:\w+:\w+:\w+\|46001\|wifi', '%(wmac)s|460%(mnc)s|wifi'%kwargs, siua_raw_string)
            # siua_raw_string = re.sub('460\|01', '460|%(mnc)s'%kwargs, siua_raw_string)
            # utm_content = re.search("\}(\d{8,})\|", siua_raw_string)
            # siua_raw_string = siua_raw_string.replace(utm_content.group(1), kwargs["utm_content"])
            # siua_raw_string = siua_raw_string.replace('9.4.2', '10.0.202')

        return self.aesEncrypt(zlib.compress((siua_raw_string % kwargs).encode()))

    # 获取加密的body
    @classmethod
    def get_encrypt_body(self, url, body, paratem_type, index_key='/api', **kwargs):
        kwargs["waimai_sign"] = self.get_waimai_sign(url, kwargs["utm_content"], kwargs["req_time"], kwargs["seq_id"],
                                                     index_key)
        request_parameter = paratem_type.format(**kwargs)
        post_parameter = body.format(**kwargs)

        encrypt_result = self.get_skcy(url, "&".join([request_parameter, post_parameter]))
        return request_parameter, post_parameter, encrypt_result

    # 加密字符串成siua的参数
    @staticmethod
    def aesEncrypt(text):
        text = text + (chr((16 - (len(text) % 16))).encode() * (16 - (len(text) % 16)))
        encryptor = AES.new(b"meituan0sankuai1", 2, b'0102030405060708')
        ciphertext = encryptor.encrypt(text)
        return base64.b64encode(ciphertext).decode()

    # 解密看siua的原本字符串
    @staticmethod
    def aesDecrypt(ciphertext):
        real_bytes = base64.b64decode(ciphertext)
        encryptor = AES.new(b"meituan0sankuai1", 2, b"0102030405060708")
        detext = encryptor.decrypt(real_bytes)
        return zlib.decompress(detext).decode()

    # 美团外卖的基础属性
    def waimai_param(self):
        userAgent = user_agent()
        utm_content = genMassImei()
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

    # 美团的基础属性
    def meituan_param(self):
        userAgent = user_agent()
        kwargs = dict()
        utm_content = genMassImsi()
        # 美团的基本参数
        kwargs["__skck"] = hashlib.md5(str(time.time() - random.randint(0, 999)).encode()).hexdigest()
        kwargs["__skua"] = hashlib.md5(userAgent[1].encode()).hexdigest()
        kwargs["push_token"] = "dpsh" + hashlib.md5(
            str(time.time() - random.randint(0, 999)).encode()).hexdigest() + "atpu"
        kwargs["ci"] = random.randint(1, 64)
        kwargs["request_id"] = str(uuid.uuid4()).upper()
        kwargs["msid"] = utm_content + msid
        kwargs["wm_mac"] = "%20".join([
            "%3A".join(["%.2x" % random.randint(17,254) for _ in range(6)])
            for _ in range(1)])
        kwargs["utm_source"] = str(random.randint(1009, 1040))
        kwargs["utm_content"] = utm_content  # IMEI
        kwargs["utm_term"] = str(random.randint(500, 600))
        kwargs["wm_visitid"] = str(uuid.uuid4())
        kwargs["wm_dtype"] = userAgent[0]
        kwargs["uuid"] = self.uid

        kwargs["utm_campaign"] = 'AgroupBgroupC0E0Ghomepage'
        kwargs["req_time"] = str(int(datetime.datetime.now().timestamp() * 1000))
        kwargs["__skts"] = str(int(datetime.datetime.now().timestamp() * 1000))
        kwargs["wm_seq"] = random.randint(3, 30)

        kwargs["seq_id"] = kwargs["wm_seq"]
        kwargs["__reqTraceID"] = str(uuid.uuid4())
        kwargs["__skno"] = str(uuid.uuid4())

        kwargs.update(self.new_param)
        self.uid = kwargs["uuid"]

        # siua 的参数

        # SDK版本号
        sdk, android_version = random.choice([
            (21, "5.0.1"), (22, "5.1.1"),
            (23, "6.0.1"), (24, "7.0.1"),
            (26, "8.0.1"), (25, "7.1.1"),
        ])
        sdk, android_version = (sdk, android_version) if not self.new_param.get("wm_dversion") else self.new_param[
            "wm_dversion"].split("_")

        # 请求头
        kwargs["header_agent"] = userAgent[1] \
            if not self.new_param.get("header_agent") else self.new_param["header_agent"]
        kwargs["pragma-os"] = "MApi 1.1 com.sankuai.meituan 10.0.202 wandoujia %s; Android %s" % (
            userAgent[0].replace('%20', '_'), android_version) \
            if not self.new_param.get("pragma-os") else self.new_param["pragma-os"]

        kwargs["wm_dversion"] = "{}_{}".format(sdk, android_version)

        base_info = {
            "rssi": random.randint(-70, 0),  # wifi信号强弱 Rssi
            "mnc": random.choice(["00", "02", "04", "07",  "09", "06", "03", "05", "11"]),  # 运营商MNC
            # "mnc": random.choice(["02"]),  # 运营商MNC
            "bssid": ":".join(
                ["".join(random.sample("%s%s" % (string.digits, "abc"), 2)) for _
                 in range(6)]),  # 路由器mac
            "ssid": "".join(
                random.sample("%s%s" % (string.ascii_uppercase, string.ascii_lowercase), random.randint(5, 10))),
            # wifi名称
            "now_time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')[:-3],  # 当前时间
            "version": '10.0.202',  # 美团APP版本号
            "package_name": "com.sankuai.meituan",  # PackageName
            "is_root": 0,
            "has_MalWare": 0,
            "is_Emulator": 0,
            "Emulator_info": 'AAAA',  # 是否root,是否有恶意软件,是否模拟器,模拟器信息
            "random_uuid": (lambda: str(uuid.uuid4()))(),
            "random_uuid1": (lambda: str(uuid.uuid4()))(),
            "phone_memory": str(random.randint(45, 64) - 8) if not self.debug else "12",  # -8减去系统内存
            "height_width": random.choice(["1280*720", "1776*1080", "1600*900", "960*540"])
            if self.debug else "1980*1080",  # Height, Width, view的大小

            "h0123abcd": random_str(10, random_type='num'),  # 09+H0H1H2H3+ABCD

            "brand": random.choice(["Xiaomi"]),  # 手机型号版本

            # "utm_content": genMassImei(),  # did utm_content
            "sdk": sdk,
            "android_version": android_version,
            "lon": "0.0",
            "lat": "0.0"
        }
        kwargs.update(base_info)

        return kwargs


class meituan_qq:

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


    @staticmethod
    def response_format(data, font_id):
        font_dict = {
            "b05eaa31": {
                "&#xe48d;": "7",
                "&#xf005;": "8",
                "&#xefdb;": "4",
                "&#xea75;": "0",
                "&#xf5ac;": "6",
                "&#xea07;": "2",
                "&#xf858;": "5",
                "&#xeed4;": "3",
                "&#xf796;": "9",
                "&#xeb60;": "1"
            },
            "c0a53bab": {
                "&#xe2da;": "1",
                "&#xe256;": "6",
                "&#xf5d9;": "2",
                "&#xe78b;": "5",
                "&#xf0e9;": "4",
                "&#xea31;": "9",
                "&#xe3eb;": "8",
                "&#xee51;": "0",
                "&#xe170;": "7",
                "&#xec95;": "3",
            }
        }
        real_response = data.decode()
        if type(font_id) == dict:
            real_font_dict = font_id
        else:
            real_font_dict = font_dict[font_id]
        for key, value in real_font_dict.items():
            real_response = real_response.replace(key, value)
        return real_response

    @staticmethod
    def format_token(data):
        try:
            lxsdk_s = re.findall("_lxsdk_s=(.*?)%7C", data)[0]
            iuuid = re.findall("iuuid=(\d+)", data)[0]
            ri = re.findall("ri=(\d+)", data)
            rv = re.findall("rv=(\d+)", data)
            mtUserId = re.findall("mtUserId=(\d+)", data)[0]
            return {
                "_lxsdk_s": lxsdk_s,
                "iuuid": iuuid,
                "ri": ri[0] if ri else "",
                "rv": rv[0] if rv else "",
                "mtUserId": mtUserId
            }
        except:
            return {}

    def get_xforwith(self):
        ts = str(int(1000 * time.time()) - random.randint(2333, 66666))
        cts = str(int(1000 * time.time()))
        xforwith = '{"ts":%s,"cts":%s,"brVD":[360,518],"brR":[[360,640],[360,640],24,24],"aM":""}' % (ts, cts)
        padding_num = 16 - (len(xforwith) % 16)
        real_data = xforwith + chr(padding_num) * padding_num
        return base64.b64encode(
            AES.new(b"jvzempodf8f9anyt", mode=AES.MODE_CBC, IV=b"jvzempodf8f9anyt").encrypt(
                real_data.encode())).decode()

    def get_token(self, data):
        return base64.b64encode(zlib.compress(data.encode())).decode()

    def get__token(self, request_param, refer_url, _type):
        sign = self.get_token('"%s"' % "&".join([unquote(value) for value in sorted(request_param.split('&'))]))
        ts = str(int(1000 * time.time()) - random.randint(2333, 66666))
        cts = str(int(1000 * time.time()))
        tmp_dict = {"ts": ts, "cts": cts, "sign": sign, "referer": refer_url}
        tmp_dict.update(self.get_locus(_type))
        token = '{"rId":100023,"ver":"1.0.6","ts":%(ts)s,"cts":%(cts)s,' \
                '"brVD":[360,518],"brR":[[360,640],[360,640],24,24],' \
                '"bI":["%(referer)s",""],"mT":%(mT)s,"kT":[],"aT":%(aT)s,"tT":%(tT)s,"aM":"",' \
                '"sign":"%(sign)s"}' % tmp_dict
        _token = quote(self.get_token(token))
        return "&_token={_token}".format(_token=_token)

    def get_request(self, url, request_param, header, refer_url, _type, token_json, method='GET', **kwargs):
        _header = copy.deepcopy(header)
        cookies_param = {
            "lat": kwargs["lat"],
            "lon": kwargs["lon"],
            "randomCount": str(random.randint(23, 666)),
            # "city": quote(random.choice(["深圳市", "上海市", "武汉市", "北京市", "广州市", "杭州市", "石家庄市", "天津市"]))
        }
        real_cookies = _header["Cookie"] if not token_json.get("cookies") else token_json["cookies"]
        _header["Cookie"] = real_cookies.format_map(cookies_param)
        real_param = request_param.format_map(kwargs)
        _token = self.get__token(real_param, refer_url, _type)
        if method == 'GET':
            real_url = url + real_param + _token + "&_={timstamp}".format(timstamp=str(int(time.time() * 1000)))
            body = None
        else:
            real_url = url
            body = real_param + _token
        _header["Referer"] = refer_url
        _header["X-FOR-WITH"] = self.get_xforwith()
        if token_json.get("user-agent"):
            _header["User-Agent"] = token_json["user-agent"]
        if method == "POST":
            return real_url, _header, body
        else:
            return real_url, _header


class hash_code:

    @staticmethod
    def convert_n_bytes(n, b):
        bits = b*8
        return (n + 2**(bits-1)) % 2**bits - 2**(bits-1)

    def convert_4_bytes(self, n):
        return self.convert_n_bytes(n, 4)

    def get(self, s):
        h = 0
        n = len(s)
        for i, c in enumerate(s):
            h = h + ord(c)*31**(n-1-i)
        return self.convert_4_bytes(h)
