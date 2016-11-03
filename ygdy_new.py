#!/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'socrates'

import datetime
import re
import requests
from bs4 import BeautifulSoup
import win32con
import win32clipboard as w


class TopPage():
    url_ygdy = 'http://www.ygdy8.net/'
    new_url = []

    def __init__(self, days=7):
        self.days = days

    def get_new_url(self):
        r = requests.get(self.url_ygdy)
        # soup = BeautifulSoup(r.content, 'html.parser', from_encoding='gbk')
        soup = BeautifulSoup(r.content, 'html.parser', from_encoding='gb18030')
        all_area2 = soup.find_all(class_='co_area2')
        movie1 = all_area2[2]
        movie2 = all_area2[3]
        for tl in movie1.find_all('tr'):
            if tl.find('font'):
                alink = tl.find(href=re.compile('\d+\.html'))
                href = alink.get('href')
                date = tl.find('font')
                t1 = datetime.datetime.strptime(date.string, '%Y-%m-%d')
                td = datetime.datetime.now() - t1
                if td.days <= self.days:
                    self.new_url.append(href)
        for tl in movie2.find_all('tr'):
            if tl.find('font'):
                alink = tl.find(href=re.compile('\d+\.html'))
                href = alink.get('href')
                date = tl.find('font')
                t1 = datetime.datetime.strptime(date.string, '%Y-%m-%d')
                td = datetime.datetime.now() - t1
                if td.days <= self.days:
                    self.new_url.append(href)

    def scrap_a_movie(self, movie_url):
        dict_result = {}
        whole_movie_url = self.url_ygdy + movie_url[1:]
        r = requests.get(whole_movie_url)
        soup = BeautifulSoup(r.content, 'html.parser', from_encoding='gb18030')
        content = soup.find(class_='co_content8').ul

        try:
            # Title
            dict_result['Title'] = soup.h1.font.string

            # 发布时间
            pattern = re.compile('发布时间.*?(\d+-\d+-\d+)\s', re.S)
            result = re.search(pattern, str(content))
            dict_result['发布时间'] = result.group(1).strip()

            # 片名
            pattern = re.compile('片\s*?名(.*?)<', re.S)
            result = re.search(pattern, str(content))
            dict_result['片名'] = result.group(1).strip()

            # 译名
            pattern = re.compile('译\s*?名(.*?)<', re.S)
            result = re.search(pattern, str(content))
            dict_result['译名'] = result.group(1).strip()

            # 年代
            pattern = re.compile('年\s*?代(.*?)<', re.S)
            result = re.search(pattern, str(content))
            dict_result['年代'] = result.group(1).strip()

            # 国家
            pattern = re.compile('国\s*?家(.*?)<', re.S)
            result = re.search(pattern, str(content))
            dict_result['国家'] = result.group(1).strip()

            # 导演
            pattern = re.compile('导\s*?演(.*?)<', re.S)
            result = re.search(pattern, str(content))
            dict_result['导演'] = result.group(1).strip()

            # 主演

            pattern = re.compile('主\s*?演(.*?)<br\s*?/><br\s*?/>', re.S)
            result = re.search(pattern, str(content))
            # print(result.group(1))
            actors = result.group(1).split(sep='<br/>')
            dict_result['主演'] = actors

            # 简介
            pattern = re.compile('简\s*?介\s*?<br/><br/>(.*?)<', re.S)
            result = re.search(pattern, str(content))
            dict_result['简介'] = result.group(1).strip()

            # 下载地址
            body = content.find('tbody')
            alink = body.find('a')
            dict_result['下载地址'] = alink.get('href')
        except AttributeError:
                return

        return dict_result

    def print_a_movie(self, dict_result):
        if dict_result is None:
            print('Parse unsuccessful! Skip...')
            return
        try:
            print('===============================================================')
            print('Title:\t\t%s' % dict_result['Title'])
            print('===============================================================')
            print('发布时间:\t%s' % dict_result['发布时间'])
            print('片名:\t\t%s' % dict_result['片名'])
            print('译名:\t\t%s' % dict_result['译名'])
            print('年代:\t\t%s' % dict_result['年代'])
            print('国家:\t\t%s' % dict_result['国家'])
            print('导演:\t\t%s' % dict_result['导演'])
            # 主演最多显示5个
            print('主演:')
            if len(dict_result['主演']) > 5:
                show_list = dict_result['主演'][:5]
            else:
                show_list = dict_result['主演']
            for l in show_list:
                print('\t\t%s' % l.strip())
            print('简介:\n\t%s' % dict_result['简介'])
            print('下载地址:\n\t%s' % dict_result['下载地址'])
            print('\n')
        except UnicodeEncodeError:
            pass


def main():
    tp = TopPage()
    tp.get_new_url()

    download = ''
    for url in tp.new_url:
        dict_result = tp.scrap_a_movie(url)
        tp.print_a_movie(dict_result)
        key = input('Choice Quit/Download/Continue ... [q/d/enter]')
        if key == 'q' or key == 'Q':
            break
        elif key == 'd' or key == 'D':
            download += dict_result['下载地址'] + '\n'

    if len(download) != 0:
        w.OpenClipboard()
        w.EmptyClipboard()
        w.SetClipboardData(win32con.CF_UNICODETEXT, download)
        w.CloseClipboard()


if __name__ == '__main__':
    main()