import base64
import json
import zlib
from gzip import GzipFile
from io import StringIO
from urllib import parse
from urllib.parse import unquote, quote

parms_dict = {'areaId': "0",
'cateId': "11",
'cityName': "深圳",
'dinnerCountAttrId': "",
'optimusCode': "10",
'originUrl': "https://sz.meituan.com/meishi/c11/",
'page': "1",
'partner': "126",
'platform': "1",
'riskLevel': "1",
'sort': "",
'userId': "",
'uuid': "0f0502af-a9f9-46f1-9ca7-418a1f34bb39"
}

parms_array = ["areaId", "cateId", "cityName", "dinnerCountAttrId", "optimusCode", "originUrl", "page", "partner", "platform", "riskLevel", "sort", "userId", "uuid"]

def ij(parms_dict):
    new_list = []
    for parms in parms_array:
        if parms == 'token' or parms == '_token':
            continue
        new_list.append(parms + '=' + parms_dict[parms])
    parms_str = '&'.join(new_list)
    jc = iI(parms_str)
    print(type(jc))
    return jc


def iI(parms_str):
    return base64.b64encode(zlib.compress(json.dumps(parms_str, ensure_ascii=False).encode())).decode()

def rest_sign():
    return ij(parms_dict)

if __name__ == '__main__':

    ij(parms_dict)
    s = 'wm_logintoken=&request_id=FA2632FA-A081-44AD-9B41-CDF05EAEAC1E&poilist_mt_cityid=30&wm_actual_longitude=113944290&wm_actual_latitude=22548953&req_time=1588908453045&last_wm_poi_id=0&trace_tag={"src_page":"p_category","tgt_page":"p_category","tgt_block":"[\"b_poilist\"]"}&wm_did=861735030994726&userid=0&wm_longitude=113944290&wm_channel=1040&poilist_wm_cityid=440300&sort_type=0&page_size=20&push_token=dpshc20654e2afb01c20681baeffb8e61c55atpu&load_type=0&category_type=910&navigate_type=910&wm_appversion=5.3.4&wm_latitude=22548953&wm_mac=02:00:00:00:00:00&waimai_sign=A40VLS9qWssTnhY2X3K0V7pTFDDQ8U23wWi4wuvM9IgMRDxrsKYgP7xNktMfvQwY3AlTSHQmJR1ZZJA0Ha9hktpyhhuJjRnj4LVMtBIYTcQtuncnVOyizprMJMgyFRnk3JkxZQRsm48dErqz9ugsCUJnzucxxKTU1dW321jfYsE=&longitude=113944290&preload=1&wm_ctype=android&second_category_type=101792&wm_visitid=dd4c9aa5-5167-47d2-bdfe-bb18582a7fa4&seq_id=196&wm_dversion=23_6.0.1&wm_uuid=450940DF938B12BD8AAC598D8CF4678D69BDD48C75BE2CD34A3C20CA525B3490&wm_dtype=Redmi Note 3&page_index=0&latitude=22548953&filter_type=0&'
    print(len(s))