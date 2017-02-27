'''
处理《资治通鉴》电子书
'''


import os
import re

dirname = r'G:\temp\资治通鉴'


def search_index(path):
    all_index = []
    for (thisdir, subs, files) in os.walk(dirname):
        for f in files:
            if f.endswith('.htm') and f.startswith('zztj'):
                all_index.append(os.path.join(thisdir, f))
    return all_index


def read_htm(file):
    with open(file, 'r', errors='ignore') as f:
        htm_txt = f.read()
    return htm_txt


def extract_txt(htm_txt):
    p = re.compile('style="font-size: 28pt"><strong>(.*?)</strong></font> </span></small></font><p><font', re.S)
    m = re.search(p, htm_txt)
    vol = m.group(1).strip()
    result = vol + '\n'

    p = re.compile('color="#CA00CA"><span style="font-size: 16pt">【<strong>(.*?)】</span><em><small> </small></font><font', re.S)
    m = re.search(p, htm_txt)
    title = m.group(1).strip()
    result += title + '\n'

    p = re.compile('color="#C0C0C0"><span style="font-size: 16pt">(.*?)</span></font></em></strong></p>', re.S)
    m = re.search(p, htm_txt)
    description = m.group(1).strip()
    result += description + '\n\n'

    p = re.compile('face="宋体" size="4">(.*?)</font><font', re.S)
    m = re.findall(p, htm_txt)
    for line in m:
        result += '    ' + line + '\n'

    result += '\n\n\n'
    return result


def main():
    l_all_txt = search_index(dirname)
    # print(len(l_all_txt), l_all_txt)

    htm = read_htm(r'G:\temp\资治通鉴\zztj_001.htm')
    print(extract_txt(htm))

    # for l in l_all_txt:
    # htm = read_htm(l)
    #     print(extract_txt(htm), l)

    # out_file = os.path.join(dirname, '资治通鉴.txt')
    # with open(out_file, 'w+') as f:
    #     for l in l_all_txt:
    #         htm = read_htm(l)
    #         f.write(extract_txt(htm))
    #         print('[Read]', l)


if __name__ == '__main__':
    main()
