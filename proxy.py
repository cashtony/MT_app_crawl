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
