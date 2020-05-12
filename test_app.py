# -*- coding: UTF-8 -*-
import base64
import hashlib
import hmac
import json
import random
import time
import uuid
from pprint import pprint
from Crypto.Cipher import AES
from tornado.escape import url_escape, url_unescape
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from urllib.parse import quote, unquote
import requests

url2 = "http://wmapi.meituan.com/api/v6/poi/filter?utm_medium=android&utm_content=861735030994726&utm_term=50304&utm_source=1040&ci=30&utm_campaign=AwaimaiBwaimaiGhomepage&uuid=450940DF938B12BD8AAC598D8CF4678D69BDD48C75BE2CD34A3C20CA525B3490&__skck=6a375bce8c66a0dc293860dfa83833ef&__skts=1588918923023&__skua=d41d8cd98f00b204e9800998ecf8427e&__skno=fe6b0619-00da-4d99-bb0c-f941c911505a&__skcy=%2BdJGSuGINBHtCCH0H32hGnIbUe4%3D"

payload2 = "wm_logintoken=&request_id=BA540C03-6113-49BE-B131-8101BC60B829&poilist_mt_cityid=30&wm_actual_longitude=113944290&wm_actual_latitude=22548953&req_time=1588918923085&last_wm_poi_id=0&wm_did=861735030994726&userid=0&wm_longitude=113944290&wm_channel=1040&poilist_wm_cityid=440300&sort_type=0&page_size=20&push_token=dpshc20654e2afb01c20681baeffb8e61c55atpu&load_type=3&category_type=0&navigate_type=0&wm_appversion=5.3.4&wm_latitude=22548953&wm_mac=02%3A00%3A00%3A00%3A00%3A00&longitude=113944290&wm_ctype=android&second_category_type=0&wm_visitid=dd4c9aa5-5167-47d2-bdfe-bb18582a7fa4&seq_id=330&wm_dversion=23_6.0.1&wm_uuid=450940DF938B12BD8AAC598D8CF4678D69BDD48C75BE2CD34A3C20CA525B3490&wm_dtype=Redmi%20Note%203&page_index=1&latitude=22548953&filter_type=0&trace_tag=%7B%22action%22%3A%22pull_up%22%2C%22src_page%22%3A%22p_homepage%22%2C%22src_block%22%3A%22b_pull_up%22%2C%22tgt_page%22%3A%22p_homepage%22%2C%22req_time%22%3A%221588918923084%22%2C%22tgt_block%22%3A%22%5B%5C%22b_poilist%5C%22%5D%22%7D&waimai_sign=LN8U%2BXv593P4s0z53Vr7a%2FvwvV%2BMymLlMK5nyERLRwGui17L6A7Lh3%2FAnIMwEBprBZHF2TLScn%2FukfPjCF3p87%2FVAqsVtcJn17BaP3%2FyAK3JMASPEKkSnPXEqkeKnvQH07ITgyCISe5L%2BvSgvRJnudyTiBcFUQhirMYkPwnsDzM%3D"

headers = {
    # '__skua': 'd41d8cd98f00b204e9800998ecf8427e',
    # '__skck': '6a375bce8c66a0dc293860dfa83833ef',
    # '__skts': '1588918923023',
    # '__skcy': '+dJGSuGINBHtCCH0H32hGnIbUe4=',
    # '__skno': 'fe6b0619-00da-4d99-bb0c-f941c911505a',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; Redmi Note 3 MIUI/6.10.13)',
    'Host': 'wmapi.meituan.com',
    'Accept-Encoding': 'gzip',
    # 'Content-Length': '1208',
    'Connection': 'keep-alive'
}
#
# response = requests.request("POST", url2, headers=headers, data = payload2)
# response_json = json.loads(response.text)
# pprint(response_json)


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


# 美团外卖的基础属性
def waimai_param():
    userAgent = ('Redmi Note 3','Dalvik/2.1.0 (Linux; U; Android 6.0.1; Redmi Note 3 MIUI/6.10.13-{}-wandoujia') # 写死
    utm_content = '861735030994726' # IMEI
    kwargs = dict()
    kwargs["__skck"] = hashlib.md5(str(int(time.time()) - random.randint(0, 999)).encode()).hexdigest()
    kwargs["__skua"] = hashlib.md5(userAgent[1].encode()).hexdigest()
    kwargs["push_token"] = "dpsh" + hashlib.md5(
        str(int(time.time()) - random.randint(0, 999)).encode()).hexdigest() + "atpu"
    kwargs["ci"] = '30' #random.randint(1, 64)
    kwargs["request_id"] = str(uuid.uuid4()).upper()
    kwargs["wm_mac"] = "%20".join([
        "%3A".join(["%.2x" % random.randint(17, 254) for _ in range(6)])
        for _ in range(1)])
    kwargs["utm_source"] = str(random.randint(1009, 1040))
    kwargs["utm_content"] = utm_content  # IMEI
    kwargs["req_time"] = str(int(time.time() * 1000) - random.randint(20, 60))
    kwargs["__skts"] = str(int(time.time() * 1000))
    kwargs["wm_visitid"] = str(uuid.uuid4())
    kwargs["wm_dtype"] = quote(userAgent[0])
    kwargs["uuid"] = '450940DF938B12BD8AAC598D8CF4678D69BDD48C75BE2CD34A3C20CA525B3490'
    kwargs["seq_id"] = random.randint(200, 1000)
    kwargs["header_agent"] = userAgent[1]
    kwargs["req_time"] = str(int(time.time() * 1000) - random.randint(20, 60))
    kwargs["__skts"] = str(int(time.time() * 1000))
    kwargs["wm_seq"] = random.randint(3, 30)
    kwargs["__skno"] = str(uuid.uuid4())
    kwargs['vm_mac'] = '7b%3A8c%3A74%3A17%3Ac6%3Ad5'
    return kwargs

# params_dict = [{i.split('=')[0]:i.split('=')[1]} for i in url_params.split('&')]
# print(params_dict)
# def get_url_params(url_params_str):
#     kwargs = waimai_param()
#     # skcy少
#     url_params_str.fomat(
#         IMEI=kwargs['utm_source'],
#         utm_source=kwargs['utm_source'],
#         ci=kwargs['ci'],
#         uuid=kwargs['uuid'],
#         skck=kwargs['__skck'],
#         skts=kwargs['__skts'],
#         skua=kwargs['__skua'],
#         skno=kwargs['__skno']
#     )


 # 获取加密的body
def get_encrypt_body(url, body, paratem_type, index_key='/api', **kwargs):
    kwargs["waimai_sign"] = get_waimai_sign(url, kwargs["utm_content"], kwargs["req_time"], kwargs["seq_id"],
                                                 index_key)
    request_parameter = paratem_type.format(**kwargs)
    post_parameter = body % kwargs
    post_parameter_target_arg = {'action':'pull_up','src_page':'p_homepage','src_block':'b_pull_up','tgt_page':'p_homepage','req_time':'1','tgt_block':'[\"b_poilist\"]'}
    post_parameter_target_arg['req_time'] = kwargs['req_time']
    post_parameter += '&trace_tag=' + url_escape(json.dumps(post_parameter_target_arg)).replace('+','') + '&waimai_sign=' + kwargs['waimai_sign']
    encrypt_result = get_skcy(url, "&".join([request_parameter, post_parameter]))
    return request_parameter, post_parameter, encrypt_result


def get_waimai_sign(url, imei, timestamp, count, index_key='/api'):

    rsa_key = int('''12083981869016806625904160907021092817445343978719657636691758456108571763332438804479335640035355
                     12215860668516972633211372985530120569151471217981967569519070010305215906205405249960933023944218
                     52427157555311661120915880014829628140915206376203479818468758857955965652575963285609268917035335
                     146444958477161'''.replace('\n', '').replace(' ', ''))
    sign_string = "/".join([url[url.index(index_key):], imei, str(timestamp), str(count)])
    print(sign_string)
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


def get_skcy(url, param, method='POST'):
    sha1_key = b'83c96b209eb9731bab61dd03dc34e1afY4yBJhR5whBO3j8lGOkXJQ=='  # 9.4.2
    sha1_key = b'Tb6yTwgSEvbLgLtguw21Q80dR8atTLZ9gbOyX3m9FB0FMGWI60SALA=='  # 10.0.202
    param += "&__sksc=http"
    raw_string = "&".join(sorted([
        "%s=%s" % (s.split("=")[0], s.split("=")[1] if len(s.split("=")) > 1 else "")
        for s in param.split("&")]))
    before = " ".join([method, url, raw_string]).encode()
    return url_escape(base64.b64encode(hmac.new(sha1_key, before, hashlib.sha1).digest()).rstrip())


kwargs = waimai_param()
url_params = 'utm_medium=android&utm_content={utm_content}&utm_term=50304&utm_source={utm_source}&ci={ci}&utm_campaign=AwaimaiBwaimaiGhomepage&uuid={uuid}&__skck={__skck}&__skts={__skts}&__skua={__skua}&__skno={__skno}' # &__skcy=%2BdJGSuGINBHtCCH0H32hGnIbUe4%3D'
payload = 'wm_logintoken=&request_id=%(request_id)s&poilist_mt_cityid=30&wm_actual_longitude=113944290&wm_actual_latitude=22548953&req_time=%(req_time)s&last_wm_poi_id=0&wm_did=861735030994726&userid=0&wm_longitude=113944290&wm_channel=1040&poilist_wm_cityid=440300&sort_type=0&page_size=20&push_token=%(push_token)s&load_type=3&category_type=0&navigate_type=0&wm_appversion=5.3.4&wm_latitude=22548953&wm_mac=%(wm_mac)s&longitude=113944290&wm_ctype=android&second_category_type=0&wm_visitid=%(wm_visitid)s&seq_id=%(seq_id)s&wm_dversion=23_6.0.1&wm_uuid=%(uuid)s&wm_dtype=%(wm_dtype)s&page_index=1&latitude=22548953&filter_type=0' #&waimai_sign={waimai_sign}'
url = 'http://wmapi.meituan.com/api/v6/poi/filter'
encrypt_body = get_encrypt_body(url, body=payload, paratem_type=url_params, index_key='/wmapi', **kwargs)

raw_url = url + '?' + encrypt_body[0] + '&__skcy={0}'.format(encrypt_body[2])
kwargs["__skcy"] = encrypt_body[2]
headers["User-Agent"] = kwargs['header_agent'].format(kwargs['utm_content'])
# headers["Content-Length"] = str(len(encrypt_body[1]))
# print(headers)
# print(raw_url)
# print(encrypt_body[1])
# print(len(encrypt_body[1]))
# print(str(len(unquote(encrypt_body[1]))))
pprint(headers)
response = requests.post(url=raw_url,headers=headers,data=encrypt_body[1])
pprint(response.text)
