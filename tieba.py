# history:
# 2019/03/28  v2.4  add input function

import re
import requests
import os
import time
import datetime
import sys
import getopt
import io
import msvcrt

stars_obs = ['周慧敏', '王祖贤']

stars = ['孙允珠', '滨崎步', '安室奈美惠', '相武纱季', '刚力彩芽', '朝比奈彩',
         '藤原纪香', '藤本美贵', '后藤真希', '桥本丽香', '石原里美',
         '堀北真希', '深田恭子', '北川景子', '黑木明纱', '久住小春',
         '木下亚由美', '桐谷美玲', '松浦亚弥', '佐佐木希', '常盘贵子',
         '上户彩', '酒井法子', '高桥爱', '泽尻英龙华', '水原希子',
         '张柏芝', '蔡卓妍', '钟欣桐', '陈慧琳',
         '朱茵', '张曼玉', '周海媚', '张敏',  '蒋怡',
         '陈法蓉', '钟楚红', '周秀娜', '熊黛林', '梁咏琪',
         '李嘉欣', '李彩桦', '李茏怡', '廖碧儿', '关芝琳', '黎姿',
         '李若彤', '梁洛施', '莫文蔚', 'maggieq', '王菲', '容祖儿', '杨恭如',
         '应采儿', '袁咏仪', 'angelababy', '邓丽欣', 'twins', '贾静雯', '陈德容',
         '张韶涵', '安以轩', '陈嘉桦', '张钧甯', '陈乔恩', '陈意涵', '陈妍希',
         '周子瑜', '范晓萱', '徐若瑄', '徐怀钰', '徐熙媛', '徐熙娣', '侯佩岑',
         '李玟', '林心如', '林嘉欣', '林熙蕾', '刘若英', '林依晨', '李倩蓉',
         '林志玲', '郭采洁', '吴佩慈', '孟广美', '任家萱', '萧亚轩', '蔡依林',
         '舒淇', '田馥甄', '王心凌',  '杨丞琳', '张庭', '卓文萱', 'she',
         '蔡琳', '韩彩英', '河智苑', '韩佳人', '韩艺瑟', '金喜善',
         '全智贤', '李英爱', '张娜拉', '李孝利', '金泰熙', '宋慧乔',
         '林允儿', '少女时代', '曹颖', '张延', '陈好', '陈红', '范冰冰',
         '董洁', '迪丽热巴', '黄奕', '高圆圆', '韩雪', '胡可', '霍思燕',
         '黄小蕾', '金莎', '甘婷婷', '古力娜扎', '李冰冰', '李小璐', '刘涛',
         '蒋勤勤', '刘亦菲', '李小冉', '金巧巧', '刘璇', '刘孜', '刘诗诗', '柳岩',
         '景甜', '江一燕', '李沁', '林允', '宁静', '马伊俐', '梅婷', '戚薇',
         '倪妮', '瞿颖', '沈星', '孙俪', '汤唯', '唐嫣', '佟丽娅', '徐静蕾',
         '许晴', '黄圣依', '王珞丹', '翟凌', '徐冬冬', '王子文', '赵薇', '张俪',
         '章子怡', '周迅', '张静初', '袁泉', '张含韵', '张靓颖', '马思纯',
         '于娜', '叶一茜', '杨幂', '张雨绮', '张梓琳', '姚晨', '张馨予', '殷桃',
         '周冬雨', '姚笛', '赵丽颖', '张天爱', '艾薇儿',
         '奥黛丽赫本', '卡梅隆·迪亚兹', '泽塔琼斯', '克劳馥', '艾玛沃特森', '艾玛',
         '梅根福克斯', '艾米莉亚克拉克', '希尔顿', '安妮·海瑟薇', '丽芙·泰勒', '朱迪福斯特', '米兰达可儿',
         '梅格瑞恩', '妮可基德曼', '娜塔丽', '麦当娜', '布兰妮', '苏菲玛索', '斯嘉丽·约翰逊',
         '克里斯汀·斯图尔特', '安吉丽娜朱莉', '李心洁', '戴佩妮',
         '唐艺昕', '潘晓婷', '关晓彤', '欧阳娜娜', '新垣结衣', '郭碧婷',
         '何穗', '奚梦瑶', '坎迪斯', '安布罗休', '辛芷蕾', '张蓝心', '钟楚曦', '宋祖儿', '张芷溪',
         '孙怡', '户田惠梨香', '白百合', '文咏珊', '林珍娜', '张雪迎', '杨超越', '桥本环奈',
         '林珍娜', '蛯原友里',
         'amberheard', 'mackenziefoy', 'evanrachelwood', 'lilyjames', 'emiliaclarke']


stars1 = ['蛯原友里']
# stars = ['孙允珠']

VERSION = '2.4'  # 版本号
# # star = '孙允珠'
# star = '倪妮'
# # star = '杨幂'
# # star = 'angelababy'
save_path = 'f:\download'  # 默认存放路径
INTERVAL = 0  # 下载一张图片间隔时间
INTERVAL1 = 0  # 访问原帖间隔时间
real_last = 0

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
        r = ''
        try:
            r = requests.get(url).text
        except Exception as e:
            print(e, ' -- Not found %s' % url)
        return r

    def post_id(self):
        '''
        通过图片贴的内容，找到原帖id
        # :return: 原帖id
        '''
        html_text = self.page_html()
        # p = re.compile('"post_id":(\d+)', re.S)
        p = re.compile('post_id\D+(\d+)', re.S)
        # result = re.search(p, html_text).group(1).strip()
        result = 0
        try:
            result = re.search(p, html_text).group(1).strip()
        except Exception as e:
            print(e, ' -- Not find post id')
        return result

    def find_all_pic(self):
        '''
        通过访问原帖找出pic的地址
        :return: 返回原帖日期及所有pic的地址
        '''
        time.sleep(INTERVAL1)
        post_id = self.post_id()
        url = 'http://tieba.baidu.com/p/%s?pid=%s#%s' % (
            self.tid, post_id, post_id)
        # r = requests.get(url=url, cookies=my_cookies, headers=my_headers)
        # r = requests.get(url)
        while(1):
            r = requests.get(url)
            if r.status_code == 200:
                break
        html_text = r.text
        # print(html_text)
        p = re.compile('http://imgsrc\.baidu\.com/forum/w.*?.jpg', re.S)
        # p = re.compile('src="http://imgsrc\.baidu\.com.*?.jpg"', re.S)
        l_pic = re.findall(p, html_text)
        p = re.compile('\d{4}-\d{2}-\d{2}', re.S)
        m = re.search(p, html_text)
        day = '0'
        try:
            day = m.group(0)
        except Exception as e:
            print(e, ' -- Not find day')

        # print(day)
        return day, l_pic

    def save_all_pic(self, test):
        '''
        下载原题网页的所有图片（在指定日期前的）
        :param test: test=True不下载，test=False下载
        :retuen: 下载数量
        '''
        count = 0
        day, l_pic = self.find_all_pic()
        if not test:
            for l in l_pic:
                self.save_a_pic(l)
                # pass  # for debug
        print('Download %d pictures %s %s' % (len(l_pic), self.name, day))
        count += len(l_pic)
        # else:
        #     print(self.name, day)
        return count

    def save_a_pic(self, pic_url):
        '''
        通过pic_url处理后，得到真正的图片地址，并下载
        :param pic_url:  从原帖取得的地址
        :return: 下载成功返回True
        '''
        save_file = pic_url.split('/')[-1]
        save_path_date = '%s\%s' % (
            save_path, datetime.datetime.now().date().strftime('%y%m%d'))
        # save_path_date = save_path + '\' +
        # datetime.datetime.now().date().strftime('%y  m % d')
        if not os.path.exists(save_path_date):
            os.mkdir(save_path_date)
        full_file = os.path.join(save_path_date, self.name + '_' + save_file)
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
        print('[Save] %s <%d bytes>' % (self.name + '_' + save_file, sz))
        time.sleep(INTERVAL)
        return True


class TiebaAll():
    '''
    根据贴吧名，找到图片汇总页，并下载相应的图片
    '''

    def __init__(self, name):
        self.name = name

    def page_urls(self):
        '''
        :return: 贴吧前10页的url
        '''
        urls = []
        s = ''
        for b in self.name.encode('utf-8'):
            s += '%%%2X' % b
        first_page_url = 'http://tieba.baidu.com/f?kw=%s&ie=utf-8' % s
        r = requests.get(first_page_url)
        p = re.compile(
            '<a href="(\S+)" class=" pagination-item " >\d+</a>', re.S)
        m = re.finditer(p, r.text)
        urls.append(first_page_url)
        for x in m:
            urls.append('http:%s' % x.group(1).strip())
        # print(urls)
        return urls

    def page_list(self):
        '''
        :return: 前10页所有帖子tid列表
        '''
        urls = []
        page_urls = self.page_urls()
        # print(page_urls)
        for page in page_urls:
            while(1):
                r = requests.get(page)
                if r.status_code == 200:
                    break
            # print(page)
            # print(r.text)
            p = re.compile(
                '<a rel="noreferrer"\s+?href="/p/(\d+)" title=', re.S)
            m = re.finditer(p, r.text)
            for x in m:
                urls.append(x.group(1).strip())
                # print(x.group(1).strip())
        # print(urls, len(urls))
        return urls


def download(star, last_id, test):
    '''
    下载一个指定贴吧，在某一日期前所有的图片
    :param star: 贴吧名
    :param last_id: 最后已下载的id
    :param test: test为True，则不下载
    :retuen: 下载数量
    '''
    global real_last
    count = 0

    tba = TiebaAll(star)
    l_tid = tba.page_list()
    # print(l_tid)
    for l in l_tid:
        if eval(l) > last_id:
            tb = TiebaPicPage(star, l)
            count += tb.save_all_pic(test)
            if eval(l) > real_last:
                real_last = eval(l)
    # print(l)
    print('----------------------------------------')
    print(star, count, 'pictures\n')
    if real_last > 0:
        save_log(str(real_last))
    return count


def download_all_stars(stars, last_id, test):
    '''
    下载一个指定贴吧，在某一日期前所有的图片
    :param stars: 贴吧名表
    :param last_id: 最后已下载的id
    :param test: test为True，则不下载
    '''
    count = 0
    for l in stars:
        count += download(l, last_id, test)
    print('----------------------------------------')
    print('Total', count, 'pictures')


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


def save_log(last_id):
    '''
    将last_id存到log文件
    :param last_id: 最后已下载的id
    :return: None
    '''
    log_file = save_path + '\log\log.txt'
    with open(log_file, 'w') as f:
        f.write(last_id + '\n')


def version():
    print('tieba.py %s' % VERSION)


def usage():
    print('tieba.py usage:')
    print('-h: print help message')
    print('-v: print version')
    print('-d: set mode')
    print('    auto - automatically download pictures')
    print('        argument: last_id')
    print('    star - download picture of a star')
    print('        argument: name last_id')
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

def input_last_id():
    print('input last id:')
    input_line = sys.stdin.readline().strip()
    return input_line


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
    last_id = eval(input_last_id())
    download_all_stars(stars, last_id, False)
    wait_any_key()

    # if len(sys.argv) == 1:
    #     usage_err()
    # try:
    #     opts, args = getopt.getopt(sys.argv[1:], 'hvd:t:')
    # except getopt.GetoptError:
    #     print(getopt.GetoptError.msg)
    #     usage_err()

    # if len(opts) == 0:
    #     usage_err()
    # for o, a in opts:
    #     if o == '-h':
    #         usage()
    #         sys.exit(0)
    #     elif o == '-v':
    #         version()
    #         sys.exit(0)
    #     elif o in ('-d', '-t'):
    #         if o == '-d':
    #             test = False
    #         else:
    #             test = True
    #         if a == 'auto':
    #             if len(args) != 1:
    #                 usage_err()
    #             else:
    #                 last_id = eval(args[0])
    #                 download_all_stars(stars, last_id, test)
    #         elif a == 'star':
    #             if len(args) != 2:
    #                 usage_err()
    #             else:
    #                 last_id = eval(args[1])
    #                 download(args[0], last_id, test)
    #         else:
    #             usage_err()


# def main():
# download_all_stars(stars, '2017-01-04', True)
# # tb = TiebaPicPage(star, '4963013075')
# # l_pid = tb.find_all_pic()
# # print(len(l_pid), l_pid)

if __name__ == '__main__':
    main()
