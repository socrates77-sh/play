#!/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'socrates'

import re
import requests
from bs4 import BeautifulSoup


class TopPage():
    url_ygdy = 'http://www.ygdy8.net/'
    new_url = []

    def __init__(self, days=1):
        self.days = days

    def get_new_url(self):
        r = requests.get(self.url_ygdy)
        r.encoding = 'gbk'
        # print(r.text)
        soup = BeautifulSoup(r.content, 'html.parser')
        tr_link = soup.find_all('tr')
        for tl in tr_link:
            if tl.find('font'):
                alink = tl.find(href=re.compile('\d+\.html'))
                href = alink.get('href')
                date = tl.find('font')
                print(href)
                print(alink.string)
                print(date.string)


def main():
    tp = TopPage()
    tp.get_new_url()


if __name__ == '__main__':
    main()


