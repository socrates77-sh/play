'''
处理《续资治通鉴》电子书
'''


import os
import re

dirname = r'e:\temp\续资治通鉴'


def search_index(path):
    all_index = []
    for (thisdir, subs, files) in os.walk(dirname):
        for f in files:
            if f.endswith('.htm') and f.startswith('xtj'):
                all_index.append(os.path.join(thisdir, f))
    return all_index


def read_htm(file):
    with open(file, 'r', errors='ignore') as f:
        htm_lines = f.readlines()
    return htm_lines


def proc_line(lines):
    txt = ''
    s_vol = 'style="font-size: 28pt"><strong>(.*?)</strong></font> </span></small></font><p><font'
    s_title = 'color="#CA00CA"><span style="font-size: 16pt">【<strong>(.*?)】</span><em><small> </small></font><font'
    s_discription = 'color="#C0C0C0"><span style="font-size: 16pt">(.*?)</span></font></em></strong></p>'
    s_king = 'color="#A60053"><span style="font-size: 18pt">(.*?)</span></font><font'
    s_year = 'face="仿宋_GB2312" size="4" color="#0080C0"><span style="font-size: 14pt"><strong>(.*?)</strong></span></font></p>'
    s_main = 'face="宋体" size="4">(.*?)</font><font'

    for l in lines:
        result = get_useful(l, s_vol)
        if len(result) > 0:
            txt += result + '\n'
        result = get_useful(l, s_title)
        if len(result) > 0:
            txt += result + '\n'
        result = get_useful(l, s_discription)
        if len(result) > 0:
            txt += result + '\n'
        result = get_useful(l, s_king)
        if len(result) > 0:
            txt += '\n' + result + '\n'
        result = get_useful(l, s_year)
        if len(result) > 0:
            txt += result + '\n'
        result = get_useful(l, s_main)
        if len(result) > 0:
            txt += '    ' + result + '\n'
    return txt


def get_useful(line, pattern):
    p = re.compile(pattern, re.S)
    m = re.search(p, line)
    if m is None:
        return ''
    else:
        return m.group(1).strip()


def main():
    l_all_txt = search_index(dirname)
    # print(len(l_all_txt), l_all_txt)

    # htm_lines = read_htm(r'e:\temp\资治通鉴\zztj_001.htm')
    # print(proc_line(htm_lines))
    # print(extract_txt(htm))

    # for l in l_all_txt:
    # htm = read_htm(l)
    #     print(extract_txt(htm), l)

    out_file = os.path.join(dirname, '续资治通鉴.txt')
    with open(out_file, 'w+') as f:
        for l in l_all_txt:
            htm_lines = read_htm(l)
            f.write(proc_line(htm_lines))
            f.write('\n' * 2)
            f.write('* ' * 15)
            f.write('\n' * 2)
            print('[Read]', l)


if __name__ == '__main__':
    main()
