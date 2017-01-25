#!/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'zwr'

import re
import requests

group_member = [
    ('曾晟', '李秀峰', '何用', '李殿英', '翁亚男', '杨颢飞'),
    ('罗鹏', '沈良', '王鹏', '徐学良'),
    ('孙建刚', '张洪杰', '项涤凡'),
    ('党朝', '李行高', '吴东方', '刘攀峰', '朱霈俊', '徐明明', '朱美娇', '吕亚磊', '商敬辉'),
    ('李霄', '顾春兰'),
]


class OaWorklog():
    def __init__(self):
        # self.url_login = 'http://192.168.1.228:7890/oa/j_acegi_security_check'
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
        l_id = []
        page_worklog = '/modules/worklog/worklog.do?method=list&t=0'
        data = dict(ec_i='ec', ec_crd='100', ec_p='1', ec_s_logDay='', ec_s_isremind='', ec_s_userXXname='',
                    ec_s_createDate='', ec_s_status='', ec_dp='1', ec_rd='100')
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
        l_one_log = []
        page_log = '/modules/worklog/worklog.do?method=edit&id=%s&t=0' % id
        r = self.s.post(self.url_oa + page_log, cookies=self.cookies)
        p = re.compile('<TBODY id="MainTable.*?/TBODY>', re.S)
        result = re.search(p, r.text).group(0).strip().splitlines()

        i = 0
        while i < len(result):
            if result[i].strip() == '<TD>':
                task = result[i + 1].strip()[:-5]
                time = result[i + 2].strip()[4:-5]
                percent = result[i + 3].strip()[4:-5]
                support = result[i + 4].strip()[4:-5]
                l_one_log.append((task, time, percent, support))
                i += 5
            else:
                i += 1
        return l_one_log

    def filter_log(self, all_id, bygroup=1, bydate=1):
        l_filtered_id = []

        for (idx, dx, px) in all_id:
            if 0 <= bygroup <= 4:
                if px in group_member[bygroup]:
                    l_filtered_id.append((idx, dx, px))
            else:
                l_filtered_id.append((idx, dx, px))
        return l_filtered_id


def main():
    wl = OaWorklog()
    wl.oa_login()
    all_id = wl.get_log_id(1)

    for (idx, datex, personx) in wl.filter_log(all_id, -1, 1):
        r = wl.get_one_log(idx)
        print(idx, datex, personx, r)


if __name__ == '__main__':
    main()