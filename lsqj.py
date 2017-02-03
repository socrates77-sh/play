'''
处理《老舍全集》电子书
'''

__author__ = 'zwr'

import os
import sys

dirname = r'G:\temp\b'


def search_index(path):
    all_index = []
    for (thisdir, subs, files) in os.walk(dirname):
        for f in files:
            # if f == 'index.txt':
            if f.endswith('.txt'):
                all_index.append(os.path.join(thisdir, f))
    return all_index


def read_first_line(file):
    s=''
    with open(file, 'r') as f:
        try:
            s = f.readline()
        except Exception as e:
            print(e)
        finally:
            return s


def main():
    l = search_index(dirname)
    for x in l:
        print(x, read_first_line(x))
        # print(x)


if __name__ == '__main__':
    main()