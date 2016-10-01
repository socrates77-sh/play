#!/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'socrates'

import requests
from bs4 import BeautifulSoup

res = requests.get('http://f1.sina.com.cn/')
res.encoding = 'utf-8'
# print(res.text)

soup = BeautifulSoup(res.content, 'html.parser')
# print(soup.text)

for news in soup.select('.item'):
    # print(news)

    h3 = news.select('h3')
    if len(h3) > 0:
        print(h3[0].text, h3[0].select('a')[0]['href'])

    plink = news.select('p')
    if len(plink) > 0:
        for p in plink:
            print(p.text, p.select('a')[0]['href'])

    # li_link = soup.select('li')
    # print(li_link)
    # # if len(li_link) > 0:
    # #     print(li_link)

