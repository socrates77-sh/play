# history:
# 2019/03/29  v1.0  initial

import re
import requests
import os
import sys
import msvcrt
# from progressbar import *

VERSION = '1.0'

DIR = '图片'
SAVE_PATH = r'.'
PORT = '8000'


def print_version(version):
    print('=' * 70)
    print('%s version: %s' % (os.path.basename(__file__), VERSION))
    print('=' * 70)


def wait_any_key():
    print('\nPress any key to exit ...')
    msvcrt.getch()


def input_from_console(prompt):
    print(prompt)
    input_line = sys.stdin.readline().strip()
    return input_line


def find_all_files(url):
    try:
        r = requests.get(url)
    except Exception as e:
        print(e)
        sys.exit(1)

    p = re.compile('onclick="downfile\(\'(\S+)\',\'\'\);', re.S)
    return re.findall(p, r.text)


def save_a_file(down_url, filename):
    try:
        res = requests.get(down_url, timeout=60)
        if res.status_code != 200:
            return 0
    except Exception as e:
        print(e)
        return 0
    full_name = os.path.join(SAVE_PATH, filename)
    sz = open(full_name, 'wb').write(res.content)
    # print('[Save] %s <%d bytes>' % (full_name, sz))
    # sys.stdout.write('[Save] %s <%d bytes>' % (full_name, sz))
    # sys.stdout.flush()
    return sz


def save_all_files(url, files):
    # widgets = [Counter(), '/%d:' % len(files), Percentage(), ' ', Bar('='), ' ',
    #            Timer(), ' ', ETA()]
    # pbar = ProgressBar(widgets=widgets, maxval=len(files)).start()
    for i in range(len(files)):
        down_url = url + files[i]
        sz = save_a_file(down_url, files[i])
        print('[Save %d/%d] %s <%d bytes>' % (i, len(files), files[i], sz))
        # pbar.update(i)

    # pbar.finish()


def main():
    print_version(VERSION)
    # ip = input_from_console('input ip:')
    ip = '192.168.137.253'
    url = 'http://%s:%s/%s/' % (ip, PORT, DIR)
    all_files = find_all_files(url)
    save_all_files(url, all_files)
    # wait_any_key()


def dosomework():
    time.sleep(0.01)


if __name__ == '__main__':
    main()
