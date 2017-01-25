__author__ = 'socrates'

import requests
from bs4 import BeautifulSoup
import json

from_data = {
    'j_mode': 'static',
    'j_locale': 'zh_CN',
    'j_username': 'zwr',
    'j_password': 'c3lzdGVtT0EsendyNzcwMjA3',
    'Submit3': '登 录'
}

my_cookies = {
    'JSESSIONID': 'C98E5B8C9E87CA2F049D1B5B3123C310',
    'userClose': '0'
}

s = requests.Session()
# s.headers = {
# 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
# 'Accept-Encoding': 'gzip, deflate',
#     'Accept-Language': 'zh-CN,zh;q=0.8',
#     'Cache-Control': 'max-age=0',
#     'Connection': 'keep-alive',
#     'Content-Length': '112',
#     'Content-Type': 'application/x-www-form-urlencoded',
#     'Cookie': 'JSESSIONID=D391B05A08DCD41DA70E4945DD2215D4; userClose=0',
#     'Host': '192.168.1.228:7890',
#     'Origin': 'http://192.168.1.228:7890',
#     'Referer': 'http://192.168.1.228:7890/oa/themes/mskin/login/login.jsp',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36'
# }

# s.headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36'
# }

s.verify = False

url = 'http://192.168.1.228:7890/oa/j_acegi_security_check'

# res = s.post(url, data=from_data)
res = s.post(url, data=from_data, cookies=my_cookies)
# res.encoding = 'utf-8'
# print(res.text)

# res1=s.post('http://192.168.1.228:7890/oa/modules/worklog/worklog.do?method=list&t=3', cookies=my_cookies)
res2=s.post('http://192.168.1.228:7890/oa/modules/worklog/worklog.do?method=list&t=4', cookies=my_cookies)
res3=s.post('http://192.168.1.228:7890/oa/modules/worklog/worklog.do?method=edit&id=27624&t=4', cookies=my_cookies)


print(res3.text)

