'''
处理《老舍全集》电子书
'''

# -*- coding: utf-8 -*-
__author__ = 'zwr'

import os
import re


dirname = r'e:\temp\b'


def search_index(path):
    all_index = []
    for (thisdir, subs, files) in os.walk(dirname):
        for f in files:
            # if f == 'index.txt':
            # if f.endswith('.txt') and f != 'index.txt':
            if f.endswith('.htm'):
                all_index.append(os.path.join(thisdir, f))
    return all_index


def read_first_line(file):
    s = ''
    with open(file, 'r', encoding='utf-8') as f:
        try:
            s = f.readline()
        except Exception as e:
            print(e)
        finally:
            return s


def read_htm(file):
    with open(file, 'r', errors='ignore') as f:
        htm_txt = f.read()

    return htm_txt


def extract_txt(htm_txt):
    p = re.compile('<META NAME="keywords" CONTENT="(.*?)">', re.S)
    m = re.search(p, htm_txt)
    title = m.group(1).strip()
    result = title + '\n'

    p = re.compile('<hr color="#EE9B73" size="1" width="94%">(.*?)<hr color="#EE9B73" size="1" width="94%">', re.S)
    m = re.search(p, htm_txt)
    txt = m.group(1).strip()
    l_lines = txt.split('<BR>')
    for l in l_lines:
        ln = l.strip()
        if ln.startswith('<font color', 0):
            p = re.compile('<font color="#993333">(.*?)</font>(.*)', re.S)
            m = re.search(p, ln)
            # result += 'ok' + ln + '\n'
            result += m.group(1) + m.group(2) + '\n'
            # result += m.group(2) + '\n'
        else:
            result += ln + '\n'

    result += '\n\n\n'
    return result


def main():
    l_all_txt = search_index(dirname)

    out_file = os.path.join(dirname, '老舍全集.txt')
    with open(out_file, 'w+') as f:
        for l in l_all_txt:
            htm = read_htm(l)
            f.write(extract_txt(htm))
            print('[Read]', l)


if __name__ == '__main__':
    main()