#!/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'zwr'

import os
import time
import xlutils
import xlrd
import xlwt

dirname = r'G:\temp\a'
all_member = ['曾晟', '李秀峰', '何用', '李殿英', '翁亚男', '杨颢飞', '张文荣']


def get_person_filename(person):
    return '数字组_员工周报_' + person + '.xlsx'


def get_person_filetime(filename):
    return time.strftime('%y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(filename)))


def get_person_sheet(filename):
    wb = xlrd.open_workbook(filename)
    return wb.sheet_names()[0]


def check_person_report():
    for p in all_member:
        filename = dirname + os.sep + get_person_filename(p)
        if os.path.exists(filename):
            print('[V] ', end='')
            print(get_person_filename(p).ljust(20),
                  get_person_filetime(filename),
                  get_person_sheet(filename))
        else:
            print('[X] ', end='')
            print(get_person_filename(p))


def main():
    print('Weekly Report')
    check_person_report()
    key = input('Choice Quit/Continue ... [q/enter]')
    if key == 'q' or key == 'Q':
        exit(1)
    print('ok')


if __name__ == '__main__':
    main()