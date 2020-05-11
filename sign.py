import base64
import json
import zlib
from gzip import GzipFile
from io import StringIO
from urllib import parse
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
