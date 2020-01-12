import os
import re

dirname = r'.'
out_file_name = '宋书.txt'

vol_n = 1


def search_index(path):
    all_index = []
    for (thisdir, subs, files) in os.walk(dirname):
        for f in files:
            if f.endswith('.htm') and f.startswith('sons'):
                all_index.append(os.path.join(thisdir, f))
    return all_index


def read_htm(file):
    with open(file, 'r', errors='ignore') as f:
        htm_txt = f.read()
    return htm_txt


def extract_txt(htm_txt):
    global vol_n
    p = re.compile('<title>(.*?)</title>', re.S)
    m = re.search(p, htm_txt)
    vol = m.group(1).strip()
    result = '第' + str(vol_n) + '卷  '
    # result = '第' + str(vol_n) + '卷  ' + vol + '  '
    vol_n = vol_n + 1

    p = re.compile(
        'face="黑体" size="5" color="#A60053"><span style="font-size: 18pt">(.*?)</span></font><p><font', re.S)
    m = re.search(p, htm_txt)
    vol1 = m.group(1).strip()
    result += vol1 + '  '

    p = re.compile(
        'style="font-size: 16pt"><font color="#CA00CA"><strong>(.*?)</strong></font></span><font', re.S)
    m = re.search(p, htm_txt)
    title = m.group(1).strip()
    # if title == '':
    #     p = re.compile(
    #         'style="font-size: 14pt"><font color="#0000A0">　　◎(.*?)</font><font color="#FFFFFF">', re.S)
    #     m = re.search(p, htm_txt)
    #     title = m.group(1).strip()
    result += title + '\n'
    # print(result)

    p = re.compile(
        'style="font-size: 14pt"><font color="#0000A0">(.*?)</font><font color="#FFFFFF">', re.S)
    m = re.findall(p, htm_txt)
    for line in m:
        line1 = line.replace(
            '</font></span><span class="body" style="font-size: 12pt"><font color="#FF80C0">', ' <<')
        line2 = line1.replace(
            '</font></span><span class="body" style="font-size: 14pt"><font color="#0000A0">', '>> ')
        result += '    ' + line2 + '\n'
        # result += line2 + '\n'

    result += '\n\n\n'
    return result


def main():
    l_all_txt = search_index(dirname)
    # print(len(l_all_txt), l_all_txt)

    # htm = read_htm(r'e:\temp\js\晋书\jinshu_035.htm')
    # print(extract_txt(htm))

    # for l in l_all_txt:
    #     htm = read_htm(l)
    #     print(extract_txt(htm), l)

    out_file = os.path.join(dirname, out_file_name)
    with open(out_file, 'w+') as f:
        for l in l_all_txt:
            htm = read_htm(l)
            f.write(extract_txt(htm))
            # extract_txt(htm)
            print('[Read]', l)


if __name__ == '__main__':
    main()
