import hashlib
import json
import random
import time
import uuid
from pprint import pprint

import requests

url = "http://wmapi.meituan.com/api/v6/poi/filter?utm_medium=android&utm_content=861735030994726&utm_term=50304&utm_source=1040&ci=30&utm_campaign=AwaimaiBwaimaiGhomepage&uuid=450940DF938B12BD8AAC598D8CF4678D69BDD48C75BE2CD34A3C20CA525B3490&__skck=6a375bce8c66a0dc293860dfa83833ef&__skts=1588918923023&__skua=d41d8cd98f00b204e9800998ecf8427e&__skno=fe6b0619-00da-4d99-bb0c-f941c911505a&__skcy=%2BdJGSuGINBHtCCH0H32hGnIbUe4%3D"

payload = "wm_logintoken=&request_id=BA540C03-6113-49BE-B131-8101BC60B829&poilist_mt_cityid=30&wm_actual_longitude=113944290&wm_actual_latitude=22548953&req_time=1588918923085&last_wm_poi_id=0&trace_tag=%7B%22action%22%3A%22pull_up%22%2C%22src_page%22%3A%22p_homepage%22%2C%22src_block%22%3A%22b_pull_up%22%2C%22tgt_page%22%3A%22p_homepage%22%2C%22req_time%22%3A%221588918923084%22%2C%22tgt_block%22%3A%22%5B%5C%22b_poilist%5C%22%5D%22%7D&wm_did=861735030994726&userid=0&wm_longitude=113944290&wm_channel=1040&poilist_wm_cityid=440300&sort_type=0&page_size=20&push_token=dpshc20654e2afb01c20681baeffb8e61c55atpu&load_type=3&category_type=0&navigate_type=0&wm_appversion=5.3.4&wm_latitude=22548953&wm_mac=02%3A00%3A00%3A00%3A00%3A00&waimai_sign=LN8U%2BXv593P4s0z53Vr7a%2FvwvV%2BMymLlMK5nyERLRwGui17L6A7Lh3%2FAnIMwEBprBZHF2TLScn%2FukfPjCF3p87%2FVAqsVtcJn17BaP3%2FyAK3JMASPEKkSnPXEqkeKnvQH07ITgyCISe5L%2BvSgvRJnudyTiBcFUQhirMYkPwnsDzM%3D&longitude=113944290&wm_ctype=android&second_category_type=0&wm_visitid=dd4c9aa5-5167-47d2-bdfe-bb18582a7fa4&seq_id=330&wm_dversion=23_6.0.1&wm_uuid=450940DF938B12BD8AAC598D8CF4678D69BDD48C75BE2CD34A3C20CA525B3490&wm_dtype=Redmi%20Note%203&page_index=1&latitude=22548953&filter_type=0"
headers = {
    '__skua': 'd41d8cd98f00b204e9800998ecf8427e',
    '__skck': '6a375bce8c66a0dc293860dfa83833ef',
    '__skts': '1588918923023',
    '__skcy': '+dJGSuGINBHtCCH0H32hGnIbUe4=',
    '__skno': 'fe6b0619-00da-4d99-bb0c-f941c911505a',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; Redmi Note 3 MIUI/6.10.13)',
    'Host': 'wmapi.meituan.com',
    'Accept-Encoding': 'gzip',
    'Content-Length': '1208',
    'Connection': 'keep-alive'
}

response = requests.request("POST", url, headers=headers, data = payload)
response_json = json.loads(response.text)
pprint(response_json)


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
    userAgent = ('Redmi Note 3','Dalvik/2.1.0 (Linux; U; Android 6.0.1; Redmi Note 3 MIUI/6.10.13)') # 写死
    utm_content = '861735030994726' # IMEI
    kwargs = dict()
    kwargs["__skck"] = hashlib.md5(str(int(time.time()) - random.randint(0, 999)).encode()).hexdigest()
    kwargs["__skua"] = hashlib.md5(userAgent[1].encode()).hexdigest()
    kwargs["push_token"] = "dpsh" + hashlib.md5(
        str(int(time.time()) - random.randint(0, 999)).encode()).hexdigest() + "atpu"
    kwargs["ci"] = random.randint(1, 64)
    kwargs["request_id"] = str(uuid.uuid4()).upper()
    kwargs["wm_mac"] = "%20".join([
        "%3A".join(["%.2x" % random.randint(17, 254) for _ in range(6)])
        for _ in range(1)])
    kwargs["utm_source"] = str(random.randint(1009, 1040))
    kwargs["utm_content"] = '861735030994726'  # IMEI
    kwargs["req_time"] = str(int(time.time() * 1000) - random.randint(20, 60))
    kwargs["__skts"] = str(int(time.time() * 1000))
    kwargs["wm_visitid"] = str(uuid.uuid4())
    kwargs["wm_dtype"] = userAgent[0]
    kwargs["uuid"] = utm_content
    kwargs["seq_id"] = random.randint(200, 1000)
    kwargs["header_agent"] = userAgent[1]
    kwargs["req_time"] = str(int(time.time() * 1000) - random.randint(20, 60))
    kwargs["__skts"] = str(int(time.time() * 1000))
    kwargs["wm_seq"] = random.randint(3, 30)
    kwargs["__skno"] = str(uuid.uuid4())
    return kwargs


kwargs = waimai_param()
url_params = 'utm_medium=android&utm_content={IMEI}&utm_term=50304&utm_source={utm_source}&ci={ci}&utm_campaign=AwaimaiBwaimaiGhomepage&uuid={uuid}&__skck=6a375bce8c66a0dc293860dfa83833ef&__skts=1588918923023&__skua=d41d8cd98f00b204e9800998ecf8427e&__skno=fe6b0619-00da-4d99-bb0c-f941c911505a&__skcy=%2BdJGSuGINBHtCCH0H32hGnIbUe4%3D'
params_dict = [{i.split('=')[0]:i.split('=')[1]} for i in url_params.split('&')]
print(params_dict)
def get_url_params():

