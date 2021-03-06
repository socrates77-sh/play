# history:
# 2019/05/19  v1.0  initial
# 2019/06/01  v1.1  optimize display
# 2019/06/22  v1.2  modify log
# 2019/07/25  v1.3  update web access method
# 2019/12/08  v1.4  change chrome options
# 2019/12/28  v1.6  update extract_pic_type_3

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
from selenium.webdriver.support.wait import WebDriverWait

VERSION = '1.5'

DST_PATH = r'f:\download'

# https://www.toutiao.com/c/user/107952533857/#mid=1628218742667278
# https://www.toutiao.com/c/user/4472462177744952/#mid=1634147228048398
# https://www.toutiao.com/c/user/4472462177744952/#mid=1634147228048398
# (username, uid, mid, weitoutiao)

all_users = [
    # ('孙允珠美珠', '1789630365055400', '1658847850889223', False),
    # ('dissemblerSH', '110928569060', '1625448678462467', False),
    # ('孙允珠图赏', '3199462578', '50394050415', False),
    # ('灵犀之声', '51595829405', '51590705887', False),
    # ('虚竹他爹', '72972943448', '1609046918037511', False),
    # ('美事图说', '78359514777', '1630072746298382', False),
    # ('美人图赏', '3640708109', '1566815609876482', False),
    # ('倾城视图', '58868350934', '1577199391283214', False),
    # ('图影度光阴', '65767525786', '1631120772459524', False),
    # ('一路高飞', '4187341958', '1575656257167374', False),
    # ('在下子程', '3161840699049672', '1650812929504263', False),
    # ('小小的世界我只保护泥', '3635977242', '1570148542825474', False),
    # ('丹丹视觉美', '89923571455', '1591554527990797', False),
    # ('美图珠', '61704193641', '1589024159354893', False)

    # ('周秀娜', '63324591791', '63326138854', True),
    # ('Angelababy情报站', '4472462177744952', '1634147228048398', True),
    # ('AngelaBaby官方粉丝团', '53020919205', '1554133922026497', True),
    # ('Dear迪丽热巴后援会', '83228158038', '1588018019031053', True),
    # ('Dear迪丽热巴部落', '87064177182', '1593266355155971', True),
    # ('迪丽热巴吧', '82810146175', '1587817676795918', True),
    # ('杨幂官方粉丝团', '74176036712', '1582880577073165', True),
    # ('唐嫣', '53750742095', '53910221361', True),
    # ('莫文蔚', '67027185115', '66938754237', True),
    # ('赵丽颖颖宝', '86304143775', '1589728210990087', True),
    # ('郭碧婷', '59283663371', '59258777731', True),
    # ('TwiceChic', '88759632870', '59258777731', True),
    # ('江一燕', '52567586994', '52593173007', True),
    # ('时尚巴莎', '3506867453', '3456229542', True),
    # ('嘉人', '4734412771', '4734412771', True),
    # ('辛芷蕾', '18908392620', '60783515819', True),
    # ('倪妮', '55614951807', '55667333055', True),
    # ('刘亦菲', '63874654903', '63896281829', True),
    # ('张俪', '1842368843', '3148925926', True),
    # ('董洁', '52448714594', '52448834772', True),
    # ('张静初', '56137701890', '56082754590', True),
    # ('歐陽娜娜Nana', '58512505418', '58376920867', True),
    # ('邓丽欣', '69704938139', '69610691059', True),
    # ('孙怡', '7866749048', '55665864123', True),
    # ('赵薇V爱', '109064938509', '1620803459355655', True),
    # ('文咏珊', '102106709586', '1607132784850948', True),
    # ('许晴的窝窝', '88594173917', '1629056073226254', True),
    # ('张钧甯', '103401034929', '1609648790618119', True),
    # ('关晓彤', '6867592696', '59899061090', True),
    # ('黄圣依', '54650316956', '54652189281', True),
    # ('林允儿YOONAYA应援站', '87472203354', '1590351320123399', True),
    # ('张天爱', '51869645312', '51891565257', True),
    # ('郭碧婷', '59283663371', '59258777731', True),
    # ('莫文蔚', '67027185115', '66938754237', True),
    ('时尚中国', '96454134877', '1596815857982478', True)
]

all_users = [all_users[0]]

ERR_WEB_ACCESS_FAIL = 'Cannot access web'
ERR_WEB_EXTRACT_FAIL = 'Cannot extract web'

WAIT_RESPONSE = 5
END_CMD_LIMIT = 50
# END_CMD_LIMIT = 200
# END_CMD_LIMIT = 2

pic_count = 0
f_log = 0


def my_str2dt(dt_str):
    return datetime.datetime.strptime(dt_str, "%Y-%m-%d %H:%M")


def wait_refresh():
    time.sleep(WAIT_RESPONSE)


class TTUserValidPages():
    def __init__(self, username, user_url, last_date, weitoutiao):
        self.weitoutiao = weitoutiao
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
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('disable-infobars')
        # chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        chrome_options.add_argument("--proxy-server=127.0.0.1:8080")
        chrome_options.add_argument("--ignore-certificate-errors")
        self.__web_driver = webdriver.Chrome(options=chrome_options)
        # self.__web_driver = webdriver.Firefox(options=chrome_options)2020
        # self.__web_driver = webdriver.Chrome()
        # self.__web_driver = webdriver.Firefox()
        # print(user_url)
        self.__web_driver.get(user_url)
        wait_refresh()
        # wait = WebDriverWait(self.__web_driver, 30)


# 　      elm = wait.until(lambda x: x.find_element_by_xpath(Xpath))
        if self.weitoutiao:
            tab_xpath = '//div[@id="wrapper"]/div[2]/div[1]/ul/li[3]'
            elem = self.__web_driver.find_element_by_xpath(xpath=tab_xpath)
            # elem = wait.until(
            #     self.__web_driver.find_element_by_xpath(xpath=tab_xpath))

            if elem:
                elem.click()
                wait_refresh()
                # self.weitoutiao = True

    def __find_pages(self):
        html_txt = self.__web_driver.page_source
        if self.weitoutiao:
            p = re.compile(
                '"ugc_comment_count" target="_blank" href="(https://www.toutiao.com/a.+?)".+?(;)(\d{4}-\d{2}-\d{2} \d{2}:\d{2})', re.S)
        else:
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


def extract_pic_type_1(html_text):
    p = re.compile('(http://p.+?pstatp.com/large/pgc-image/.+?)"', re.S)
    # http://p9.pstatp.com/large/pgc-image/f52f5ffc3842460ea84f492276e6542d
    result = re.findall(p, html_text)
    return result


def extract_pic_type_2(html_text):
    p = re.compile(
        'url_list....{."url.":."http:\\\\.+?(p.+?pstatp.com)\\\\.+?origin\\\\.+?pgc-image\\\\.......(.+?)"', re.S)
    result = re.findall(p, html_text)
    pic_urls = []
    for (p, id) in result:
        url = 'http://%s/origin/pgc-image/%s' % (p, id)
        pic_urls.append(url)
    # print(result)
    return pic_urls


def extract_pic_type_3(html_text):
    # p = re.compile(
    #     '"\\\\u002F\\\\u002F(p.+?-tt.byteimg.com)\\\\u002Fimg\\\\u002Fpgc-image\\\\u002F(.+?)"', re.S)
    p = re.compile(
        '"\\\\u002F\\\\u002F(p.+?-tt.byteimg.com)\\\\u002Fimg\\\\u002F(.+?)\\\\u002F(.+?)\?.+?"', re.S)
    result = re.findall(p, html_text)
    # print(result)
    pic_urls = []
    for (p, img, id) in result:
        url = 'https://%s/img/%s/%s' % (p, img, id)
        # print(url)
        pic_urls.append(url)
    return pic_urls


# def extract_pic_type_4(html_text):
#     p = re.compile(
#         '"\\\\u002F\\\\u002F(p.+?-tt.byteimg.com)\\\\u002Fimg\\\\u002Ftos-cn-i-0022\\\\u002F(.+?)"', re.S)
#     result = re.findall(p, html_text)
#     pic_urls = []
#     for (p, id) in result:
#         url = 'https://%s/img/tos-cn-i-0022/%s' % (p, id)
#         # print(url)
#         pic_urls.append(url)
#     return pic_urls


def get_page_source(page_url):
    chrome_options = Options()
    # chrome_options.add_argument('--headless')
    browser = webdriver.Chrome(options=chrome_options)
    browser.get(page_url)
    time.sleep(WAIT_RESPONSE)
    html = browser.page_source
    browser.quit()
    return html


def get_pic_urls_from_a_page(page_url):
    html = get_page_source(page_url)
    # print(html)
    if html:
        result = extract_pic_type_1(html)
        if result != []:
            return result
        result = extract_pic_type_2(html)
        if result != []:
            return result
        result = extract_pic_type_3(html)
        if result != []:
            return result
        # result = extract_pic_type_4(html)
        # if result != []:
        #     return result

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
    # print(pic_urls)
    for url in pic_urls:
        # print(url)
        pic_url = url.replace('\\', '')
        # pic_url = pic_url.replace('=', '')
        # pic_url = pic_url.replace('?', '')
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

    for (username, uid, mid, weitoutiao) in all_users:
        user_url = 'https://www.toutiao.com/c/user/%s/#mid=%s' % (uid, mid)
        tt = TTUserValidPages(username, user_url, last_date, weitoutiao)
        pages = tt.page_list
        # print(pages)
        count_pages = len(pages)
        for i in range(count_pages):
            if tt.weitoutiao:
                page_url = pages[i][0]
            else:
                page_url = 'https://www.toutiao.com/i%s/' % pages[i][0]
            print('%s %s [%d/%d] ' % (page_url, pages[i][2], i+1, count_pages))
            download_a_page(username, page_url, save_path_date)

    print('=' * 70)
    print('%d pictures download' % pic_count)
    save_info('%d pictures download' % pic_count)

    wait_any_key()


if __name__ == '__main__':
    main()
