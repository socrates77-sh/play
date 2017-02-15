'''
处理《上杉谦信》电子书
'''
__author__ = 'zwr'

import os
import sys


def do_format(filename):
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
        with open(filename, 'r', encoding='utf-8') as f:
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
                if l.startswith('第'):
                    f.write('\n')
                    f.write(l)
                    print(l)
                elif len(l) > 1 and l[-1] == '\n':
                    f.write(l[:-1])
                else:
                    f.write(l)
            except Exception as e:
                print(e)

    print('[Save]', out_file)

def main():
    do_format(r'e:\download\ssqx.txt')


if __name__ == '__main__':
    main()