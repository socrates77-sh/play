__author__ = 'socrates'

import requests
from bs4 import BeautifulSoup

res = requests.get('http://news.sina.com.cn/china/')
# print(type(res))
res.encoding = 'utf-8'
print(res.text)



# html_sample = ' \
# <html> \
#     <body> \
#     <h1 id="title">Hello World</h1> \
#     <a href="#" class="link">This is link1</a> \
#     <a href="# link2" class="link"> This is link2</a> \
#     <body> \
# </html>'
#
# soup = BeautifulSoup(html_sample, 'html.parser')
# print(type(soup))
# print(soup.text)
#
# header = soup.select('h1')
# print(type(header))
# print(header[0])
#
# alink = soup.select('.link')
# for l in alink:
#     print(type(l))
#     print(l['href'])
