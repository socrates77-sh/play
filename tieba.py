__author__ = 'socrates'

import re
import requests
import os
import time
import datetime
import sys
import getopt


stars = ['孙允珠', '滨崎步', '安室奈美惠', '相武纱季', '刚力彩芽', '朝比奈彩',
         '藤原纪香', '藤本美贵', '后藤真希', '桥本丽香', '石原里美',
         '堀北真希', '深田恭子', '北川景子', '黑木明纱', '久住小春',
         '木下亚由美', '桐谷美玲', '松浦亚弥', '佐佐木希', '常盘贵子',
         '上户彩', '酒井法子', '高桥爱', '泽尻英龙华', '水原希子',
         '张柏芝', '蔡卓妍', '钟欣桐', '陈慧琳',
         '朱茵', '张曼玉', '周海媚', '张敏', '周慧敏', '蒋怡',
         '陈法蓉', '钟楚红', '周秀娜', '熊黛林', '梁咏琪',
         '李嘉欣', '李彩桦', '李茏怡', '廖碧儿', '关芝琳', '黎姿',
         '李若彤', '梁洛施', '莫文蔚', 'maggieq', '王菲', '容祖儿', '杨恭如',
         '应采儿', '袁咏仪', 'angelababy', '邓丽欣', 'twins', '贾静雯', '陈德容',
         '张韶涵', '安以轩', '陈嘉桦', '张钧甯', '陈乔恩', '陈意涵', '陈妍希',
         '周子瑜', '范晓萱', '徐若瑄', '徐怀钰', '徐熙媛', '徐熙娣', '侯佩岑',
         '李玟', '林心如', '林嘉欣', '林熙蕾', '刘若英', '林依晨', '李倩蓉',
         '林志玲', '郭采洁', '吴佩慈', '孟广美', '任家萱', '萧亚轩', '蔡依林',
         '舒淇', '田馥甄', '王心凌', '王祖贤', '杨丞琳', '张庭', '卓文萱', 'she',
         '权宝儿', '蔡琳', '韩彩英', '河智苑', '韩佳人', '韩艺瑟', '金喜善',
         '全智贤', '李英爱', '张娜拉', '李孝利', '金泰熙', '郑秀妍', '宋慧乔',
         '宋允儿', '少女时代', '曹颖', '张延', '陈好', '陈红', '范冰冰',
         '董洁', '迪丽热巴', '黄奕', '高圆圆', '韩雪', '胡可', '霍思燕',
         '黄小蕾', '金莎', '甘婷婷', '古力娜扎', '李冰冰', '李小璐', '刘涛',
         '蒋勤勤', '刘亦菲', '李小冉', '金巧巧', '刘璇', '刘孜', '刘诗诗', '柳岩',
         '景甜', '江一燕', '李沁', '鞠婧祎', '林允', '宁静', '马伊俐', '梅婷', '戚薇',
         '倪妮', '瞿颖', '沈星', '孙俪', '汤唯', '唐嫣', '佟丽娅', '徐静蕾',
         '许晴', '黄圣依', '王珞丹', '翟凌', '徐冬冬', '王子文', '赵薇',
         '章子怡', '周迅', '张静初', '袁泉', '张含韵', '张靓颖', '马思纯',
         '于娜', '叶一茜', '杨幂', '张雨绮', '张梓琳', '姚晨', '张馨予', '殷桃',
         '郑爽', '周冬雨', '姚笛', '赵丽颖', '张天爱', '艾薇儿',
         '奥黛丽赫本', '卡梅隆·迪亚兹', '泽塔琼斯', '克劳馥', '艾玛沃特森', '艾玛',
         '梅根福克斯', '艾米莉亚克拉克', '希尔顿', '安妮·海瑟薇', '丽芙·泰勒', '朱迪福斯特', '米兰达可儿',
         '梅格瑞恩', '妮可基德曼', '娜塔丽', '麦当娜', '布兰妮', '苏菲玛索',
         '克里斯汀·斯图尔特', '安吉丽娜朱莉', '李心洁', '戴佩妮']

stars = ['滨崎步', '安室奈美惠', '相武纱季', '刚力彩芽', '朝比奈彩',
         '藤原纪香', '藤本美贵', '后藤真希', '桥本丽香', '石原里美',
         '堀北真希', '深田恭子', '北川景子', '黑木明纱', '久住小春',
         '木下亚由美', '桐谷美玲', '松浦亚弥', '佐佐木希', '常盘贵子',
         '上户彩', '酒井法子', '高桥爱', '泽尻英龙华', '水原希子',
         '张柏芝', '蔡卓妍', '钟欣桐', '陈慧琳',
         '朱茵', '张曼玉', '周海媚', '张敏', '周慧敏', '蒋怡',
         '陈法蓉', '钟楚红', '周秀娜', '熊黛林', '梁咏琪',
         '李嘉欣', '李彩桦', '李茏怡', '廖碧儿', '关芝琳', '黎姿',
         '李若彤', '梁洛施', '莫文蔚', 'maggieq', '王菲', '容祖儿', '杨恭如',
         '应采儿', '袁咏仪', 'angelababy', '邓丽欣', 'twins', '贾静雯', '陈德容',
         '张韶涵', '安以轩', '陈嘉桦', '张钧甯', '陈乔恩', '陈意涵', '陈妍希',
         '周子瑜', '范晓萱', '徐若瑄', '徐怀钰', '徐熙媛', '徐熙娣', '侯佩岑',
         '李玟', '林心如', '林嘉欣', '林熙蕾', '刘若英', '林依晨', '李倩蓉',
         '林志玲', '郭采洁', '吴佩慈', '孟广美', '任家萱', '萧亚轩', '蔡依林',
         '舒淇', '田馥甄', '王心凌', '王祖贤', '杨丞琳', '张庭', '卓文萱', 'she',
         '权宝儿', '蔡琳', '韩彩英', '河智苑', '韩佳人', '韩艺瑟', '金喜善',
         '全智贤', '李英爱', '张娜拉', '李孝利', '金泰熙', '郑秀妍', '宋慧乔',
         '宋允儿', '少女时代', '曹颖', '张延', '陈好', '陈红', '范冰冰',
         '董洁', '迪丽热巴', '黄奕', '高圆圆', '韩雪', '胡可', '霍思燕',
         '黄小蕾', '金莎', '甘婷婷', '古力娜扎', '李冰冰', '李小璐', '刘涛',
         '蒋勤勤', '刘亦菲', '李小冉', '金巧巧', '刘璇', '刘孜', '刘诗诗', '柳岩',
         '景甜', '江一燕', '李沁', '鞠婧祎', '林允', '宁静', '马伊俐', '梅婷', '戚薇',
         '倪妮', '瞿颖', '沈星', '孙俪', '汤唯', '唐嫣', '佟丽娅', '徐静蕾',
         '许晴', '黄圣依', '王珞丹', '翟凌', '徐冬冬', '王子文', '赵薇',
         '章子怡', '周迅', '张静初', '袁泉', '张含韵', '张靓颖', '马思纯',
         '于娜', '叶一茜', '杨幂', '张雨绮', '张梓琳', '姚晨', '张馨予', '殷桃',
         '郑爽', '周冬雨', '姚笛', '赵丽颖', '张天爱', '艾薇儿',
         '奥黛丽赫本', '卡梅隆·迪亚兹', '泽塔琼斯', '克劳馥', '艾玛沃特森', '艾玛',
         '梅根福克斯', '艾米莉亚克拉克', '希尔顿', '安妮·海瑟薇', '丽芙·泰勒', '朱迪福斯特', '米兰达可儿',
         '梅格瑞恩', '妮可基德曼', '娜塔丽', '麦当娜', '布兰妮', '苏菲玛索',
         '克里斯汀·斯图尔特', '安吉丽娜朱莉', '李心洁', '戴佩妮']

# stars = ['孙允珠']

VERSION = '1.0'  # 版本号
# # star = '孙允珠'
# star = '倪妮'
# # star = '杨幂'
# # star = 'angelababy'
save_path = 'e:\download'  # 默认存放路径
INTERVAL = 0.5  # 下载一张图片间隔时间
INTERVAL1 = 0  # 访问原帖间隔时间

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
        day = '0'
        try:
            day = m.group(0)
        except Exception as e:
            print(e, ' -- Not find day')

        # print(day)
        return day, l_pic


    def save_all_pic(self, before_this_day, test):
        '''
        下载原题网页的所有图片（在指定日期前的）
        :param before_this_day: 制定日期
        :param test: test=True不下载，test=False下载
        :retuen: 下载数量
        '''
        count = 0
        day, l_pic = self.find_all_pic()
        if day > before_this_day:
            if not test:
                for l in l_pic:
                    self.save_a_pic(l)
                    # pass  # for debug
            print('Download %d pictures %s %s' % (len(l_pic), self.name, day))
            count += len(l_pic)
        else:
            print(self.name, day)
        return count

    def save_a_pic(self, pic_url):
        '''
        通过pic_url处理后，得到真正的图片地址，并下载
        :param pic_url:  从原帖取得的地址
        :return: 下载成功返回True
        '''
        save_file = pic_url.split('/')[-1]
        full_file = os.path.join(save_path, self.name + '_' + save_file)
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
    :retuen: 下载数量
    '''
    count = 0
    tba = TiebaAll(star)
    l_tid = tba.page_list()
    # print(l_tid)
    for l in l_tid:
        tb = TiebaPicPage(star, l)
        count += tb.save_all_pic(before_this_day, test)
    print('----------------------------------------')
    print(star, count, 'pictures\n')
    return count


def download_all_stars(stars, before_this_day, test):
    '''
    下载一个指定贴吧，在某一日期前所有的图片
    :param stars: 贴吧名表
    :param before_this_day: 指定的日期
    :param test: test为True，则不下载
    '''
    count = 0
    for l in stars:
        count += download(l, before_this_day, test)
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

    if len(opts) == 0:
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
            elif a == 'star':
                if len(args) != 4:
                    usage_err()
                else:
                    day = get_day(eval(args[0]), eval(args[1]), eval(args[2]))
                    download(args[0], day, test)
            else:
                usage_err()


# def main():
# download_all_stars(stars, '2017-01-04', True)
# # tb = TiebaPicPage(star, '4963013075')
# # l_pid = tb.find_all_pic()
# # print(len(l_pid), l_pid)


if __name__ == '__main__':
    main()

