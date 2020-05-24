# history:
# 2020/05/24  v1.0  initial


import re
import requests
import json
import sys
import io
import os

VERSION = '1.0'

DST_PATH = r'f:\download\douban'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
}

ERR_WEB_ACCESS_FAIL = 'Cannot access web'
ERR_WEB_EXTRACT_FAIL = 'Cannot extract web'

pic_count = 0


def print_version(version):
    print('=' * 70)
    print('%s version: %s' % (os.path.basename(__file__), VERSION))
    print('=' * 70)


def usage():
    print('usage:')
    print('    %s album_url' % os.path.basename(__file__))


def get_page_text(url):
    try:
        res = requests.get(url, headers=HEADERS)
        return res.text
    except Exception:
        print('Error: %s %s' % (ERR_WEB_EXTRACT_FAIL, url))


def find_next_page(url):
    html_text = get_page_text(url)
    p = re.compile('<link rel="next" href="(.*?)"', re.S)
    result = re.search(p, html_text)
    if result:
        next_url = result.group(1)
        return next_url
    else:
        return ''


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


def download_a_page(url):
    html_text = get_page_text(url)
    # print(html_text)
    # <img src="https://img1.doubanio.com/view/photo/m/public/p2292192778.jpg" class="" />
    # <img src="https://img9.doubanio.com/view/photo/m/public/p2292280514.webp" class="" />
    # https://movie.douban.com/celebrity/1348586/photo/2295507479/#photo
    # https://img9.doubanio.com/view/photo/l/public/p2300271056.webp
    p = re.compile(
        '<img src="(https://img.*?.doubanio.com/view/photo/m/public/.*?)" class="" />', re.S)
    result = re.findall(p, html_text)
    # print(result)
    for a_pic_url in result:
        print(a_pic_url)
        print(a_pic_url.replace('/m/', '/l/'))
        print(a_pic_url)
        filename = a_pic_url.split('/')[-1]
        save_a_pic(a_pic_url, DST_PATH, filename)


def main():
    global pic_count

    print_version(VERSION)
    # if len(sys.argv) != 2:
    #     usage()
    #     sys.exit(1)

    # album_url = sys.argv[1]
    album_url = 'https://movie.douban.com/celebrity/1348586/photos/'
    album_url = 'https://movie.douban.com/celebrity/1316810/photos/'

    all_page_urls = [album_url]
    url = album_url

    while(True):
        next = find_next_page(url)
        if next == '':
            break
        else:
            all_page_urls.append(next)
            url = next

    n_page = len(all_page_urls)

    if(not os.path.exists(DST_PATH)):
        os.makedirs(DST_PATH, exist_ok=True)

    # for i in range(0, n_page):
    for i in range(0, 1):
        url = all_page_urls[i]
        download_a_page(url)
        print('page[%d/%d] <%d pictures>\n' % (i+1, n_page, pic_count))
        print(url)

    print('=' * 30)
    print('%d pictures download\n' % pic_count)


if __name__ == '__main__':
    main()
