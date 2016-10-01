#!/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'socrates'

# import urllib
import urllib.request
import re


page = 1
url = 'http://www.qiushibaike.com/hot/page/' + str(page)
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = {'User-Agent': user_agent}

try:
    request = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(request)
    # print(response.read())

    content = response.read().decode('utf-8')
    # pattern = re.compile('<div.*?author">.*?<a.*?<img.*?>(.*?)</a>.*?<div.*?' +
    # 'content">(.*?)<!--(.*?)-->.*?</div>(.*?)<div class="stats.*?class="number">(.*?)</i>',re.S)
    pattern = re.compile('<div.*?author.*?<h2>(.*?)</h2>.*?<span>(.*?)</span>.*?<i class="number">(.*?)</i>', re.S)
    # pattern = re.compile('<div.*?author.*?<h2>(.*?)</h2>', re.S)
    items = re.findall(pattern, content)
    for item in items:
        print('author:', item[0])
        print(item[1])
        print('点赞:', item[2])
        print('')
        # for item in items:
        # haveImg = re.search("img", item[3])
        # if not haveImg:
        #         print(item[0], item[1], item[2], item[4])
except urllib.request.URLError as e:
    if hasattr(e, "code"):
        print(e.code)
    if hasattr(e, "reason"):
        print(e.reason)
