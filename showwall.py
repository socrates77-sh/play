#!/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'socrates'

import re
import requests
from bs4 import BeautifulSoup


class Showwall():
    def __init__(self):
        # self.url_main = 'http://www.showwall.com'
        self.url_main = 'http://img.showwall.com/download.php?id=324377&k=asae_shiraishi&u=9999999999'

        self.cookies = {
            'JSESSIONID': 'C98E5B8C9E87CA2F049D1B5B3123C310',
            'userClose': '0'
        }
        self.s = requests.session()
        self.s.verify = False
        # self.s.encoding = 'chunked'
        self.s.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36'
        }

    def login(self):
        # page_login = '/j_acegi_security_check'
        # data = {
        # 'j_mode': 'static',
        # 'j_locale': 'zh_CN',
        # 'j_username': 'zwr',
        # 'j_password': 'c3lzdGVtT0EsendyNzcwMjA3',
        #     'Submit3': '登 录'
        # }
        return self.s.post(self.url_main)


# http://img.showwall.com/download.php?id=324377&k=asae_shiraishi&u=9999999999

def main():
    # sw = Showwall()
    # r = sw.login()
    # soup = BeautifulSoup(r.content, 'html.parser', from_encoding='utf-8')
    #
    # print(soup.text)
    # all_id = wl.get_log_id(1)
    #
    # for (idx, datex, personx) in wl.filter_log(all_id, -1, 1):
    # r = wl.get_one_log(idx)
    # print(idx, datex, personx, r)

    cookies1 = dict(
        __cfduid='d3d96b32a79d4f9f2828f2c556b6518521485350718',
        uid='141043-2919320843-0-2',
        sid='d5fbf9c678e53e58e66d',
        uname='%E5%AD%90%E7%BD%95%E8%A8%80%E5%88%A9%E4%B8%8E%E5%91%BD%E4%B8%8E%E4%BB%81',
        __utmt='1',
        __utma='19282554.1522409781.1485350848.1485350848.1485350848.1',
        __utmb='19282554.9.10.1485350848',
        __utmc='19282554',
        __utmz='19282554.1485350848.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)'
    )
    url = 'http://img.showwall.com/download.php?id=324377&k=asae_shiraishi&u=9999999999'
    # ir = requests.get(url, cookies=cookies1)
    ir = requests.get(url, cookies=cookies1)
    sz = open('324377.jpg', 'wb').write(ir.content)
    print('324377.jpg', sz, 'bytes')


if __name__ == '__main__':
    main()
