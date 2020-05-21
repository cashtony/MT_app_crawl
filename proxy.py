import requests


def abuyun():
    # 要访问的目标页面
    targetUrl = "http://test.abuyun.com"
    #targetUrl = "http://proxy.abuyun.com/switch-ip"
    #targetUrl = "http://proxy.abuyun.com/current-ip"

    # 代理服务器
    proxyHost = "http-dyn.abuyun.com"
    proxyPort = "9020"

    # 代理隧道验证信息
    proxyUser = "HVW705154359YE8D"
    proxyPass = "A95D390D789445A7"

    proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
      "host" : proxyHost,
      "port" : proxyPort,
      "user" : proxyUser,
      "pass" : proxyPass,
    }

    proxies = {
        "http"  : proxyMeta,
        "https" : proxyMeta,
    }
    return proxies



def taiyang_proxy():
    resp = requests.get('http://http.tiqu.qingjuhe.cn/getip?num=1&type=1&pack=20681&port=11&lb=4&pb=45&regions=')
    # print(resp.text)
    if '请求' in resp.text:
        resp = requests.get('http://http.tiqu.qingjuhe.cn/getip?num=1&type=1&pack=50186&port=1&lb=1&pb=4&regions=')
    proxy =  {
        'http':'http://'+resp.text,
        'https':'https://'+resp.text
    }
    return proxy


