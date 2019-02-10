# scan PIC_PATH and save md5sum to picinfo.csv

# history:
# 2019/01/16  v1.0  initial
# 2019/02/10  v1.1  add file size


import os
import hashlib
import msvcrt
import pandas as pd

VERSION = '1.1'

# PIC_PATH = r'e:\temp\pic'
PIC_PATH = r'd:\pic'
SAVE_FILE = r'd:\temp\picinfo.csv'

# df_pic = pd.DataFrame(columns=['name', 'md5'])


def wait_any_key():
    print('press any key to exit...')
    msvcrt.getch()


def calc_md5(filepath):
    """
    :param filepath: 含路径文件名
    :return: str，md5sum值，16进制
    """
    with open(filepath, 'rb') as f:
        sha1obj = hashlib.md5()
        sha1obj.update(f.read())
        sha1sum = sha1obj.hexdigest()
        # print(hash)
        return sha1sum


def get_filesize(filepath):
    fsize = os.path.getsize(filepath)
    return fsize


def scan_pic_dir(dir):
    print('scanning whole pic directory ...')
    files = os.listdir(dir)
    # files = []
    # for l in os.listdir(dir):
    #     if os.path.isfile(os.path.join(dir, l)):
    #         files.append(l)
    md5_size = []
    for f in files:
        md5sum = calc_md5(os.path.join(PIC_PATH, f))
        fsize = get_filesize(os.path.join(PIC_PATH, f))
        print(f, fsize, md5sum)
        md5_size.append('%s_%d' % (md5sum, fsize))

    # df_pic['name'] = files
    # df_pic['md5'] = md5s
    df_pic = pd.DataFrame({'name': files, 'md5_size': md5_size})
    # df_pic = pd.DataFrame(md5s, index=files, columns=['md5'])

    print('write data to csv file %s ...' % SAVE_FILE)
    df_pic.to_csv(SAVE_FILE)
    # print(pd_pic)


def main():
    scan_pic_dir(PIC_PATH)

    wait_any_key()


if __name__ == '__main__':
    main()
