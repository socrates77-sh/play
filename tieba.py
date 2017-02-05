__author__ = 'socrates'

import re
import requests
import os
import time
import datetime
import sys
import getopt

stars = ['ayum_hamasaki', 'amuro_namie', 'saki_aibu', 'gouriki_ayame', 'asahina_aya',
         'norika_fujiwara', 'fujimoto_miki', 'maki_goto', 'reika_hashimoto', 'satomi_ishihara',
         'maki_horikita', 'kyoko_fukada', 'keiko_kitagaw', 'kuroki_meisa', 'kusumi_koharu',
         'kinoshita_ayumi', 'kiritani_mirei', 'aya_matsuura', 'sasaki_nozomi', 'takako_tokiwa',
         'aya_ueto', 'noriko_sakai', 'ai_takahashi', 'erika_sawajiri', 'mizuhara_kiko',
         'cecilia_cheung', 'charlene_choi', 'elle_choi', 'gillian_chung', 'kelly_chen',
         'athena_chu', 'cheung_maggie', 'kathy_chao', 'sharla_cheung', 'vivian_chow', 'coco_jiang',
         'monica_chan', 'cherie_chung', 'chrissie_chau', 'jessica_cambensy', 'iynn_hung', 'gigi_leung',
         'michelle_lee', 'rain_lee', 'tiffany_lee', 'bernice_liu', 'rosamund_kwan', 'gigi_lai',
         'carman_lee', 'isabella_leung', 'karen_mok', 'maggie_q', 'faye_wong', 'joey_yung', 'kristy_yeung',
         'cherrie_ying', 'anita_yuen', 'angela_yeung', 'stephy_tang', 'twins', 'alyssa_chia', 'vivian_chen',
         'angela_chang', 'ady_an', 'ella_chen', 'chang_chun_ning', 'joe_chen', 'ivy_chen', 'michelle_chan',
         'chou_tzu_yu', 'mavis_fan', 'vivian_hsu', 'yuki_hsu', 'barbie_hsu', 'tsui_hsu', 'patty_hou',
         'coco_lee', 'ruby_lin', 'karena_lam', 'kelly_lin', 'rene_liu', 'ariel_lam', 'janet_lee',
         'chiling_lin', 'hayden_kwok', 'pace_ng', 'meng_jessey', 'selina_yam', 'evle_sill', 'jolin_choi',
         'shu_qi', 'hebe', 'cyndi_wong', 'joey_wong', 'rainie_yeung', 'zhang_ting', 'genie_zhuo', 's_h_e',
         'boa', 'chae_lim', 'han_chae_young', 'ha_ji_won', 'han_ga_in', 'han_ye_sle', 'kim_hee_sun',
         'jun_ji_hyun', 'lee_young_ae', 'jang_na_ra', 'lee_hyo_lee', 'kim_tae_hee', 'jessica', 'song_hye_kyo',
         'yoona', 'girls_generation', 'cao_ying', 'jane_chang', 'chen_hao', 'chen_hong', 'fan_bingbing',
         'dong_jie', 'dilraba_dilmurat', 'huang_yi', 'gao_yuanyuan', 'han_xue', 'hu_ke', 'huo_si_yan',
         'huang_siu_lei', 'kym_gin', 'gan_ting_ting', 'gulnazar', 'li_bingbing', 'jacqueline_lu',
         'chinchin_jiang',
         'crystal_liu', 'li_xiao_ran', 'jin_qiao_qiao', 'liu_xuan', 'liu_zi', 'cecilia_liu', 'ada_liu',
         'sally_jing', 'jiang_yi_yan', 'li_qin', 'ju_jing_yi', 'lin_yun', 'ning_jing', 'ma_yi_li', 'mei_ting',
         'ni_ni', 'qu_ying', 'shum_sing', 'li_sun', 'tong_wei', 'tiffany_tong', 'tong_li_ya', 'jing_lei',
         'xu_qing', 'eva_wong', 'wang_luo_dan', 'xiao_zhai', 'xu_dong_dong', 'olivia_wang', 'vicki_zhao',
         'zhang_zi_yi', 'jue_zhou', 'zhang_jing_chu', 'yuan_quan', 'kristy_zhang', 'zhang_liang_yin',
         'yu_na', 'ye_yi_qian', 'yang_mi', 'kitty_zhang', 'zhang_zi_lin', 'yao_chen', 'viann_zhang', 'yin_tao',
         'zheng_shuang', 'zhou_dong_yu', 'yao_di', 'zhao_li_ying', 'crystal_zhang', 'lavigne_avril',
         'audrey_hepburn', 'diaz_cameron', 'catherine_zeta_jones', 'cindy_crawford', 'emma_watson',
         'megan_fox', 'clarke', 'paris_hilton', 'anne_hathaway', 'liv_tyler', 'jodie_foster', 'miranda_kerr',
         'meg_ryan', 'nicole_kidman', 'natalie_portman', 'madonna', 'spears_britney', 'sophie_marceau',
         'kristen_stewart', 'jolie_angelina', 'angelica_lee', 'penny_tai']

stars = ['孙允珠', '倪妮', '杨幂', 'angelababy', '古力娜扎', '范冰冰', '李冰冰', '张静初', '唐嫣', '董洁',
         '高圆圆', '迪丽热巴', '黄奕', '韩雪', '胡可', '金莎', '李小璐']
# stars = ['胡可']

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
            if a == 'star':
                if len(args) != 4:
                    usage_err()
                else:
                    day = get_day(eval(args[0]), eval(args[1]), eval(args[2]))
                    download(args[0], day, test)
            else:
                usage_err()
        else:
            usage_err()

# def main():
# download_all_stars(stars, '2017-01-04', True)
# # tb = TiebaPicPage(star, '4963013075')
# # l_pid = tb.find_all_pic()
# # print(len(l_pid), l_pid)


if __name__ == '__main__':
    main()

