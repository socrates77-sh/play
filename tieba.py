__author__ = 'socrates'

import re
import requests
import os
import time
import datetime
import sys
import getopt


stars = ['孙允珠', '倪妮', '杨幂', 'angelababy', '古力娜扎', '范冰冰', '李冰冰', '张静初', '唐嫣', '董洁',
         '高圆圆', '迪丽热巴','黄奕','韩雪','胡可','金莎','李小璐']
stars = ['李小璐']

VERSION = '1.0'  # 版本号
# # star = '孙允珠'
# star = '倪妮'
# # star = '杨幂'
# # star = 'angelababy'
save_path = 'e:\download'  # 默认存放路径
INTERVAL = 0.5  # 下载一张图片间隔时间

# my_cookies = dict(
# userFromPsNeedShowTab='1',
# BAIDUID='2439DBF33E30904DED8B39F29EB7CAF1',
# TIEBA_USERTYPE='23fdbb3618a28080716918e4',
# bdshare_firstime='1475328751554',
# BDUSS='WtCRFNXRXFIcENMcXZJbXRyV3ZCaX5GVmhnajEtRUVEeTZ-bEF3WEd-S2xYNzFZSVFBQUFBJCQAAAAAAAAAAAEAAADC5WUwV1oyS05RVEFEYQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKXSlVil0pVYN', \
# STOKEN='ce542d8fb8dddd60c90bf732b05795de88366d9095287fbaa1469c390c2c7be6',
# TIEBAUID='ae4849f4b018882d5440bee8', wise_device='0', LONGID='811984322')
#
# my_headers = {
# 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
# }


class TiebaPicPage():
    '''
    指定贴吧名，图片贴的id
    '''

    def __init__(self, name, tid):
        self.name = name
        self.tid = tid


    def page_url(self):
        '''
        :return: 图片贴的url
        '''
        s = ''
        for b in self.name.encode('utf-8'):
            s += '%%%2X' % b
        r = 'http://tieba.baidu.com/photo/p?kw=%s&fp=1&tid=%s' % (s, self.tid)
        return r

    def page_html(self):
        '''
        :return: 图片贴的html文本
        '''
        url = self.page_url()
        r = requests.get(url)
        # print(r.text)
        return r.text

    def post_id(self):
        '''
        通过图片贴的内容，找到原帖id
        :return: 原帖id
        '''
        html_text = self.page_html()
        # p = re.compile('"post_id":(\d+)', re.S)
        p = re.compile('post_id\D+(\d+)', re.S)
        result = re.search(p, html_text).group(1).strip()
        return result

    def find_all_pic(self):
        '''
        通过访问原帖找出pic的地址
        :return: 返回原帖日期及所有pic的地址
        '''
        post_id = self.post_id()
        url = 'http://tieba.baidu.com/p/%s?pid=%s#%s' % (self.tid, post_id, post_id)
        # r = requests.get(url=url, cookies=my_cookies, headers=my_headers)
        r = requests.get(url)
        html_text = r.text
        # print(html_text)
        p = re.compile('http://imgsrc\.baidu\.com/forum/w.*?.jpg', re.S)
        # p = re.compile('src="http://imgsrc\.baidu\.com.*?.jpg"', re.S)
        l_pic = re.findall(p, html_text)
        p = re.compile('\d{4}-\d{2}-\d{2}', re.S)
        m = re.search(p, html_text)
        day='0'
        try:
            day = m.group(0)
        except Exception as e:
            print(e,'Not find day')

        # print(day)
        return day, l_pic


    def save_all_pic(self, before_this_day, test):
        '''
        下载原题网页的所有图片（在指定日期前的）
        :param before_this_day: 制定日期
        :param test: test=True不下载，test=False下载
        '''
        day, l_pic = self.find_all_pic()
        if day >= before_this_day:
            if not test:
                for l in l_pic:
                    self.save_a_pic(l)
                    # pass  # for debug
            print('Download %d pictures %s %s' % (len(l_pic), self.name, day))
        else:
            print(self.name, day)

    def save_a_pic(self, pic_url):
        '''
        通过pic_url处理后，得到真正的图片地址，并下载
        :param pic_url:  从原帖取得的地址
        :return: 下载成功返回True
        '''
        save_file = pic_url.split('/')[-1]
        full_file = os.path.join(save_path, self.name + '-' + save_file)
        pid = save_file.split('.')[0]
        down_url = 'http://imgsrc.baidu.com/forum/pic/item/%s.jpg' % pid
        try:
            res = requests.get(down_url, timeout=60)
            if res.status_code != 200:
                return False
        except Exception as e:
            print(e)
            return False
        sz = open(full_file, 'wb').write(res.content)
        print('[Save] %s <%d bytes>' % (save_file, sz))
        time.sleep(INTERVAL)
        return True


class TiebaAll():
    '''
    根据贴吧名，找到图片汇总页，并下载相应的图片
    '''

    def __init__(self, name):
        self.name = name

    def page_url(self):
        '''
        :return: 图片汇总页的url
        '''
        s = ''
        for b in self.name.encode('utf-8'):
            s += '%%%2X' % b
        r = 'http://tieba.baidu.com/f?kw=%s&tab=album&subTab=album_thread' % s
        # print(r)
        return r

    def page_html(self):
        '''
        :return: 图片汇总页的html文本
        '''
        url = self.page_url()
        r = requests.get(url)
        # print(r.text)
        return r.text

    def page_list(self):
        '''
        在图片汇总页找到所有的图片贴
        :return: 图片贴的id列表
        '''
        html_text = self.page_html()
        p = re.compile('id="pic_item_(\d+)"', re.S)
        l_tid = []
        m = re.finditer(p, html_text)
        for x in m:
            l_tid.append(x.group(1).strip())
        # print(l_tid)
        return l_tid


def download(star, before_this_day, test):
    '''
    下载一个指定贴吧，在某一日期前所有的图片
    :param star: 贴吧名
    :param before_this_day: 指定的日期
    :param test: test为True，则不下载
    '''
    tba = TiebaAll(star)
    l_tid = tba.page_list()
    # print(l_tid)
    for l in l_tid:
        tb = TiebaPicPage(star, l)
        tb.save_all_pic(before_this_day, test)


def download_all_stars(stars, before_this_day, test):
    '''
    下载一个指定贴吧，在某一日期前所有的图片
    :param stars: 贴吧名表
    :param before_this_day: 指定的日期
    :param test: test为True，则不下载
    '''
    for l in stars:
        download(l, before_this_day, test)


def get_day(y, m, d):
    '''
    指定y（年），m（月），d（日），得到如下格式2017-02-07
    :param y: 年
    :param m: 月
    :param d: 日
    :return: 返回指定格式
    '''
    d = datetime.date(y, m, d)
    str = d.strftime('%Y-%m-%d')
    # print(type(str), str)
    return str


def version():
    print('tieba.py %s' % VERSION)


def usage():
    print('tieba.py usage:')
    print('-h: print help message')
    print('-v: print version')
    print('-d: set mode')
    print('    auto - automatically download pictures')
    print('        argument: y m d')
    print('    star - download picture of a star')
    print('        argument: name y m d')
    print('-t: set mode for try')
    print('        argument: same as -d, but not realy download')


def usage_err():
    print('ERROR: invalid option or argument')
    usage()
    sys.exit(1)


# def main():
# argn = len(sys.argv)
# if argn == 2:
# download(eval(sys.argv[1]))
# else:
# usage_err()

def main():
    if len(sys.argv) == 1:
        usage_err()
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hvd:t:')
    except getopt.GetoptError:
        print(getopt.GetoptError.msg)
        usage_err()
    for o, a in opts:
        if o == '-h':
            usage()
            sys.exit(0)
        elif o == '-v':
            version()
            sys.exit(0)
        elif o in ('-d', '-t'):
            if o == '-d':
                test = False
            else:
                test = True
            if a == 'auto':
                if len(args) != 3:
                    usage_err()
                else:
                    day = get_day(eval(args[0]), eval(args[1]), eval(args[2]))
                    download_all_stars(stars, day, test)
            if a == 'star':
                if len(args) != 4:
                    usage_err()
                else:
                    day = get_day(eval(args[0]), eval(args[1]), eval(args[2]))
                    download(args[0], day, test)
        else:
            usage()
            sys.exit(1)

# def main():
# download_all_stars(stars, '2017-01-04', True)
# # tb = TiebaPicPage(star, '4963013075')
# # l_pid = tb.find_all_pic()
# # print(len(l_pid), l_pid)


if __name__ == '__main__':
    main()

