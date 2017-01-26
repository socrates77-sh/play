'''
用于从OA抓取工作日志，并存放到桌面worklog.xls文件
注意：worklog.xls文件需处于关闭状态，或不存在
命令行：
    python worklog.py [group [days]]
        group: 选取的组（0-数字；1-模拟；2-版图；3-SA；4-管理；其他-所有组；默认为所有组）
        days： 从最新日志回溯的天数，默认为1天（即只选取最新1天的日志）
'''

__author__ = 'zwr'

import xlwt
import os
import re
import requests
import datetime
import sys

# 版本号
VERSION = 1.0

# 组成员
group_member = [
    ('曾晟', '李秀峰', '何用', '李殿英', '翁亚男', '杨颢飞'),  # 数字
    ('罗鹏', '沈良', '王鹏', '徐学良'),  # 模拟
    ('孙建刚', '张洪杰', '项涤凡'),  # 版图
    ('党朝', '李行高', '吴东方', '刘攀峰', '朱霈俊', '徐明明', '朱美娇', '吕亚磊', '商敬辉'),  # SA
    ('李霄', '顾春兰')  # 管理
]

# 组名
group_name = ['数字组', '模拟组', '版图组', 'SA', '管理']

# 最多访问的日志页数
PAGE_LIMIT = 100


class OaWorklog():
    '''
    OaWorklog处理登录、页面抓取等
    '''

    def __init__(self):
        self.url_oa = 'http://192.168.1.228:7890/oa'

        self.cookies = {
            'JSESSIONID': 'C98E5B8C9E87CA2F049D1B5B3123C310',
            'userClose': '0'
        }
        self.s = requests.session()
        self.s.verify = False
        self.s.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36'
        }

    def oa_login(self):
        '''
        登录OA
        :return: 登录后首页内容
        '''
        page_login = '/j_acegi_security_check'
        data = {
            'j_mode': 'static',
            'j_locale': 'zh_CN',
            'j_username': 'zwr',
            'j_password': 'c3lzdGVtT0EsendyNzcwMjA3',
            'Submit3': '登 录'
        }
        return self.s.post(self.url_oa + page_login, data=data, cookies=self.cookies)

    def get_log_id(self, page=1):
        '''
        取得指定页每一日志条目的ID、日期、人员
        :param page: 指定页码，默认为1
        :return: list，成员为ID、日期、人员组成的tuple
        '''
        l_id = []
        page_worklog = '/modules/worklog/worklog.do?method=list&t=0'
        data = dict(ec_i='ec', ec_crd='100', ec_p='1', ec_s_logDay='', ec_s_isremind='', ec_s_userXXname='',
                    ec_s_createDate='', ec_s_status='', ec_dp='1', ec_rd='100')
        # 以下两个data值设置页码
        data['ec_p'] = page
        data['et_dp'] = page
        r = self.s.post(self.url_oa + page_worklog, data=data, cookies=self.cookies)
        # soup = BeautifulSoup(r.content, 'html.parser', from_encoding='gb18030')
        pattern = re.compile('<a href="javascript:ec\.action.*?/a>', re.S)
        result = re.findall(pattern, r.text)
        # print(len(result))
        for x in result:
            # print(x)
            p = re.compile('id=(\d*)', re.S)
            id = re.search(p, x).group(1).strip()
            # print(id)
            # p = re.compile('>\r\n(.*)\r\n.*<', re.S)
            p = re.compile('(\d*-\d*-\d*)--(.*)--.*\r\n', re.S)
            r1 = re.search(p, x)
            date, person = r1.group(1).strip(), r1.group(2).strip()
            # print(log)
            l_id.append((id, date, person))
        # print(dict_id)
        # print(len(dict_id))
        return l_id

    def get_one_log(self, id):
        '''
        根据ID号抓取日志的详细信息
        :param id: 指定的ID号
        :return: list，成员一条日志所有的task等组成的tuple
        '''
        l_one_log = []
        page_log = '/modules/worklog/worklog.do?method=edit&id=%s&t=0' % id
        r = self.s.post(self.url_oa + page_log, cookies=self.cookies)
        p = re.compile('<TBODY id="MainTable.*?/TBODY>', re.S)
        result = re.search(p, r.text).group(0).strip().splitlines()

        i = 0
        while i < len(result):
            if result[i].strip() == '<TD>':
                # task可能有多行
                task = ''
                while not result[i + 1].endswith('</TD>'):
                    task += result[i + 1].strip() + '\n'
                    i += 1
                task += result[i + 1].strip()[:-5]
                time = result[i + 2].strip()[4:-5]
                percent = result[i + 3].strip()[4:-5]
                support = result[i + 4].strip()[4:-5]
                l_one_log.append((task, time, percent, support))
                i += 5
            else:
                i += 1
        return l_one_log

    def debug_a_log(self, id):
        '''
        调试函数，根据ID号抓取日志的页面
        :param id: 指定的ID号
        :return: 用于调试
        '''
        page_log = '/modules/worklog/worklog.do?method=edit&id=%s&t=0' % id
        r = self.s.post(self.url_oa + page_log, cookies=self.cookies)
        p = re.compile('<TBODY id="MainTable.*?/TBODY>', re.S)
        result = re.search(p, r.text).group(0).strip().splitlines()
        # print(re.search(p, r.text).group(0).strip())

        i = 0
        while i < len(result):
            if result[i].strip() == '<TD>':
                task = ''
                while not result[i + 1].endswith('</TD>'):
                    task += result[i + 1].strip() + '\n'
                    i += 1
                task += result[i + 1].strip()[:-5]
                time = result[i + 2].strip()[4:-5]
                percent = result[i + 3].strip()[4:-5]
                support = result[i + 4].strip()[4:-5]
                print(task, time, percent, support)
                print(task)
                # print(result)
                i += 5
            else:
                i += 1

        return r


    def get_useful_log(self, last_date):
        '''
        根据指定的最早日期，抓取足够的页面，直到早于指定日期
        :param last_date: string，最早日期
        :return: list，所有抓到的日志条目ID等
        '''
        all_id = self.get_log_id(1)
        for i in range(2, PAGE_LIMIT):
            first, last = get_date_boundry(all_id)
            # print(last)
            # print(type(last))
            # print(len(all_id))
            if last < last_date:
                break
            else:
                all_id += self.get_log_id(i)
        return all_id


class XlWrite():
    '''
    用于XLS文件输出
    '''

    def __init__(self):
        self.f = xlwt.Workbook()
        self.sheet1 = self.f.add_sheet('worklog', cell_overwrite_ok=True)
        self.line = 1

    def print_title(self):
        '''
        打印表格的标题行，并设置每列宽度
        :return: None
        '''
        title = ['日期', '组别', '人员', '工作内容', '工时', '进度(%)', '配合人员']
        for i in range(0, len(title)):
            self.sheet1.write(0, i, title[i], xlwt.easyxf('font: bold on'))
            self.sheet1.col(i).width = 3000
        self.sheet1.col(3).width = 15000

    def print_log(self, an_id, a_group, a_log):
        '''
        打印一条日志的全部内容
        :param an_id: 日志ID等
        :param a_group: 成员所属组别
        :param a_log: 日志详情
        :return: None
        '''

        # 打印日期、组别、成员
        self.sheet1.write(self.line, 0, an_id[1], xlwt.easyxf('align: wrap on, horiz left, vert center'))
        self.sheet1.write(self.line, 1, a_group, xlwt.easyxf('align: wrap on, horiz left, vert center'))
        self.sheet1.write(self.line, 2, an_id[2], xlwt.easyxf('align: wrap on, horiz left, vert center'))

        # 打印一条日志所有的任务
        for i in range(len(a_log)):
            self.sheet1.write(self.line, 3, a_log[i][0], xlwt.easyxf('align: wrap on, horiz left, vert center'))
            self.sheet1.write(self.line, 4, a_log[i][1], xlwt.easyxf('align: wrap on, horiz left, vert center'))
            self.sheet1.write(self.line, 5, a_log[i][2], xlwt.easyxf('align: wrap on, horiz left, vert center'))
            self.sheet1.write(self.line, 6, a_log[i][3], xlwt.easyxf('align: wrap on, horiz left, vert center'))
            self.line += 1

    def save_xl(self):
        '''
        保存xls文件
        :return: None
        '''

        # 获取desk目录名
        desk_path = os.path.join(os.path.expanduser("~"), 'Desktop')
        xl_file = os.path.join(desk_path, 'worklog.xls')

        # 如xls未关闭，则会报错
        try:
            self.f.save(xl_file)
            print('==========================================================================')
            print('[worklog v%s] Save to %s' % (VERSION, xl_file))
            print('==========================================================================')
        except PermissionError:
            print('==========================================================================')
            print('[worklog v%s] ERROR: %s is opened now' % (VERSION, xl_file))
            print('==========================================================================')
            exit(1)


def filter_by_group(all_id, bygroup=0):
    '''
    根据组别筛选ID，组的定义见group_name
    :param all_id: 被筛选的列表
    :param bygroup: 需要选取的组号
    :return: 返回筛选成功的列表
    '''
    l_filtered_id = []

    for (idx, dx, px) in all_id:
        # 超出0-4的，则全选
        if 0 <= bygroup <= 4:
            if px in group_member[bygroup]:
                l_filtered_id.append((idx, dx, px))
        else:
            l_filtered_id.append((idx, dx, px))
    return l_filtered_id


def filter_by_date(all_id, bydate):
    '''
    根据输入的日期，早于该日期的ID均被滤除
    :param all_id: 被筛选的列表
    :param bydate: string, 限定的日期
    :return: 返回筛选成功的列表
    '''
    l_filtered_id = []
    for (idx, dx, px) in all_id:
        if dx >= bydate:
            l_filtered_id.append((idx, dx, px))
    return l_filtered_id


def get_date_boundry(all_id):
    '''
    获取一个ID列表的最早和最晚日期
    :param all_id: 输入的列表
    :return: 返回最晚、最早的日期
    '''
    first = all_id[0][1]
    last = first
    for i in range(0, len(all_id)):
        if all_id[i][1] > first:
            first = all_id[i][1]
        if all_id[i][1] < last:
            last = all_id[i][1]
    return first, last


def get_valid_last_date(days_from_latest):
    '''
    获取有效日期
    :param days_from_latest: 从最晚日期回溯的间隔天数
    :return: 返回最早的有效日期
    '''
    if days_from_latest < 1:
        days_from_latest = 1
    wl = OaWorklog()
    wl.oa_login()
    try_id = wl.get_log_id(1)
    first, last = get_date_boundry(try_id)
    y, m, d = first.split('-')
    if m[0] == '0':
        m = m[-1:]
    if d[0] == '0':
        d = d[-1:]

    d0 = datetime.date(eval(y), eval(m), eval(d))
    d1 = d0 - datetime.timedelta(days_from_latest - 1)
    # print(d0, d1)
    return d1.isoformat()


def get_group(an_id):
    '''
    获取一个ID所属的组
    :param an_id: 输入的ID
    :return: 组名
    '''
    for i in range(0, len(group_name)):
        if an_id[2] in group_member[i]:
            return group_name[i]
    return '其他'


def getargs():
    argn = len(sys.argv)
    if argn == 3:
        day_count, group = sys.argv[1:]
    elif argn == 2:
        day_count = sys.argv[1]
        group = '-1'
    elif argn == 1:
        day_count = '1'
        group = '-1'
    else:
        print('Usage:')
        print('python worklog.py [group [days]]')
        print('group: 选取组（0-数字；1-模拟；2-版图；3-SA；4-管理；其他-所有组；默认为所有组）')
        print('days： 从最新日志回溯的天数，默认为1天（即只选取最新1天的日志）')
        sys.exit(-1)
    return day_count, group


def main():
    # 分析命令行参数
    d, g = getargs()
    group_select = eval(g)
    days_from_latest = eval(d)

    # 抓取网页
    wl = OaWorklog()
    wl.oa_login()
    d1 = get_valid_last_date(days_from_latest)
    all_id = wl.get_useful_log(d1)
    all_by_g = filter_by_group(all_id, group_select)
    all_by_gd = filter_by_date(all_by_g, d1)

    # XLS输出、保存
    xl = XlWrite()
    xl.print_title()
    for x in all_by_gd:
        log = wl.get_one_log(x[0])
        xl.print_log(x, get_group(x), log)
        print(x, get_group(x), log)
    xl.save_xl()

    # for DEBUG
    # r1 = wl.debug_a_log('27620').text
    # print(r1)


if __name__ == '__main__':
    main()