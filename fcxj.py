'''
在线阅读网站抓取txt——丰臣秀吉（山冈庄八）
'''

__author__ = 'zwr'

import re
import requests
import os
import time
import sys

save_path = 'e:\download\丰臣秀吉'  # 默认存放路径
url_main = 'http://www.yooread.com/5/2518/'
header = {
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36'}


class MainPage():
    @staticmethod
    def page_html():
        r = requests.get(url_main)
        return r.text

    def chapter_id(self):
        html_text = self.page_html()
        p = re.compile('a href="/5/2518/(\d+)\.html" title="(.*?)"', re.S)
        result = re.findall(p, html_text)
        return result

    @staticmethod
    def chapter_html(cid):
        url = url_main + cid + '.html'
        r = requests.get(url=url, headers=header)
        r.encoding = 'utf-8'
        # r.encoding = 'gb18030'
        # print(r.text)
        return r.text

    def chapter_text(self, cid, txt, num):
        html_text = self.chapter_html(cid)
        p = re.compile('<p>(.*?)</p>', re.S)
        all_lines = re.findall(p, html_text)
        full_file = os.path.join(save_path, num + '.txt')
        # print(all_lines)
        with open(full_file, 'w+') as f:
            f.write('第%s章 %s\n' % (num, txt))
            # f.writelines(all_lines)
            for l in all_lines:
                try:
                    f.write('%s\n' % l)
                except Exception as e:
                    print(e)
        print('[Save] %s' % full_file)


def main():
    mp = MainPage()
    l_chapter = mp.chapter_id()
    l_chapter_sorted = sorted(l_chapter, key=lambda t: t[0])

    # print(len(l_chapter_sorted))

    # i = 1
    # cid, txt = l_chapter_sorted[i]
    # num = '%03d' % (i + 1)
    # mp.chapter_text(cid, txt, num)

    for i in range(0, len(l_chapter)):
        cid, txt = l_chapter_sorted[i]
        num = '%03d' % (i + 1)
        mp.chapter_text(cid, txt, num)


if __name__ == '__main__':
    main()