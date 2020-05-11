import json
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

