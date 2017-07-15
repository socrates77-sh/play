import re
import requests
import win32con
import win32clipboard as w

VERSION = '1.0'


def get_all_link(url):
    l_link = []
    try:
        r = requests.get(url)
    except Exception as e:
        print(e, ' -- Cannot access %s' % url)
        return None
    # print(r.encoding)
    r.encoding = 'gbk'
    # print(r.content)
    txt = r.text
    # print(txt)
    # p = re.compile('<a href="(.*?)">', re.S)
    p = re.compile('<a href="(.*?)">.*?</td>')
    # p = re.compile('<a href="ftp://g:g@tv.dl1234.com:2121/白', re.S)
    m = re.finditer(p, txt)
    for x in m:
        l_link.append(x.group(1).strip())

    return l_link


def main():
    url = input("请输入url: ")
    # url = 'http://www.ygdy8.com/html/tv/hytv/20170517/54012.html'

    download = ''
    for l in get_all_link(url):
        download += l + '\n'

    if len(download) != 0:
        w.OpenClipboard()
        w.EmptyClipboard()
        w.SetClipboardData(win32con.CF_UNICODETEXT, download)
        w.CloseClipboard()

if __name__ == '__main__':
    main()
