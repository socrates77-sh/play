# history:
# 2019/05/15  v1.0  initial


import os
import sys
import msvcrt
import re
import requests
import json
import sqlite3
from win32.win32crypt import CryptUnprotectData


VERSION = '1.0'

DST_PATH = r'e:\download\5'

# ('username', 'id', type)
# type, main page url like:
# 0：https://www.toutiao.com/m1628218742667278/
# 1: https://www.toutiao.com/c/user/58868350934/#mid=1577199391283214
all_users = [
    ('安全的情网', '1628218742667278', 0),
    ('倾城视图', '58868350934', 1),
    ('图影度光阴', '65767525786', 1),
    ('在下子程', '61713811819', 1)
]

ERR_WEB_ACCESS_FAIL = 'Cannot access web'
ERR_WEB_EXTRACT_FAIL = 'Cannot extract web'

# MY_COOKIES = dict(
#     tt_webid='6691101051205502477',
#     WEATHER_CITY='%E5%8C%97%E4%BA%AC',
#     UM_distinctid='16ab9aea4d23f1-0cdb430dfdfdd6-8383268-100200-16ab9aea4d334b',
#     csrftoken='921e5b74805b24ab139be1ca38fcead9',
#     s_v_web_id='c44b6a1e4cb787de9d6e29c8aa76d1bc',
#     passport_auth_status='7ba19e5c8c1250194a7d44722e21de6c',
#     sso_uid_tt='1def03a7e1503fc53068b964e250e137',
#     toutiao_sso_user='677fad1be30833611f169f1933509938',
#     login_flag='24dd313bfc805db42654cc776c8b9985',
#     sessionid='8e4f38c474c2c27f0d49bfe44eeda260',
#     uid_tt='b5494efde40796477d4b367260e23678',
#     sid_tt='8e4f38c474c2c27f0d49bfe44eeda260',
#     sid_guard="8e4f38c474c2c27f0d49bfe44eeda260|1557893910|15552000|Mon\054 11-Nov-2019 04:18:30 GMT",
#     __tasessionId='65yldlp911557906502579',
#     CNZZDATA1259612802='2057682951-1557889129-%7C1557905329'
# )

MY_COOKIES = dict(
    UM_distinctid='16ab9aea4d23f1-0cdb430dfdfdd6-8383268-100200-16ab9aea4d334b',
    csrftoken='921e5b74805b24ab139be1ca38fcead9',
    passport_auth_status='7ba19e5c8c1250194a7d44722e21de6c',
    sso_uid_tt='1def03a7e1503fc53068b964e250e137',
    toutiao_sso_user='677fad1be30833611f169f1933509938',
    login_flag='24dd313bfc805db42654cc776c8b9985',
    sessionid='8e4f38c474c2c27f0d49bfe44eeda260',
    uid_tt='b5494efde40796477d4b367260e23678',
    sid_tt='8e4f38c474c2c27f0d49bfe44eeda260',
    sid_guard="8e4f38c474c2c27f0d49bfe44eeda260|1557893910|15552000|Mon\054 11-Nov-2019 04:18:30 GMT",
    tt_webid='75486819522',
    uuid="w:ae821e41340d4a53b131b77fedd32970",
    __tasessionId='mw3jwv1mw1558087742926',
    s_v_web_id='c44b6a1e4cb787de9d6e29c8aa76d1bc',
    cp='5CDEB89CBAE84E1',
    CNZZDATA1259612802='2057682951-1557889129-%7C1558088929'
)

MY_HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
}


class TTUserType0():
    def __init__(self, user_id):
        self.__page_list = []
        self.__extract_page(user_id)

    def __extract_page(self, user_id):
        url = 'https://www.toutiao.com/pgc/ma/?media_id=%s&page_type=1&max_behot_time=0&count=10&version=2&platform=pc&as=A1853C3D2E98CA8&cp=5CDEB89CBAE84E1' % user_id
        res = requests.get(url, headers=MY_HEADERS)
        print(res.text)


def getcookiefromchrome(host='.oschina.net'):
    cookiepath = os.environ['LOCALAPPDATA'] + \
        r"\Google\Chrome\User Data\Default\Cookies"
    sql = "select host_key,name,encrypted_value from cookies where host_key='%s'" % host
    # sql = "select host_key,name,encrypted_value from cookies"
    with sqlite3.connect(cookiepath) as conn:
        cu = conn.cursor()
        cookies = {name: CryptUnprotectData(encrypted_value)[1].decode(
        ) for host_key, name, encrypted_value in cu.execute(sql).fetchall()}
        # print(cookies)
        return cookies


def getcookiefrom360se(host='.oschina.net'):
    cookiepath = os.environ['APPDATA'] + \
        r"\360se6\User Data\Default\Cookies"
    sql = "select host_key,name,encrypted_value from cookies where host_key='%s'" % host
    # sql = "select host_key,name,encrypted_value from cookies"
    with sqlite3.connect(cookiepath) as conn:
        cu = conn.cursor()
        # print(cu.execute(sql).fetchall())
        cookies = {name: CryptUnprotectData(encrypted_value)[1].decode(
        ) for host_key, name, encrypted_value in cu.execute(sql).fetchall()}
        # print(cookies)
        return cookies


def print_data_field(data, field):
    num = 0
    for d in data:
        if field in d.keys():
            print(num, d[field])
            num += 1


def get_valid_page_id(data):
    result = []
    for d in data:
        if 'title' in d.keys():
            result.append(d['id'])
    return result


def scan_all_pages(username):
    i = 0
    while(1):
        offset = i*20
        url = 'https://www.toutiao.com/api/search/content/?aid=24&app_name=web_search&offset=%d&format=json&keyword=%s' % (
            offset, username)
        res = requests.get(url, cookies=MY_COOKIES)
        html_json = res.json()
        print('return_count', html_json['return_count'])
        print('has_more', html_json['has_more'])
        if html_json['return_count'] != 20:
            break
        i += 1


def get_page_urls_from_username(username):
    # url = 'https://www.toutiao.com/api/search/content/?aid=24&app_name=web_search&offset=40&format=json&keyword=%E5%AE%89%E5%85%A8%E7%9A%84%E6%83%85%E7%BD%91&autoload=true&count=200&en_qc=1&cur_tab=1&from=search_tab&pd=synthesis&timestamp=1557906650638'
    url = 'https://www.toutiao.com/api/search/content/?aid=24&app_name=web_search&offset=0&format=json&keyword=%s' % username
    res = requests.get(url, cookies=MY_COOKIES)
    # cookies = getcookiefromchrome('.toutiao.com')
    # print(cookies)
    if res.status_code == 200:
        html_json = res.json()
        # print(html_json)
        # print(json.dumps(html_json, indent=4))
        # # print(type(html_json))
        # print('return_count', html_json['return_count'])
        # print('offset', html_json['offset'])
        # print(html_json.keys())

        # print(len(html_json['data']))
        # print(html_json['data'][1].keys())
        # print(html_json['data'][1])
        # # print(html_json)
        # print_data_field(html_json['data'], 'title')
        # print_data_field(html_json['data'], 'id')
        valid_id = get_valid_page_id(html_json['data'])
        result = []
        for id in valid_id:
            url = 'https://www.toutiao.com/a%s' % id
            result.append(url)

        return result

        # pass

        # else:
        #     print('Error: %s %s' % (ERR_WEB_EXTRACT_FAIL, url))
    else:
        print('Error: %s %s' % (ERR_WEB_ACCESS_FAIL, url))


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


def save_a_pic(pic_url, file_name):
    full_file = os.path.join(DST_PATH, file_name)
    try:
        res = requests.get(pic_url, timeout=60)
        if res.status_code != 200:
            return False
    except Exception as e:
        print(e)
        return False
    sz = open(full_file, 'wb').write(res.content)
    print('[Save] %s <%d bytes>' % (file_name, sz))


def wait_any_key():
    print('press any key to exit...')
    msvcrt.getch()


def print_version(version):
    print('=' * 70)
    print('%s version: %s' % (os.path.basename(__file__), VERSION))
    print('=' * 70)


def main():
    # sys.stdout = io.TextIOWrapper(
    #     sys.stdout.buffer, encoding='gb18030', line_buffering=True)

    print_version(VERSION)

    if(not os.path.exists(DST_PATH)):
        os.makedirs(DST_PATH, exist_ok=True)

    # pic_url = 'http://p1.pstatp.com/origin/pgc-image/79c42c58f04b4de8887c3289607e3c99'
    # # pic_url = 'http://p1.pstatp.com/large/pgc-image/79c42c58f04b4de8887c3289607e3c99'
    # file_name = pic_url.split('/')[-1]+'.jpg'
    # save_a_pic(pic_url, file_name)

    # page_url = 'https://www.toutiao.com/a6690854000499098120/'  # type1
    # # page_url = 'https://www.toutiao.com/a6690434218440262156/'  # type2
    # # page_url = 'https://www.toutiao.com/a6475469222464979469' # type1_1
    # page_url = 'https://www.toutiao.com/i6691049901360415245/'  # type1_1
    # pic_urls = get_pic_urls_from_a_page(page_url)
    # print(len(pic_urls))
    # for url in pic_urls:
    #     pic_url = url.replace('\\', '')
    #     # print(pic_url)
    #     file_name = pic_url.split('/')[-1]+'.jpg'
    #     save_a_pic(pic_url, file_name)

    # username = '安全的情网'
    # username = '倾城视图'
    # page_urls = get_page_urls_from_username(username)
    # print(page_urls)

    # for page_url in page_urls:
    #     print(page_url)
    #     pic_urls = get_pic_urls_from_a_page(page_url)
    #     # print(len(pic_urls))
    #     for url in pic_urls:
    #         pic_url = url.replace('\\', '')
    #         file_name = username + '_' + pic_url.split('/')[-1] + '.jpg'
    #         save_a_pic(pic_url, file_name)

    # scan_all_pages(username)

    (username, id, type) = all_users[0]
    print(id)

    tt = TTUserType0(id)

    # wait_any_key()


if __name__ == '__main__':
    main()
