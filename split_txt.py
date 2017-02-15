#!/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'zwr'

import os
import sys


def split_txt(filename, num):
    if not os.path.exists(filename):
        print('File %s not existed.' % filename)
        sys.exit(1)

    # abs_filename = os.path.abspath(filename)
    # dir_name = os.path.split(abs_filename)[0]
    prefix = os.path.splitext(filename)[0]
    ext = os.path.splitext(filename)[1]
    # print(dir_name, prefix, ext)

    l_lines = ''
    try:
        with open(filename, 'r') as f:
            l_lines = f.readlines()
    except Exception as e:
        print(e)

    unit = int(len(l_lines) / num) + 1
    print('Total Lines: ', len(l_lines))

    for i in range(0, num - 1):
        out_file = '%s%02d%s' % (prefix, i, ext)
        # print('[Save] ', out_file)
        print('[Save] %s (Line: %d - %d)' % (out_file, i * unit, i * unit + unit - 1))
        with open(out_file, 'w+') as f:
            for j in range(0, unit):
                f.write(l_lines[i * unit + j])
                # print(i * unit + j)
                # print('=' * 10)

    out_file = '%s%02d%s' % (prefix, num - 1, ext)
    print('[Save] %s (Line: %d - %d)' % (out_file, (num - 2) * unit + unit, len(l_lines) - 1))
    with open(out_file, 'w+') as f:
        for j in range((num - 2) * unit + unit, len(l_lines)):
            f.write(l_lines[j])


def main():
    argn = len(sys.argv)
    # print(argn)
    if argn == 3:
        filename, num = sys.argv[1:]
    else:
        print('Usage:')
        print('python split_txt.py filename num')
        sys.exit(-1)

    split_txt(filename, eval(num))
    # split_txt(r'e:\download\dcjk.txt', 7)


if __name__ == '__main__':
    main()