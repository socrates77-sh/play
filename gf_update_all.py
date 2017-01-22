"""
整理GF工艺文件更新
Note:
    只适用于全套工艺文件下载后的整理
    可设置老版本目录old_version_dir和新版本目录new_version_dir
    过时的文件会被移到新版本目录的obsoleted目录下
    log文件存放在新版本目录下
"""

# -*- coding: utf-8 -*-

__author__ = 'socrates'

import os
import hashlib
import datetime
import shutil

old_version_dir = r'D:\work\工艺文件\GlobalFoundries\GF180\PDK'
new_version_dir = r'd:\temp\PDK_018MCU_V1.1_3.2_-_-180NM_3.3V_6V_MCU_PLATFORM20161216T131843'


def calc_sha1(filepath):
    """
    :param filepath: 含路径文件名
    :return: str，sha1sum值，16进制
    """
    with open(filepath, 'rb') as f:
        sha1obj = hashlib.sha1()
        sha1obj.update(f.read())
        sha1sum = sha1obj.hexdigest()
        # print(hash)
        return sha1sum


def main():
    old_files = os.listdir(old_version_dir)
    new_files = os.listdir(new_version_dir)
    for f in old_files:
        if not os.path.isfile(os.path.join(old_version_dir, f)):
            old_files.remove(f)
    for f in new_files:
        if not os.path.isfile(os.path.join(new_version_dir, f)):
            new_files.remove(f)

    log_file = os.path.join(new_version_dir, 'log.txt')
    obsoleted_dir = os.path.join(new_version_dir, 'obsoleted')

    # 根据文件名，从老版本目录查找同名文件same_files和新版本目录中没有的文件obsoleted_files
    same_files = []
    obsoleted_files = []
    for f in old_files:
        if f in new_files:
            same_files.append(f)
        else:
            obsoleted_files.append(f)

    # 检查sha1值，筛选出真正的same_files和obsoleted_files
    for f in same_files:
        sha1_old = calc_sha1(os.path.join(old_version_dir, f))
        sha1_new = calc_sha1(os.path.join(new_version_dir, f))
        if sha1_old != sha1_new:
            same_files.remove(f)
            obsoleted_files.append(f)

    # 从new_files中剔除same_files
    for f in new_files:
        if f in same_files:
            new_files.remove(f)

    # 输入log文件
    if not os.path.exists(obsoleted_dir):
        os.mkdir(obsoleted_dir)

    f = open(log_file, 'w+')
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S\n'), file=f)

    print('---------------------------------------------', file=f)
    print('Not update:', len(same_files), 'file(s)', file=f)
    print('\nNot update:', len(same_files), 'file(s)')
    print('---------------------------------------------', file=f)
    for l in same_files:
        print(l, calc_sha1(os.path.join(new_version_dir, l)), file=f)
        print('.', end='')

    print('\n---------------------------------------------', file=f)
    print('New:', len(new_files), 'file(s)', file=f)
    print('\nNew:', len(new_files), 'file(s)')
    print('---------------------------------------------', file=f)
    for l in new_files:
        print(l, calc_sha1(os.path.join(new_version_dir, l)), file=f)
        print('.', end='')

    # obsoleted file移到obsoleted目录
    print('\n---------------------------------------------', file=f)
    print('Obsoleted:', len(obsoleted_files), 'file(s)', file=f)
    print('\nObsoleted:', len(obsoleted_files), 'file(s)')
    print('---------------------------------------------', file=f)
    for l in obsoleted_files:
        print(l, calc_sha1(os.path.join(old_version_dir, l)), file=f)
        print('move', l, ' -> ', obsoleted_dir)
        shutil.move(os.path.join(old_version_dir, l), obsoleted_dir)

    f.close()


if __name__ == '__main__':
    main()