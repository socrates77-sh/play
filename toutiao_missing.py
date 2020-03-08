# history:
# 2020/03/07  v1.0  initial


import time
import sys
import os
import re
import msvcrt
import datetime
import requests
import json

# import abc
from enum import Enum, auto

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait


VERSION = '1.0'

URL_PREFIX = 'https://www.toutiao.com'
DST_PATH = r'f:\download'


WAIT_RESPONSE = 5

ERR_WEB_ACCESS_FAIL = 'Cannot access web'
ERR_WEB_EXTRACT_FAIL = 'Cannot extract web'

pic_count = 0


def extract_pic(html_text):
    pic_url_list = []
    p = re.compile('gallery: JSON.parse\("({\\\\".+?})"\),', re.S)
    ret = re.search(p, html_text)
    if ret:
        j_ret = json.loads(ret.group(1).replace('\\\"', '"'))
        sub_images = j_ret['sub_images']
        for img in sub_images:
            url_dirty = img['url']
            url = url_dirty.replace('\\', '')
            pic_url_list.append(url)
    if pic_url_list != []:
        return pic_url_list

    p = re.compile('images: (\[.+?])', re.S)
    ret = re.search(p, html_text)
    if ret:
        images = eval(ret.group(1))
        for img in images:
            url = 'https:' + img.replace('\\u002F', '/')
            pic_url_list.append(url)
    if pic_url_list != []:
        return pic_url_list

    p = re.compile('&quot;(http:.+?)\\\\&quot;', re.S)
    ret = re.findall(p, html_text)
    if ret != []:
        for img in ret:
            url = img.replace('\\u002F', '/')
            pic_url_list.append(url)
    if pic_url_list != []:
        return pic_url_list

    return pic_url_list


def get_page_source1(page_url):
    r = ''
    try:
        # r = requests.get(page_url, headers=my_headers, cookies=my_cookies)
        r = requests.get(page_url)
    except Exception:
        print('Error: %s %s' % (ERR_WEB_ACCESS_FAIL, page_url))
    return r.text


def get_page_source(page_url):
    chrome_options = Options()
    # chrome_options.add_argument('--headless')
    web_driver = webdriver.Chrome(options=chrome_options)
    web_driver.minimize_window()
    web_driver.get(page_url)
    time.sleep(WAIT_RESPONSE)
    html_txt = web_driver.page_source
    # print(html_txt)
    return html_txt


def get_pic_urls_from_a_page(page_url):
    html = get_page_source(page_url)
    if html:
        result = extract_pic(html)
        if result == []:
            print('Error: %s %s' % (ERR_WEB_EXTRACT_FAIL, page_url))
        return result
    else:
        print('Error: %s %s' % (ERR_WEB_ACCESS_FAIL, page_url))
        return []


def save_a_pic(pic_url, path, filename):
    global pic_count
    full_file = os.path.join(path, filename)
    try:
        res = requests.get(pic_url, timeout=60)
        if res.status_code != 200:
            return False
    except Exception as e:
        print(e)
        return False
    sz = open(full_file, 'wb').write(res.content)
    print('[Save] %s <%d bytes>' % (filename, sz))
    pic_count += 1


def download_a_page(username, page_url, save_path):
    pic_urls = get_pic_urls_from_a_page(page_url)
    # print(pic_urls)
    if pic_urls == []:
        return False
    for url in pic_urls:
        # print(url)
        pic_url = url.replace('\\', '')
        pic_url = pic_url.replace('?from=post', '')
        # pic_url = pic_url.replace('?', '')n
        filename = username + '_' + pic_url.split('/')[-1] + '.jpg'
        save_a_pic(pic_url, save_path, filename)
    return True


def read_missing():
    l_lines = ''
    missing_file = DST_PATH + r'\log\missing_tt.txt'
    try:
        with open(missing_file, 'r') as f:
            l_lines = f.readlines()
            # print(l_lines)
    except Exception as e:
        print(e)
    return l_lines


def wait_any_key():
    print('press any key to exit...')
    msvcrt.getch()


def print_version(version):
    print('=' * 70)
    print('%s version: %s' % (os.path.basename(__file__), VERSION))
    print('=' * 70)


def main():
    print_version(VERSION)
    global pic_count

    save_path_date = r'%s\%s_tt_missing' % (
        DST_PATH, datetime.datetime.now().date().strftime('%y%m%d'))

    if(not os.path.exists(save_path_date)):
        os.makedirs(save_path_date, exist_ok=True)

    all_pages = read_missing()

    for i in range(len(all_pages)):
        page = all_pages[i]
        print()
        print(page)
        download_a_page('missing', page, save_path_date)
        print('page[%d/%d] <%d pictures> ' % (i+1, len(all_pages), pic_count))

    print('=' * 70)
    print('%d pictures download' % pic_count)

    wait_any_key()


if __name__ == '__main__':
    main()
