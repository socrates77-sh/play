'''
用于下载www.showwall.com的图片
'''
__author__ = 'socrates'

import re
import requests
import os
import sys
import time
import getopt
# from bs4 import BeautifulSoup

VERSION = '1.0'  # 版本号
save_path = 'e:\download'  # 默认存放路径
url_main = 'http://www.showwall.com'  # 主页网址
my_cookies = dict(
    __cfduid='d3d96b32a79d4f9f2828f2c556b6518521485350718',
    uid='141043-2919320843-0-2',
    sid='d5fbf9c678e53e58e66d',
    uname='%E5%AD%90%E7%BD%95%E8%A8%80%E5%88%A9%E4%B8%8E%E5%91%BD%E4%B8%8E%E4%BB%81',
    __utmt='1',
    __utma='19282554.1522409781.1485350848.1485350848.1485350848.1',
    __utmb='19282554.9.10.1485350848',
    __utmc='19282554',
    __utmz='19282554.1485350848.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)'
)

INTERVAL = 5  # 下载一张图片间隔时间
f_miss = 0

# 自动下载时默认选择的人物
intest_stars = ['ayum_hamasaki', 'amuro_namie', 'saki_aibu', 'gouriki_ayame', 'asahina_aya',
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
                'chiling_lin', 'amber_kwok', 'pace_ng', 'meng_jessey', 'selina_yam', 'evle_sill', 'jolin_choi',
                'shu_qi', 'hebe', 'cyndi_wong', 'joey_wong', 'rainie_yeung', 'zhang_ting', 'genie_zhuo', 's_h_e',
                'boa', 'chae_lim', 'han_chae_young', 'ha_ji_won', 'han_ga_in', 'han_ye_sle', 'kim_hee_sun',
                'jun_ji_hyun', 'lee_young_ae', 'jang_na_ra', 'lee_hyo_lee', 'kim_tae_hee', 'jessica', 'song_hye_kyo',
                'yoona', 'girls_generation', 'cao_ying', 'jane_chang', 'chen_hao', 'chen_hong', 'fan_bingbing',
                'dong_jie', 'dilraba_dilmurat', 'huang_yi', 'gao_yuanyuan', 'han_xue', 'hu_ke', 'huo_si_yan',
                'huang_siu_lei', 'kym_gin', 'gan_ting_ting', 'gulnazar', 'li_bingbing', 'jacqueline_lu',
                'chinchin_jiang', 'liu_tao', 'stephy_qi',
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
                'kristen_stewart', 'jolie_angelina', 'angelica_lee', 'penny_tai','scarlett_johansson']


class ShowwallStar():
    def __init__(self, name, last_id=0):
        '''
        :param name: 人物
        :param last_id: 最后已下载的id
        :return: None
        '''
        self.name = name
        self.last_id = last_id

    def page_text(self, page=1):
        '''
        抓取图片html页面
        :param page: 页码
        :return: 页面html的文本
        '''
        if page <= 1:
            url = url_main + '/wallpaper/' + self.name + '/'
        else:
            url = url_main + '/wallpaper/' + self.name + '/page/' + str(page) + '/'
        r = requests.get(url)
        r.encoding = 'utf-8'
        print('[Access] %s page %d ... (status:%d)' % (self.name, page, r.status_code))
        return r.text

    @staticmethod
    def full_name(html_text):
        '''
        从页面获取人物的全名
        :param html_text: 页面内容文本
        :return: 人物全名
        '''
        p = re.compile('<title>(.*?)【共收藏', re.S)
        result = re.search(p, html_text).group(1).strip()
        return result

    @staticmethod
    def pic_count(html_text):
        '''
        从页面获取图片总数
        :param html_text: 页面内容文本
        :return: 图片总数
        '''
        p = re.compile('【共收藏(.*?)張桌布圖】', re.S)
        result = re.search(p, html_text).group(1).strip()
        return eval(result)

    @staticmethod
    def id_one_page(html_text):
        '''
        获取一个页面的全部id
        :param html_text: 页面内容文本
        :return: 全部id列表
        '''
        p = re.compile('/shorten/(.*?)\.jpg', re.S)
        result = re.findall(p, html_text)
        return result

    def id_all(self):
        '''
        搜索所有页面，获取last_id之后所有的id
        :return: 所有符合id的list
        '''

        l_id_all = []
        t = self.page_text(1)
        count = self.pic_count(t)
        l_id_page = self.id_one_page(t)
        l_id_all += [x for x in l_id_page if eval(x) > self.last_id]
        if eval(l_id_page[-1]) <= self.last_id or int(count / 20) + 1 == 1:
            return l_id_all

        for i in range(2, int(count / 20) + 2):
            # print('page=%d' % i)
            t = self.page_text(i)
            l_id_page = self.id_one_page(t)
            l_id_all += [x for x in l_id_page if eval(x) > self.last_id]
            if eval(l_id_page[-1]) <= self.last_id or i == int(count / 20) + 1:
                return l_id_all

    @staticmethod
    def save_a_pic(name, id, g):
        '''
        下载并存储图片
        :param name: 人物名
        :param id: id
        :param g: 是否glance
        :return: 成功返回True，失败返回False
        '''
        url = 'http://img.showwall.com/download.php?id=' + str(id) + '&k=' + name + '&u=9999999999'
        save_file = name + '_' + str(id) + '.jpg'
        full_file = os.path.join(save_path, save_file)
        if g:
            print('[Save] %s' % save_file)
            return True
        else:
            try:
                res = requests.get(url, cookies=my_cookies, timeout=60)
                if res.status_code != 200:
                    print('status error')
                    return False
                sz = open(full_file, 'wb').write(res.content)
                if sz <= 0:
                    print('size 0')
                    return False
            except Exception as e:
                print(e)
                print('exception')
                return False
            # sz = open(full_file, 'wb').write(res.content)
            print('[Save] %s <%d bytes>' % (save_file, sz))
            time.sleep(INTERVAL)
            return True

    def save_all(self, id_all, g):
        '''
        下载所有id列表的图片
        :param id_all: 需下载的id列表
        :param g: 是否glance
        :return: None
        '''
        global f_miss
        l_missing = []
        for x in id_all:
            if not self.save_a_pic(self.name, x, g):
                l_missing.append((self.name, x))
                print(l_missing)
        if len(l_missing) > 0:
            for x in l_missing:
                print('save missing')
                f_miss.write(x[0] + ' ' + x[1] + '\n')


def save_log(last_id):
    '''
    将last_id存到log文件
    :param last_id: 最后已下载的id
    :return: None
    '''
    log_file = save_path + '\log\log.txt'
    with open(log_file, 'w+') as f:
        f.write(last_id)


def auto_mode(last_id, g):
    '''
    自动模式，遍历intest_stars，下载所有晚于last_id的图片
    :param last_id: 最后已下载的id
    :param g: 是否glance
    :return: None
    '''
    global f_miss
    missing_file = save_path + '\log\missing.txt'
    f_miss = open(missing_file, 'w+')
    count_pic = 0
    real_last = 0
    for star in intest_stars:
        sw = ShowwallStar(star, last_id)
        r1 = sw.id_all()
        sw.save_all(r1, g)
        count_pic += len(r1)
        if len(r1) > 0:
            if eval(r1[0]) > real_last:
                real_last = eval(r1[0])
    print('Download %d pictures' % count_pic)
    if not g and real_last > 0:
        save_log(str(real_last))
    f_miss.close()


def star_mode(name, last_id, g):
    '''
    下载一个人物所有晚于last_id的图片
    :param name: 指定的人物
    :param last_id: 最后已下载的id
    :param g: 是否glance
    :return: None
    '''
    global f_miss
    missing_file = save_path + '\log\missing.txt'
    f_miss = open(missing_file, 'w+')
    sw = ShowwallStar(name, last_id)
    r1 = sw.id_all()
    sw.save_all(r1, g)
    print('Download %d pictures' % len(r1))
    f_miss.close()


def file_mode(file_name, g):
    '''
    从文件获取要下载的图片信息，并下载
    :param file_name: 包含下载信息的文件
    :param g: 是否glance
    :return: None
    '''
    print(file_name)
    if not os.path.exists(file_name):
        print('ERROR: File %s not exist' % file_name)
    else:
        for line in open(file_name):
            l = line.split(sep=' ')
            ShowwallStar.save_a_pic(l[0], eval(l[1]), g)


def version():
    print('showwall.py %s' % VERSION)


def usage():
    print('showwall.py usage:')
    print('-h: print help message')
    print('-v: print version')
    print('-d: set mode')
    print('    auto - automatically download pictures')
    print('        argument: last_id')
    print('    one - download one picture')
    print('        argument: name id')
    print('    star - download picture of a star')
    print('        argument: name, last_id')
    print('    file - download pictures defined by a file')
    print('        argument: file_name')
    print('-t: set mode for try')
    print('        argument: same as -d, but not realy download')


def usage_err():
    print('ERROR: invalid option or argument')
    usage()
    sys.exit(1)


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
                glance = False
            else:
                glance = True
            if a == 'auto':
                if len(args) != 1:
                    usage_err()
                else:
                    auto_mode(eval(args[0]), glance)
            if a == 'one':
                if len(args) != 2:
                    usage_err()
                else:
                    ShowwallStar.save_a_pic(args[0], eval(args[1]), glance)
            if a == 'star':
                if len(args) != 2:
                    usage_err()
                else:
                    star_mode(args[0], eval(args[1]), glance)
            if a == 'file':
                if len(args) != 1:
                    usage_err()
                else:
                    file_mode(args[0], glance)
        else:
            usage()
            sys.exit(1)


if __name__ == '__main__':
    main()
