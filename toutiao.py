# history:
# 2019/05/19  v1.0  initial
# 2019/06/01  v1.1  optimize display
# 2019/06/22  v1.2  modify log
# 2019/07/25  v1.3  update web access method
# 2019/12/08  v1.4  change chrome options
# 2019/12/28  v1.6  update extract_pic_type_3
# 2020/03/01  v2.0  new strategy

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


VERSION = '2.0'

URL_PREFIX = 'https://www.toutiao.com'
DST_PATH = r'f:\download'
# DST_PATH = r'e:\py\play\temp\download'
CHROME_LOG = DST_PATH + r'\log\chrome.log'
# CHROME_LOG = DST_PATH + r'\log\2.log'

my_cookies = dict(
    tt_webid='6741558964419626509',
    SLARDAR_WEB_ID='987ff669-f73a-441f-b1ba-87a050433e0a',
    s_v_web_id='verify_k7eq67da_j4Yz1vJS_0dp2_4abR_9KpO_s7BUUNoL7vKm',
    ttcid='8dfd4d1fe69146e09c563b761e16584694',
    __tasessionId='bihmlchj11583411248403',
    csrftoken='9a084254d44eab1965baf1a28dc168fd',
    tt_scid='N9jrBvIpLhMpmTyUTuR0GX2uRjDeagD8lmer6Bt7A.9aCg1VCJd7tZI8J7HKoO4Vdbd0')


my_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}


# https://www.toutiao.com/c/user/107952533857/#mid=1628218742667278
# https://www.toutiao.com/c/user/4472462177744952/#mid=1634147228048398
# https://www.toutiao.com/c/user/4472462177744952/#mid=1634147228048398
# (username, uid, mid, weitoutiao)
# username&weitoutiao is useless now

all_users = [
    ('孙允珠写真', '1077146809284925', '1628140616779787', False),
    ('孙允珠时尚写真', '6242084862', '1597610377320462', False),
    ('孙允珠美珠', '1789630365055400', '1658847850889223', False),
    ('dissemblerSH', '110928569060', '1625448678462467', False),
    ('孙允珠图赏', '3199462578', '50394050415', False),
    ('灵犀之声', '51595829405', '51590705887', False),
    ('虚竹他爹', '72972943448', '1609046918037511', False),
    ('美事图说', '78359514777', '1630072746298382', False),
    ('美人图赏', '3640708109', '1566815609876482', False),
    ('倾城视图', '58868350934', '1577199391283214', False),
    ('图影度光阴', '65767525786', '1631120772459524', False),
    ('一路高飞', '4187341958', '1575656257167374', False),
    ('在下子程', '3161840699049672', '1650812929504263', False),
    ('小小的世界我只保护泥', '3635977242', '1570148542825474', False),
    ('丹丹视觉美', '89923571455', '1591554527990797', False),
    ('美图珠', '61704193641', '1589024159354893', False),

    ('周秀娜', '63324591791', '63326138854', True),
    ('Angelababy情报站', '4472462177744952', '1634147228048398', True),
    ('AngelaBaby官方粉丝团', '53020919205', '1554133922026497', True),
    ('Dear迪丽热巴后援会', '83228158038', '1588018019031053', True),
    ('Dear迪丽热巴部落', '87064177182', '1593266355155971', True),
    ('迪丽热巴吧', '82810146175', '1587817676795918', True),
    ('杨幂官方粉丝团', '74176036712', '1582880577073165', True),
    ('唐嫣', '53750742095', '53910221361', True),
    ('莫文蔚', '67027185115', '66938754237', True),
    ('赵丽颖颖宝', '86304143775', '1589728210990087', True),
    ('郭碧婷', '59283663371', '59258777731', True),
    ('TwiceChic', '88759632870', '59258777731', True),
    ('江一燕', '52567586994', '52593173007', True),
    ('时尚巴莎', '3506867453', '3456229542', True),
    ('嘉人', '4734412771', '4734412771', True),
    ('辛芷蕾', '18908392620', '60783515819', True),
    ('倪妮', '55614951807', '55667333055', True),
    ('刘亦菲', '63874654903', '63896281829', True),
    ('张俪', '1842368843', '3148925926', True),
    ('董洁', '52448714594', '52448834772', True),
    ('张静初', '56137701890', '56082754590', True),
    ('歐陽娜娜Nana', '58512505418', '58376920867', True),
    ('邓丽欣', '69704938139', '69610691059', True),
    ('孙怡', '7866749048', '55665864123', True),
    ('赵薇V爱', '109064938509', '1620803459355655', True),
    ('文咏珊', '102106709586', '1607132784850948', True),
    ('许晴的窝窝', '88594173917', '1629056073226254', True),
    ('张钧甯', '103401034929', '1609648790618119', True),
    ('关晓彤', '6867592696', '59899061090', True),
    ('黄圣依', '54650316956', '54652189281', True),
    ('林允儿YOONAYA应援站', '87472203354', '1590351320123399', True),
    ('张天爱', '51869645312', '51891565257', True),
    ('时尚中国', '96454134877', '1596815857982478', True)
]

all_users1 = [all_users[0]]

WAIT_RESPONSE = 5

ERR_WEB_ACCESS_FAIL = 'Cannot access web'
ERR_WEB_EXTRACT_FAIL = 'Cannot extract web'

pic_count = 0
f_log = 0
f_missing = 0
last_time_new = 0


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
        try:
            images = eval(ret.group(1))
        except Exception:
            images = []
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


def open_log():
    global f_log
    global f_missing
    log_file = DST_PATH + r'\log\log_tt.txt'
    missing_file = DST_PATH + r'\log\missing_tt.txt'
    f_log = open(log_file, 'w')
    f_missing = open(missing_file, 'w')


def save_date():
    # global f_log
    now_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    f_log.write(now_date + '\n')


def save_info(info):
    # global f_log
    # f_log.write('=' * 30)
    # f_log.write('\n')
    f_log.write(info + '\n')
    # f_log.close()


def save_missing(info):
    f_missing.write(info + '\n')


def wait_any_key():
    print('press any key to exit...')
    msvcrt.getch()


def print_version(version):
    print('=' * 70)
    print('%s version: %s' % (os.path.basename(__file__), VERSION))
    print('=' * 70)


def input_last_time():
    print('input last time:')
    input_line = sys.stdin.readline().strip()
    return input_line


def input_refresh_http():
    print('refresh http [y/n]:')
    key_in = msvcrt.getch()
    choice = (key_in.decode() in 'yY')
    if choice:
        print('confirm!')
    else:
        print('skip refresh')
    return choice


def get_all_sheets_text(chrome_log_file):
    with open(chrome_log_file, 'r', encoding='utf-8') as f:
        l_lines = f.readlines()
    return l_lines


class SheetStyle(Enum):
    unknown = auto()
    article = auto()
    weitoutiao = auto()


class PageStyle(Enum):
    unknown = auto()
    type_1 = auto()
    type_2 = auto()
    type_3 = auto()
    type_4 = auto()


class TTSheet():
    def __init__(self, sheet_text):
        self.__text = sheet_text
        self.__json = json.loads(self.__text)

    @property
    def style(self):
        keys = self.__json.keys()
        if keys == {'data', 'message', 'has_more', 'next'}:
            return SheetStyle.weitoutiao
        elif keys == {'login_status', 'has_more', 'next', 'page_type', 'message', 'data', 'is_self'}:
            return SheetStyle.article
        else:
            return SheetStyle.unknown

    @property
    def page_count(self):
        if(self.style == SheetStyle.unknown):
            return None
        else:
            return len(self.__json['data'])

    @property
    def page_data(self):
        if self.style == SheetStyle.unknown:
            return []
        else:
            return self.__json['data']


class TTPage():
    def __init__(self, data):
        self._data = data
        if 'source' in data.keys():
            self.__type = PageStyle.type_1
        else:
            if data['concern_talk_cell']:
                self.__type = PageStyle.type_2
            elif data['stream_cell']['data_type'] == 1:
                self.__type = PageStyle.type_4
            else:
                self.__type = PageStyle.type_3

    def get_name(self):
        if self.__type == PageStyle.type_1:
            return self._data['source']
        elif self.__type == PageStyle.type_2:
            a = json.loads(self._data['concern_talk_cell']['packed_json_str'])
            return a['user']['name']
        else:
            a = json.loads(self._data['stream_cell']['raw_data'])
            return a['comment_base']['user']['info']['name']

    def get_title(self):
        if self.__type == PageStyle.type_1:
            return self._data['title']
        elif self.__type == PageStyle.type_2:
            a = json.loads(self._data['concern_talk_cell']['packed_json_str'])
            return a['content']
        else:
            a = json.loads(self._data['stream_cell']['raw_data'])
            # print(json.dumps(a, indent=4))
            return a['comment_base']['content']

    def get_time(self):
        if self.__type == PageStyle.type_1:
            return self._data['behot_time']
        elif self.__type == PageStyle.type_2:
            a = json.loads(self._data['concern_talk_cell']['packed_json_str'])
            return a['create_time']
        else:
            # a = json.loads(self._data['stream_cell']['raw_data'])
            return self._data['base_cell']['behot_time']

    def get_tid(self):
        if self.__type == PageStyle.type_1:
            return self._data['item_id']
        elif self.__type == PageStyle.type_2:
            a = json.loads(self._data['concern_talk_cell']['packed_json_str'])
            return a['thread_id']
        elif self.__type == PageStyle.type_4:
            return 'video'
        else:
            # a = json.loads(self._data['stream_cell']['raw_data'])
            return self._data['base_cell']['log_pb']['fw_id']


def open_chrome(uid, mid):
    chrome_option = '--proxy-server=127.0.0.1:8080 -ignore-certificate-errors'
    user_url = 'https://www.toutiao.com/c/user/%s/#mid=%s' % (uid, mid)
    os.system('chrome %s %s' % (chrome_option, user_url))


# user_url = 'https://www.toutiao.com/c/user/58512505418/#mid=58376920867'
# user_url = 'https://www.toutiao.com/c/user/96454134877/#mid=1596815857982478'
# user_url = 'https://www.toutiao.com/c/user/1789630365055400/#mid=1658847850889223'

def main():
    print_version(VERSION)
    if input_refresh_http():
        for i in range(len(all_users)):
            user = all_users[i]
            name = user[0]
            uid = user[1]
            mid = user[2]
            print('[%d/%d] %s' % (i+1, len(all_users), name))
            open_chrome(uid, mid)

        print('shutdown proxy first!!!')
        wait_any_key()

    global pic_count
    global last_time_new

    last_time = eval(input_last_time())
    # last_time = 1583136150
    last_time_new = last_time

    save_path_date = r'%s\%s_tt' % (
        DST_PATH, datetime.datetime.now().date().strftime('%y%m%d'))

    if(not os.path.exists(save_path_date)):
        os.makedirs(save_path_date, exist_ok=True)

    open_log()
    save_date()

    sheets_text = get_all_sheets_text(CHROME_LOG)

    for i in range(len(sheets_text)):
    # for i in range(69, len(sheets_text)):
        sheet = TTSheet(sheets_text[i])
        if sheet.style == SheetStyle.article:
            style_text = 'artile'
            page_code = 'i'
        else:
            style_text = 'weitoutiao'
            page_code = 'a'

        for j in range(len(sheet.page_data)):
            page = TTPage(sheet.page_data[j])
            # page = TTPage(sheet.page_data[6])
            page_url = '%s/%s%s' % (URL_PREFIX, page_code, page.get_tid())

            print()
            print(page_url)
            # print(page.get_title())
            # print(page.get_time())
            if page.get_time() <= last_time:
                print('===old & skip===')
            else:
                # print('===download===')
                if(page.get_tid() != 'video'):
                    ret = download_a_page(
                        page.get_name(), page_url, save_path_date)
                    # ret = 1
                    if ret:
                        if last_time_new < page.get_time():
                            last_time_new = page.get_time()
                    else:
                        save_missing(page_url)

            print('sheet[%d/%d]:%s, page[%d/%d] <%d pictures> ' % (i+1, len(sheets_text),
                                                                   style_text, j+1, len(sheet.page_data), pic_count))

    print('=' * 70)
    print('%d pictures download' % pic_count)
    save_info('=' * 30)
    save_info('%d pictures download\nlast: %d' % (pic_count, last_time_new))
    f_log.close()
    f_missing.close()

    wait_any_key()

    # s = sheets_text[0]
    # sheet = TTSheet(s)
    # d = sheet.page_data[5]
    # page = TTPage(d)
    # if sheet.style == SheetStyle.article:
    #     style_text = 'artile'
    #     page_code = 'i'
    # else:
    #     style_text = 'weitoutiao'
    #     page_code = 'a'
    # page_url = '%s/%s%s' % (URL_PREFIX, page_code, page.get_tid())
    # print(page.get_name())
    # print(page.get_title())
    # print(page.get_tid())
    # print(page.get_time())
    # print(page._data)
    # print(page._data['stream_cell']['data_type'])
    # download_a_page(page.get_name(), page_url, save_path_date)


if __name__ == '__main__':
    main()
