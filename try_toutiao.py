import time
import sys
import os
import re
import msvcrt
import datetime
import requests
import json

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

# my_cookies = dict(
#     tt_webid='6741558964419626509',
#     SLARDAR_WEB_ID='987ff669-f73a-441f-b1ba-87a050433e0a',
#     s_v_web_id='verify_k7eq67da_j4Yz1vJS_0dp2_4abR_9KpO_s7BUUNoL7vKm',
#     ttcid='8dfd4d1fe69146e09c563b761e16584694',
#     __tasessionId='bihmlchj11583411248403',
#     csrftoken='9a084254d44eab1965baf1a28dc168fd',
#     tt_scid='N9jrBvIpLhMpmTyUTuR0GX2uRjDeagD8lmer6Bt7A.9aCg1VCJd7tZI8J7HKoO4Vdbd0')

# my_headers = {
#     # 'authority':'www.toutiao.com',
#     # ':method':'GET',
#     # ':path':'/i6800151831243653636',
#     # ':scheme':'https',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
#     'upgrade-insecure-requests': '1',
#     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
#     'accept-encoding': 'gzip, deflate, br',
#     'accept-language': 'zh-CN,zh;q=0.9',
#     'cookie': 'WEATHER_CITY=%E5%8C%97%E4%BA%AC; csrftoken=9a084254d44eab1965baf1a28dc168fd; uuid="w:c38b69d1e33c4e6698438c6e10721f78"; tt_webid=6741558964419626509; tt_webid=6741558964419626509; msh=9AebRDpy-Ii7n6JBi5ufGdSyvNI; ttcid=8dfd4d1fe69146e09c563b761e16584694; __utma=24953151.78746598.1583071987.1583071987.1583071987.1; __utmz=24953151.1583071987.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); SLARDAR_WEB_ID=987ff669-f73a-441f-b1ba-87a050433e0a; __tasessionId=bihmlchj11583411248403; s_v_web_id=verify_k7es3uyu_aw7pkdjn_eS7m_4a6M_9yWY_MV6NXsVdpcgC; sso_auth_status=75c4b6af4e42130e41ebef5fc9b0c479; sso_uid_tt=d06556f51050312465ee34b600421cd2; toutiao_sso_user=b51da73521d5ed9b7ebf79f31372bd8c; passport_auth_status=9994c716ea8578c158f5b0808f7c6cbf%2Cfdf91bcae3ab8825ab1825b1db5f6fa7; sid_guard=511bdf8009eb1b3e09a6d96c8c37693e%7C1583416968%7C5184000%7CMon%2C+04-May-2020+14%3A02%3A48+GMT; uid_tt=6fc36973621b641cc0bd9d38e06cd922; sid_tt=511bdf8009eb1b3e09a6d96c8c37693e; sessionid=511bdf8009eb1b3e09a6d96c8c37693e; tt_scid=dSnU7b.dUC9.ot892meAU6u8SjBQN2seVHsBJIalk33GZxx99IA.yd3agwSdc-4Rcfbc'
# }

ERR_WEB_ACCESS_FAIL = 'Cannot access web'
ERR_WEB_EXTRACT_FAIL = 'Cannot extract web'


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
    web_driver = webdriver.Chrome(options=chrome_options)
    web_driver.minimize_window()
    web_driver.get(page_url)
    
    html_txt = web_driver.page_source
    print(html_txt)
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


def main():
    page_url = 'https://www.toutiao.com/i6800152751490728461'
    page_url = 'https://www.toutiao.com/i6800151831243653636'
    page_url = 'https://www.toutiao.com/a1652953486829582'
    page_url = 'https://www.toutiao.com/a1653816605107204'
    page_url = 'https://www.toutiao.com/i6800291741090972164'
    page_url = 'https://www.toutiao.com/i6795042890620862980'
    page_url = 'https://www.toutiao.com/a1652953486829582'
    # page_url = 'https://www.toutiao.com/a0000000000'

    ret = get_pic_urls_from_a_page(page_url)
    print(ret)
    print(len(ret))


if __name__ == '__main__':
    main()
