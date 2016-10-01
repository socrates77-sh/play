#!/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'socrates'

import requests
from bs4 import BeautifulSoup

res = requests.get('http://sports.sina.com.cn/f1/2016-09-29/doc-ifxwkzyh3792669.shtml')
res.encoding = 'utf-8'
# print(res.text)

soup = BeautifulSoup(res.content, 'html.parser')

title = soup.select('#artibodyTitle')
print(title[0].text.strip())

datesel = soup.select('#pub_date')
datestr = datesel[0].text.strip()

from datetime import datetime
dt=datetime.strptime(datestr,'%Y年%m月%d日%H:%M')
print(dt)