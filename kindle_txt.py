import os
import sys

# -*- coding: utf-8 -*-

'''
处理上传到kindle的txt文件，防止encoding的问题
'''

org_file = r'E:\temp\js\晋书\晋书.txt'


def do_format(filename):
    if not os.path.exists(filename):
        print('File %s not existed.' % filename)
        sys.exit(1)

    # abs_filename = os.path.abspath(filename)
    # dir_name = os.path.split(abs_filename)[0]
    prefix = os.path.splitext(filename)[0]
    ext = os.path.splitext(filename)[1]
    print(filename)

    l_lines = ''
    try:
        with open(filename, 'r') as f:
        # with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
        # with open(filename, 'r', errors='ignore') as f:
            # l_lines = f.readlines()
            l_lines = f.readlines()
    except Exception as e:
        print(e)

    print(l_lines)
    # for l in l_lines:
    # print(l)

    out_file = '%s%d%s' % (prefix, 0, ext)

    with open(out_file, 'w+') as f:
        for l in l_lines:
            try:
                f.write(l)
            except Exception as e:
                print(e)

    print('[Save]', out_file)


def main():
    do_format(org_file)


if __name__ == '__main__':
    main()
