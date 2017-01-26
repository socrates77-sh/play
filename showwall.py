#!/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'socrates'

import re
import requests
import os
import time
# from bs4 import BeautifulSoup

VERSION = '1.0'
save_path = 'e:\download'
url_main = 'http://www.showwall.com'
my_cookies = dict(
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

INTERVAL = 5
intest_stars = ['ayum_hamasaki', 'amuro_namie', 'saki_aibu', 'gouriki_ayame', 'asahina_aya',
                'jun_ji_hyun']
last_id = 320000


class ShowwallStar():
    def __init__(self, name, last_id=0):
        self.name = name
        self.last_id = last_id

    def page_text(self, page=1):
        if page <= 1:
            url = url_main + '/wallpaper/' + self.name + '/'
        else:
            url = url_main + '/wallpaper/' + self.name + '/page/' + str(page) + '/'
        r = requests.get(url)
        r.encoding = 'utf-8'
        print('[Access] %s page %d ... (status:%d)' % (self.name, page, r.status_code))
        return r.text

    @staticmethod
    def full_name(html_text):
        p = re.compile('<title>(.*?)【共收藏', re.S)
        result = re.search(p, html_text).group(1).strip()
        return result

    @staticmethod
    def pic_count(html_text):
        p = re.compile('【共收藏(.*?)張桌布圖】', re.S)
        result = re.search(p, html_text).group(1).strip()
        return eval(result)

    @staticmethod
    def id_one_page(html_text):
        p = re.compile('/shorten/(.*?)\.jpg', re.S)
        result = re.findall(p, html_text)
        return result

    def id_all(self):
        l_id_all = []
        t = self.page_text(1)
        l_id_page = self.id_one_page(t)
        l_id_all += [x for x in self.id_one_page(t) if eval(x) > self.last_id]
        if eval(l_id_page[-1]) <= self.last_id:
            return l_id_all

        count = self.pic_count(t)
        for i in range(2, int(count / 20) + 2):
            # print('page=%d' % i)
            t = self.page_text(i)
            l_id_page = self.id_one_page(t)
            l_id_all += [x for x in self.id_one_page(t) if eval(x) > self.last_id]
            if eval(l_id_page[-1]) <= self.last_id or i == int(count / 20) + 1:
                return l_id_all

    def save_pic(self, id_all, glance=False):
        i = 1
        for x in id_all:
            save_file = self.name + '_' + str(x) + '.jpg'
            full_file = os.path.join(save_path, save_file)
            url = 'http://img.showwall.com/download.php?id=' + str(x) + '&k=' + self.name + '&u=9999999999'
            if glance:
                print('[Save] (%d) %s' % (i, save_file))
            else:
                ir = requests.get(url, cookies=my_cookies)
                sz = open(full_file, 'wb').write(ir.content)
                time.sleep(INTERVAL)
                print('[Save] (%d) %s <%d bytes>' % (i, save_file, sz))
            i += 1


def main():
    count_pic = 0
    for star in intest_stars:
        sw = ShowwallStar(star, last_id)
        r1 = sw.id_all()
        sw.save_pic(r1, glance=True)
        count_pic += len(r1)

    print('Download %d pictures' % count_pic)


if __name__ == '__main__':
    main()
