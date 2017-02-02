#!/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'socrates'

import re
import requests
import os
import time
import sys

VERSION = '1.0'  # 版本号
star = '孙允珠'
save_path = 'e:\download'  # 默认存放路径
INTERVAL = 1  # 下载一张图片间隔时间


class TiebaPicPage():
    def __init__(self, name, tid):
        self.name = name
        self.tid = tid


    def page_url(self):
        s = ''
        for b in self.name.encode('utf-8'):
            s += '%%%2X' % b
        r = 'http://tieba.baidu.com/photo/p?kw=%s&fp=1&tid=%s' % (s, self.tid)
        return r

    def page_html(self):
        url = self.page_url()
        r = requests.get(url)
        return r.text

    def post_id(self):
        html_text = self.page_html()
        p = re.compile('"post_id":(\d+)', re.S)
        result = re.search(p, html_text).group(1).strip()
        return result

    def find_all_pic(self):
        post_id = self.post_id()
        url = 'http://tieba.baidu.com/p/%s?pid=%s#%s' % (self.tid, post_id, post_id)
        r = requests.get(url)
        html_text = r.text
        # print(html_text)
        p = re.compile('http://imgsrc\.baidu\.com/forum/w.*?.jpg', re.S)
        # p = re.compile('src="http://imgsrc\.baidu\.com.*?.jpg"', re.S)
        l_pic = re.findall(p, html_text)
        return l_pic

    def save_all_pic(self):
        l_pic = self.find_all_pic()
        for l in l_pic:
            self.save_a_pic(l)
        print('Download %d pictures' % len(l_pic))

    @staticmethod
    def save_a_pic(pic_url):
        save_file = pic_url.split('/')[-1]
        full_file = os.path.join(save_path, save_file)
        pid = save_file.split('.')[0]
        down_url = 'http://imgsrc.baidu.com/forum/pic/item/%s.jpg' % pid
        try:
            res = requests.get(down_url, timeout=60)
            if res.status_code != 200:
                return False
        except Exception as e:
            print(e)
            return False
        sz = open(full_file, 'wb').write(res.content)
        print('[Save] %s <%d bytes>' % (save_file, sz))
        time.sleep(INTERVAL)
        return True


class TiebaAll():
    def __init__(self, name):
        self.name = name

    def page_url(self):
        s = ''
        for b in self.name.encode('utf-8'):
            s += '%%%2X' % b
        r = 'http://tieba.baidu.com/f?kw=%s&tab=album&subTab=album_thread' % s
        return r

    def page_html(self):
        url = self.page_url()
        r = requests.get(url)
        return r.text

    def page_list(self):
        html_text = self.page_html()
        p = re.compile('id="pic_item_(\d+)"', re.S)
        l_tid = []
        m = re.finditer(p, html_text)
        for x in m:
            l_tid.append(x.group(1).strip())
        return l_tid

    def save_all_tid(self, tid):
        tb = TiebaPicPage(self.name, tid)
        tb.save_all_pic()


def download(num):
    tb = TiebaAll(star)
    l_tid = tb.page_list()
    for i in range(0, num):
        tb.save_all_tid(l_tid[i])


def version():
    print('tieba.py %s' % VERSION)


def usage():
    print('usage:')
    print('tieba.py num_of_page')


def usage_err():
    print('ERROR: invalid option or argument')
    usage()
    sys.exit(1)


def main():
    argn = len(sys.argv)
    if argn == 2:
        download(eval(sys.argv[1]))
    else:
        usage_err()


if __name__ == '__main__':
    main()

