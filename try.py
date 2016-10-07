__author__ = 'socrates'

import requests

# r = requests.get('https://github.com', verify=True)
# r = requests.get('https://github.com',verify=False)
r = requests.get('https://kyfw.12306.cn/otn/', verify=False)
print(r.text)