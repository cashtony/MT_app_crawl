import json
from pprint import pprint

import requests

payload = 'geoType=2&mtWmPoiId=1112840116809435&source=shoplist&uuid=450940DF938B12BD8AAC598D8CF4678D69BDD48C75BE2CD34A3C20CA525B3490&platform=3&partner=4&originUrl=https%3A%2F%2Fh5.waimai.meituan.com%2Fwaimai%2Fmindex%2Fmenu%3FdpShopId%3D%26mtShopId%3D1112840116809435%26utm_source%3Dwandoujia%26channel%3Dmtjj%26source%3Dshoplist%26initialLat%3D22.544568%26initialLng%3D113.949059%26actualLat%3D22.544568%26actualLng%3D113.949059&riskLevel=71&optimusCode=10&wm_latitude=22544568&wm_longitude=113949059&openh5_uuid=450940DF938B12BD8AAC598D8CF4678D69BDD48C75BE2CD34A3C20CA525B3490'

headers = {
    'Host': 'i.waimai.meituan.com',
    'Accept': 'application/json',
    'Origin': 'https://h5.waimai.meituan.com',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; Redmi Note 3 Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.91 Mobile Safari/537.36 TitansX/11.19.6 KNB/1.2.0 android/6.0.1 mt/com.sankuai.meituan/10.0.202 App/10120/10.0.202 MeituanGroup/10.0.202',
    'Referer': 'https://h5.waimai.meituan.com/waimai/mindex/menu?dpShopId=&mtShopId=1112840116809435&utm_source=wandoujia&channel=mtjj&source=shoplist&initialLat=22.544568&initialLng=113.949059&actualLat=22.544568&actualLng=113.949059',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,en-US;q=0.9',
    'Cookie': 'cityid=30; uuid=450940DF938B12BD8AAC598D8CF4678D69BDD48C75BE2CD34A3C20CA525B3490; utm_medium=android; utm_term=1000000202; utm_content=861735030994726; w_actual_lat=22544568; w_actual_lng=113949059',
    'X-Requested-With': 'com.sankuai.meituan',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Connection': 'keep-alive',
}

url = 'https://i.waimai.meituan.com/openh5/poi/food?_=1589277696918'
# response = requests.post(url,headers=headers,data=payload)
# json_response = json.loads(response.text)
# pprint(json_response)


### 最简化参数  商品
url = 'https://i.waimai.meituan.com/openh5/poi/food?_=1589277696918'
Cookie = {
    'utm_medium':'android',
    'utm_content':'861735030994726'
}
payload = 'mtWmPoiId=1112840116809435&openh5_uuid=450940DF938B12BD8AAC598D8CF4678D69BDD48C75BE2CD34A3C20CA525B3490'

# resp = requests.post(url,headers=headers,data=payload)
# print(resp.text)


### 列表页H5
url = 'https://i.waimai.meituan.com/openh5/channel/kingkongshoplist?_=1589286734004&X-FOR-WITH=hm9%2F921txPSC3FxMG1OojAVTYEv59ddIfmtQPw91s3b7dcOAW%2F%2B6q1eB9peawqDaQwGuDnnvwkFiujW24bh%2By7S1WNkY421KXRGIb4wwvkQ%2B9%2Fv4ourALGBgnQ076lSbivyCwd5YGdWtHNO5vigg11ncGLSn9ZnqQlBd0A9XG4ajwrsEgTGKP3dd0rgCMldlQp3mAkwbRDL6r7idGgZaVw%3D%3D'

headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
headers['Cookie'] = '_lxsdk_cuid=1719b4ea86ac8-0bfd3bb31469b4-5313f6f-1fa400-1719b4ea86ac8; t_lxid=1719b4ea9f2c8-0217437ea7aac-5313f6f-1fa400-1719b4ea9f2c8-tid; ci=1; rvct=1; _hc.v=34edf988-42dc-17df-4202-f3ef87a698df.1587448615; uuid=07a6037edb4f4c68adf4.1588820856.1.0.0; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _ga=GA1.3.806081906.1588820859; __mta=209662893.1588820860537.1588820914260.1588822844430.4; wm_order_channel=default; utm_source=; au_trace_key_net=default; openh5_uuid=07a6037edb4f4c68adf4.1588820856.1.0.0; terminal=i; w_utmz="utm_campaign=(direct)&utm_source=5000&utm_medium=(none)&utm_content=(none)&utm_term=(none)"; w_actual_lat=22555064; w_actual_lng=113941550; openh5_uuid=07a6037edb4f4c68adf4.1588820856.1.0.0; w_visitid=2734c6e1-4465-4eaa-b97e-b6e16ade40f1; channelType={%22default%22:%220%22}; w_latlng=22555064,113941550; w_uuid=TN0VoeXwz57HsjbO105kDc4_XM3vhdSqSclZ6pSWkZcSW2XOldD_ujivlMaEbNiS; cssVersion=70d23f01; _lxsdk_s=17208c66246-bd0-1ea-9d5%7C%7C24'

payload = 'startIndex=0&sortId=&navigateType=910&firstCategoryId=910&secondCategoryId=101792&multiFilterIds=&sliderSelectCode=&sliderSelectMin=&sliderSelectMax=&actualLat=22.555064&actualLng=113.94155&initialLat=22.555064&initialLng=113.94155&geoType=2&rankTraceId=&uuid=07a6037edb4f4c68adf4.1588820856.1.0.0&platform=3&partner=4&originUrl=https%3A%2F%2Fh5.waimai.meituan.com%2Fwaimai%2Fmindex%2Fkingkong%3FnavigateType%3D910%26firstCategoryId%3D910%26secondCategoryId%3D910%26title%3D%25E7%25BE%258E%25E9%25A3%259F&riskLevel=71&optimusCode=10&wm_latitude=22555064&wm_longitude=113941550&wm_actual_latitude=22555064&wm_actual_longitude=113941550&openh5_uuid=07a6037edb4f4c68adf4.1588820856.1.0.0&_token=eJxdkGuPmkAUhv8Lif0ikftlTDYNy63oIgoo6GY%2FoAwwIhdhRLDpfy92ux%2FaZJLnPc%2Bck5yZn0RjxcScoRmJZkiigw0xJ5gZPRMJksDteCPIgJVFieMERiSJ078OAEASx2anEfN3CUgk4KSPp3DH%2Bp0BLE0ytEx%2FkF%2BZHzPLj%2BfZZY1NRIZx3c4pKhNm9wgVEZoVEOFbVM5OVUF9KqpAZQx7Kkdlmldl%2Br2MOpRGGPpDDV8AQ39LUNNidTRp1QxW%2FMe18FSV8X8SI3yBLxNdmrzqE1mf6GCicBNgjK8lxp0K%2F7kToElpFCOET%2FAjZEByT8gk8wn6OZA%2FB0ZGf4m%2Fanv8x7GvRWk5JrgYdnmLb%2FezsnET2VjueFFjLesSDVfXUzJ6F9ZmU%2FYLq79LNjrI67Pk5Orl0rzVoJI6OR4OZlR4sAgDVHjByTN0uy0P%2FtFh%2FJXdl9Og1pe9ygHjpMe%2BUzJx9MBLnYEKK%2FSHvMcK4n2uCKiHEYW1dtNdjTegmMvDVQH7V3jXV9sVVLn9BXOiEww7d5V3%2BhaYMRRgkG%2FfmiX0rsuqRd4m7%2Fkhs6eOgo5d3UpaaClw%2BXCTMj3HtItB7%2F9wZHOtZjejU3Sb9u5d6K6S%2Bpi9Xqf6VgI%2FAsgmjfCQV%2BttAzewaLvMXgx71TbwuopdfYfYtEeMZNLBYxHcwkVan4SIZ9HQXcxzfQnjhuqvlZ8eMlGi3MrZOxs62Tw6zWzuEqumtd55oXw9OpheRNY6XSscfc4t7TqYhb9KqdcStxjHPmtF7H2qqQ1zYYOpuA7qc4RdxCZGOfRJuZFvGhaVm6WATUP8%2Bg2GtPw4'
resp = requests.post(url,headers=headers,data=payload)
print(resp.text)


### 列表页
url = 'https://i.waimai.meituan.com/openh5/channel/kingkongshoplist?_=1589286163907'

payload = 'startIndex=2&navigateType=910&firstCategoryId=910&secondCategoryId=101792&geoType=2&platform=3&partner=4&originUrl=https%3A%2F%2Fh5.waimai.meituan.com%2Fwaimai%2Fmindex%2Fkingkong%3FnavigateType%3D910%26firstCategoryId%3D910%26secondCategoryId%3D910%26title%3D%25E7%25BE%258E%25E9%25A3%259F&riskLevel=71&optimusCode=10&wm_actual_latitude=22544568&wm_actual_longitude=113949059&openh5_uuid=450940DF938B12BD8AAC598D8CF4678D69BDD48C75BE2CD34A3C20CA525B3490'

headers['Cookie'] = 'cityid=30; network=wifi; uuid=450940DF938B12BD8AAC598D8CF4678D69BDD48C75BE2CD34A3C20CA525B3490; utm_medium=android; utm_content=861735030994726; w_actual_lat=22544568; w_actual_lng=113949059'

