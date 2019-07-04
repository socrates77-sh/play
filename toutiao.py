# history:
# 2019/05/19  v1.0  initial
# 2019/06/01  v1.1  optimize display
# 2019/06/22  v1.2  modify log

import time
import sys
import os
import re
import msvcrt
import datetime
import requests

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

VERSION = '1.2'

DST_PATH = r'f:\download'

# https://www.toutiao.com/c/user/107952533857/#mid=1628218742667278
# ('username', 'uid', mid)

all_users = [
    ('安全的情网', '107952533857', '1628218742667278'),
    ('倾城视图', '58868350934', '1577199391283214'),
    ('图影度光阴', '65767525786', '1631120772459524'),
    ('孙允珠精品美图', '2818790666547229', '1632605670327303'),
    ('一路高飞', '4187341958', '1575656257167374'),
    ('在下子程', '61713811819', '1617661839064067'),
    ('小小的世界我只保护你', '3635977242', '1570148542825474'),
    ('丹丹视觉美', '89923571455', '1591554527990797'),
    ('美图珠', '61704193641', '1589024159354893')
]

all_users1 = [all_users[-1]]

ERR_WEB_ACCESS_FAIL = 'Cannot access web'
ERR_WEB_EXTRACT_FAIL = 'Cannot extract web'

WAIT_RESPONSE = 5
END_CMD_LIMIT = 100
# END_CMD_LIMIT = 1000
# END_CMD_LIMIT = 1

pic_count = 0
f_log = 0


def my_str2dt(dt_str):
    return datetime.datetime.strptime(dt_str, "%Y-%m-%d %H:%M")


def wait_refresh():
    time.sleep(WAIT_RESPONSE)


class TTUserValidPages():
    def __init__(self, username, user_url, last_date):
        self.__page_list = []
        self.__last_date = last_date
        self.__init_web(user_url)
        self.__username = username
        self.__extract_pages()

    # def __del__(self):
    #     self.__web_driver.close()

    @property
    def page_list(self):
        return self.__page_list

    def __init_web(self, user_url):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        self.__web_driver = webdriver.Chrome(options=chrome_options)
        # self.__web_driver = webdriver.Chrome()
        self.__web_driver.get(user_url)
        wait_refresh()

    def __find_pages(self):
        html_txt = self.__web_driver.page_source
        p = re.compile(
            r'<a class=\"link title\" target=\"_blank\" href=\"/item/(.*?)/\">(.*?)</a>.*?<span class=\"lbtn\">.*?(\d{4}.*?)</span>', re.M)
        result = re.findall(p, html_txt)
        return result

    def __refresh_cmd(self):
        webdriver.ActionChains(self.__web_driver).key_down(Keys.END).perform()
        wait_refresh()

    def __valid_pages(self, pages):
        ret = []
        for p in pages:
            dt = my_str2dt(p[2])
            if dt >= self.__last_date:
                ret.append(p)

        return ret

    def __extract_pages(self):
        for i in range(END_CMD_LIMIT):
            self.__refresh_cmd()
            print('%s: send end command %d/%d' %
                  (self.__username, i+1, END_CMD_LIMIT))

        pages = self.__find_pages()
        self.__page_list = self.__valid_pages(pages)
        self.__web_driver.quit()


def extract_pic_type_1(res):
    html_text = res.text
    p = re.compile(
        '(http://p.+?pstatp.com/large/.+?)&quot', re.S)
    # p = re.compile(
    #     '(http://p.+?pstatp.com/large/pgc-image/.+?)&quot', re.S)
    result = re.findall(p, html_text)
    return result


def extract_pic_type_2(res):
    html_text = res.text
    # p = re.compile(
    #     '\"url\":\"http:\\/\\/p1.pstatp.com\\/origin\\/pgc-image\\/b222b8f1f6724931bd385f874cbefc09\"', re.S)
    p = re.compile(
        r':\[{\\\"url\\\":\\\"(http:\\\\/\\\\/p.+?pstatp.com.*?)\\\",.*?url_list', re.S)
    p = re.compile(
        r'\"url_list\\\":\[{\\\"url\\\":\\"(http:\\\\/\\\\/p.+?.pstatp.com.*?)\\\"}', re.S)
    result = re.findall(p, html_text)
    # print(result)
    return result


def get_pic_urls_from_a_page(page_url):
    res = requests.get(page_url)
    if res.status_code == 200:
        result = extract_pic_type_1(res)
        if result != []:
            return result
        result = extract_pic_type_2(res)
        if result != []:
            return result

        else:
            print('Error: %s %s' % (ERR_WEB_EXTRACT_FAIL, page_url))
            return []
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
    for url in pic_urls:
        pic_url = url.replace('\\', '')
        filename = username + '_' + pic_url.split('/')[-1] + '.jpg'
        save_a_pic(pic_url, save_path, filename)


# def save_log():
#     log_file = DST_PATH + r'\log\log_tt.txt'
#     now_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
#     with open(log_file, 'w') as f:
#         f.write(now_date + '\n')


def open_log():
    global f_log
    log_file = DST_PATH + r'\log\log_tt.txt'
    f_log = open(log_file, 'w')


def save_date():
    # global f_log
    now_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    f_log.write(now_date + '\n')


def save_info(info):
    # global f_log
    f_log.write('=' * 30)
    f_log.write('\n')
    f_log.write(info)
    f_log.close()


def wait_any_key():
    print('press any key to exit...')
    msvcrt.getch()


def print_version(version):
    print('=' * 70)
    print('%s version: %s' % (os.path.basename(__file__), VERSION))
    print('=' * 70)


def input_last_date():
    print('input last date:')
    input_line = sys.stdin.readline().strip()
    return input_line


def main():
    global pic_count
    # sys.stdout = io.TextIOWrapper(
    #     sys.stdout.buffer, encoding='gb18030', line_buffering=True)

    print_version(VERSION)

    save_path_date = r'%s\%s_tt' % (
        DST_PATH, datetime.datetime.now().date().strftime('%y%m%d'))

    if(not os.path.exists(save_path_date)):
        os.makedirs(save_path_date, exist_ok=True)

    open_log()
    save_date()

    last_date = my_str2dt(input_last_date())

    for (username, uid, mid) in all_users:
        user_url = 'https://www.toutiao.com/c/user/%s/#mid=%s' % (uid, mid)
        tt = TTUserValidPages(username, user_url, last_date)
        pages = tt.page_list
        count_pages = len(pages)
        for i in range(count_pages):
            page_url = 'https://www.toutiao.com/i%s/' % pages[i][0]
            print('%s %s [%d/%d] ' % (page_url, pages[i][2], i+1, count_pages))
            download_a_page(username, page_url, save_path_date)

    print('=' * 70)
    print('%d pictures download' % pic_count)
    save_info('%d pictures download' % pic_count)

    wait_any_key()


if __name__ == '__main__':
    main()
