#!/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'socrates'

import requests

url = 'http://imgsrc.baidu.com/forum/pic/item/130268385343fbf21f49f26db97eca8064388ff2.jpg'
# url='http://imgsrc.baidu.com/forum/pic/item/278d2f2c11dfa9ecf97e02596bd0f703908fc18f.jpg'

ir = requests.get(url)
# ir = requests.get(url, cookies=cookies1)
sz = open('324377.jpg', 'wb').write(ir.content)
print('324377.jpg', sz, 'bytes')

