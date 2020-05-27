import json
from pprint import pprint
from proxy import taiyang_proxy
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
def pro(response):
    return json.loads(response.content.decode())

payload = 'geoType=2&mtWmPoiId=1112840116809435&source=shoplist&uuid=450940DF938B12BD8AAC598D8CF4678D69BDD48C75BE2CD34A3C20CA525B3490&platform=3&partner=4&originUrl=https%3A%2F%2Fh5.waimai.meituan.com%2Fwaimai%2Fmindex%2Fmenu%3FdpShopId%3D%26mtShopId%3D1112840116809435%26utm_source%3Dwandoujia%26channel%3Dmtjj%26source%3Dshoplist%26initialLat%3D22.544568%26initialLng%3D113.949059%26actualLat%3D22.544568%26actualLng%3D113.949059&riskLevel=71&optimusCode=10&wm_latitude=22544568&wm_longitude=113949059&openh5_uuid=450940DF938B12BD8AAC598D8CF4678D69BDD48C75BE2CD34A3C20CA525B3490'

headers = {
    'Host': 'i.waimai.meituan.com',
    'Accept': 'application/json',
    'Origin': 'https://h5.waimai.meituan.com',
    # 'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; Redmi Note 3 Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.91 Mobile Safari/537.36 TitansX/11.19.6 KNB/1.2.0 android/6.0.1 mt/com.sankuai.meituan/10.0.202 App/10120/10.0.202 MeituanGroup/10.0.202',
    'User-Agent':'AiMeiTuan /Meizu-5.1-MX4-1920x1152-480-10.8.404-1000080404-862095026057122-meizu4',
    'Referer': 'https://h5.waimai.meituan.com/waimai/mindex/menu?dpShopId=&mtShopId=1112840116809435&utm_source=wandoujia&channel=mtjj&source=shoplist&initialLat=22.544568&initialLng=113.949059&actualLat=22.544568&actualLng=113.949059',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,en-US;q=0.9',
    'Cookie': 'cityid=30; network=wifi; utm_source=meizu4; utm_medium=android; utm_term=1000000202; utm_content=862095026057122; utm_campaign=AgroupBgroupC0E0Ghomepage_category1_394__a1__c-1024; wm_order_channel=mtjj; au_trace_key_net=default; openh5_uuid=E1BD0ABE0A4A8F012F3E7C3D393E13D4598E05C2BFE038A1F57A72FD44F391FC; channelType=%7b%22mtjj%22%3a%220%22%7d;',
    'X-Requested-With': 'com.sankuai.meituan',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Connection': 'keep-alive',
}

url = 'https://i.waimai.meituan.com/openh5/poi/food?_=1589277696918'
# response = requests.post(url,headers=headers,data=payload)
# json_response = json.loads(response.text)
# pprint(json_response)

### 商家信息页 手机端 用
url = 'https://i.waimai.meituan.com/openh5/poi/info?_=1589277696918'
payload = 'mtWmPoiId=939443697603857&openh5_uuid=E1BD0ABE0A4A8F012F3E7C3D393E13D4598E05C2BFE038A1F57A72FD44F391FC'
# headers['Cookie'] = 'cityid=30; network=wifi; uuid=E1BD0ABE0A4A8F012F3E7C3D393E13D4598E05C2BFE038A1F57A72FD44F391FC; utm_source=wandoujia; utm_medium=android; utm_term=1000000202; utm_content=861735030994726; wm_order_channel=mtjj; au_trace_key_net=default; openh5_uuid=450940DF938B12BD8AAC598D8CF4678D69BDD48C75BE2CD34A3C20CA525B3490; terminal=i; w_utmz="utm_campaign=(direct)&utm_source=5000&utm_medium=(none)&utm_content=(none)&utm_term=(none)"; openh5_uuid=450940DF938B12BD8AAC598D8CF4678D69BDD48C75BE2CD34A3C20CA525B3490; service-off=0; utm_campaign=AgroupBgroupC0E0Ghomepage_category1_394__a1__c-1024; channelType={%22mtjj%22:%220%22}; w_actual_lat=22546510; w_actual_lng=113948770'
# resp = requests.post(url,headers=headers,data=payload,verify=False)
# json_resp = pro(resp)
# pprint(json_resp)

### 最简化参数  商品 用
url = 'https://i.waimai.meituan.com/openh5/poi/food?_=1589277696918'

payload = 'mtWmPoiId=856245886615563&openh5_uuid=E1BD0ABE0A4A8F012F3E7C3D393E13D4598E05C2BFE038A1F57A72FD44F391FC&dpShopId=-1&source=shoplist'

# resp = requests.post(url,headers=headers,data=payload,verify=False)
# json_resp = pro(resp)
# print(json_resp)

# 商家评论页 手机端 用  可能会过期
url = 'https://i.waimai.meituan.com/openh5/poi/comments?_=1589425001731'
headers['Cookie'] = 'cityid=30; network=wifi; utm_medium=android; utm_term=1000000202; utm_content=862095026057122; _lxsdk_cuid=1725440c0da2-08336aca1-5a10162d-3c000-1725440c0dc62; _lxsdk=E1BD0ABE0A4A8F012F3E7C3D393E13D4598E05C2BFE038A1F57A72FD44F391FC; _lxsdk_s=1725440c0e0-f28-0db-5e0%7C-1%7CNaN;'

payload = 'shopId=0&mtWmPoiId=943382183119710&startIndex=0&platform=3&partner=4&originUrl=https%3A%2F%2Fh5.waimai.meituan.com%2Fwaimai%2Fmindex%2Fmenu%3FdpShopId%3D%26mtShopId%3D891876934366856%26utm_source%3Dwandoujia%26channel%3Dmtjj%26source%3Dshoplist%26initialLat%3D%26initialLng%3D%26actualLat%3D22.544568%26actualLng%3D113.949059&riskLevel=71&optimusCode=10&openh5_uuid=E1BD0ABE0A4A8F012F3E7C3D393E13D4598E05C2BFE038A1F57A72FD44F391FC'
# resp = requests.post(url,headers=headers,data=payload,verify=False)
# resp_json = pro(resp)
# pprint(resp_json)

### 列表页 根据商品分类 手机请求 用
url = 'https://i.waimai.meituan.com/openh5/channel/kingkongshoplist?_=1589461806277'

payload = 'startIndex=0&navigateType=910&firstCategoryId=910&secondCategoryId=100321&geoType=2&platform=3&partner=4&originUrl=https://h5.waimai.meituan.com/waimai/mindex/kingkong?navigateType=910&firstCategoryId=910&secondCategoryId=910&title=%E7%BE%8E%E9%A3%9F&riskLevel=71&optimusCode=10&wm_actual_latitude=22544568&wm_actual_longitude=113949059&openh5_uuid=E1BD0ABE0A4A8F012F3E7C3D393E13D4598E05C2BFE038A1F57A72FD44F391FC'

# headers['Cookie'] = 'cityid=30; network=wifi; uuid=E1BD0ABE0A4A8F012F3E7C3D393E13D4598E05C2BFE038A1F57A72FD44F391FC; utm_source=wandoujia; utm_medium=android; utm_term=1000000202; utm_content=862095026057122; wm_order_channel=mtjj; au_trace_key_net=default; openh5_uuid=E1BD0ABE0A4A8F012F3E7C3D393E13D4598E05C2BFE038A1F57A72FD44F391FC; terminal=i; w_utmz="utm_campaign=(direct)&utm_source=5000&utm_medium=(none)&utm_content=(none)&utm_term=(none)"; openh5_uuid=E1BD0ABE0A4A8F012F3E7C3D393E13D4598E05C2BFE038A1F57A72FD44F391FC; service-off=0; utm_campaign=AgroupBgroupC0E0Ghomepage_category1_394__a1__c-1024; channelType={%22mtjj%22:%220%22}; w_actual_lat=22546510; w_actual_lng=113948770'
resp = requests.post(url,headers=headers,data=payload,proxies=taiyang_proxy())
json_resp = pro(resp)
print(resp.text)



### 列表页 根据位置距离 手机请求
url = 'https://i.waimai.meituan.com/openh5/homepage/poilist?_=1589358865578'
headers['Cookie'] = 'cityid=30; network=wifi; utm_medium=android; utm_term=1000000202; utm_content=861735030994726; au_trace_key_net=default; terminal=i; utm_campaign=AgroupBgroupC0E0Ghomepage_category1_394__a1__c-1024; w_actual_lat=22544568; w_actual_lng=113949059'
payload = 'startIndex=1&sortId=5&geoType=2&platform=3&partner=4&originUrl=https%3A%2F%2Fh5.waimai.meituan.com%2Fwaimai%2Fmindex%2Fhome%3Ftype%3Dmain_page%26channel%3Dmtjj%26utm_source%3D60374%26f%3Dandroid%26lat%3D22.547581662624406%26lng%3D113.94418152492057%26utm_medium%3Dandroid%26utm_term%3D1000000202%26version_name%3D10.0.202%26utm_content%3D861735030994726%26utm_campaign%3DAgroupBgroupC0E0Ghomepage_category1_394__a1__c-1024%26ci%3D30%26msid%3D8617350309947261589353838250%26uuid%3D450940DF938B12BD8AAC598D8CF4678D69BDD48C75BE2CD34A3C20CA525B3490%26userid%3D-1&riskLevel=71&optimusCode=10&wm_latitude=22544568&wm_longitude=113949059&openh5_uuid=450940DF938B12BD8AAC598D8CF4678D69BDD48C75BE2CD34A3C20CA525B3490'
# resp = requests.post(url,headers=headers,data=payload)
# print(resp.text)


# 详情页 商品 浏览器端 不过期
url = 'https://i.waimai.meituan.com/openh5/poi/food?_=1589340714380'

headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
headers['Cookie'] = '_lxsdk_cuid=1719b4ea86ac8-0bfd3bb31469b4-5313f6f-1fa400-1719b4ea86ac8; t_lxid=1719b4ea9f2c8-0217437ea7aac-5313f6f-1fa400-1719b4ea9f2c8-tid; ci=1; rvct=1; _hc.v=34edf988-42dc-17df-4202-f3ef87a698df.1587448615; uuid=07a6037edb4f4c68adf4.1588820856.1.0.0; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _ga=GA1.3.806081906.1588820859; __mta=209662893.1588820860537.1588820914260.1588822844430.4; wm_order_channel=default; utm_source=; au_trace_key_net=default; openh5_uuid=07a6037edb4f4c68adf4.1588820856.1.0.0; terminal=i; w_utmz="utm_campaign=(direct)&utm_source=5000&utm_medium=(none)&utm_content=(none)&utm_term=(none)"; openh5_uuid=07a6037edb4f4c68adf4.1588820856.1.0.0; w_uuid=TN0VoeXwz57HsjbO105kDc4_XM3vhdSqSclZ6pSWkZcSW2XOldD_ujivlMaEbNiS; w_visitid=7d78a759-22b1-4c7d-bbcb-b076c6ef4cb9; channelType={%22default%22:%220%22}; channelConfig={%22channel%22:%22default%22%2C%22type%22:0%2C%22fixedReservation%22:{%22reservationTimeStatus%22:0%2C%22startReservationTime%22:0%2C%22endReservationTime%22:0}}; service-off=0; w_actual_lat=22555064; w_actual_lng=113941550; cssVersion=c4a699b0; _lxsdk_s=1720c13fad0-7ef-1e7-2a9%7C%7C33'

payload = 'geoType=2&mtWmPoiId=1083746008377954&source=searchresult&platform=3&partner=4&originUrl=https%3A%2F%2Fh5.waimai.meituan.com%2Fwaimai%2Fmindex%2Fmenu%3FmtShopId%3D1083746008377954%26initialLat%3D22.555064%26initialLng%3D113.94155%26actualLat%3D22.555064%26actualLng%3D113.94155%26source%3Dsearchresult&riskLevel=71&optimusCode=10&wm_latitude=22555064&wm_longitude=113941550&openh5_uuid=07a6037edb4f4c68adf4.1588820856.1.0.0'

# resp = requests.post(url,headers=headers,data=payload)
# print(resp.text)

# 商店列表页 手机端 根据poi_id  get请求
url = 'https://i.waimai.meituan.com/external/poi/1030333795405299?utm_source=5913&amp;wmi_from=cpoiinfo&amp;user_id=2599273935'

"""

"""