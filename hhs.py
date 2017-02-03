'''
处理《后汉书》电子书
'''

__author__ = 'socrates'

import os
import re

dirname = r'e:\temp\hhs'


def search_index(path):
    all_index = []
    for (thisdir, subs, files) in os.walk(dirname):
        for f in files:
            if f.endswith('.htm') and f.startswith('hhs'):
                all_index.append(os.path.join(thisdir, f))
    return all_index


def read_htm(file):
    with open(file, 'r', errors='ignore') as f:
        htm_txt = f.read()
    return htm_txt


def extract_txt(htm_txt):
    p = re.compile('face="黑体" size="5" color="#A60053"><span style="font-size: 18pt">(.*?)</span></font><p><font', re.S)
    m = re.search(p, htm_txt)
    vol = m.group(1).strip()
    result = vol + '\n'

    p = re.compile('style="font-size: 16pt"><font color="#CA00CA"><strong>(.*?)</strong></font></span><font', re.S)
    m = re.search(p, htm_txt)
    title = m.group(1).strip()
    result += title + '\n'

    p = re.compile('style="font-size: 14pt"><font color="#0000A0">(.*?)</font><font color="#FFFFFF">', re.S)
    m = re.findall(p, htm_txt)
    for line in m:
        result += '    ' + line + '\n'

    result += '\n\n\n'
    return result


def main():
    l_all_txt = search_index(dirname)
    # print(len(l_all_txt), l_all_txt)

    # htm = read_htm(r'e:\temp\hhs\hhsu_001.htm')
    # print(extract_txt(htm))

    # for l in l_all_txt:
    # htm = read_htm(l)
    #     print(extract_txt(htm), l)

    out_file = os.path.join(dirname, '后汉书.txt')
    with open(out_file, 'w+') as f:
        for l in l_all_txt:
            htm = read_htm(l)
            f.write(extract_txt(htm))
            print('[Read]', l)


if __name__ == '__main__':
    main()