# compare md5sum of picture files in current directory from in pic directory
# move duplitcated files to DUP_PATH
# need picinfo.csv first

# history:
# 2019/01/16  v1.0  initial
# 2019/01/18  v1.1  check pic file only


import os
import hashlib
import msvcrt
import shutil
import glob
import pandas as pd

VERSION = '1.0'

INFO_FILE = r'd:\temp\picinfo.csv'
PIC_PATH = r'.'
DUP_PATH = '3'

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


def read_df(csv_file):
    print('load data from csv file %s ...' % INFO_FILE)
    df_pic = pd.read_csv(csv_file)
    # print(pd_pic)
    return df_pic


def get_files(dir):
    files = glob.glob(dir + '\\*.jpg')
    # files = []
    # for l in os.listdir(dir):
    #     if os.path.isfile(os.path.join(dir, l)):
    #         files.append(l)
    md5s = []
    for f in files:
        # print(f)
        md5sum = calc_md5(os.path.join(PIC_PATH, f))
        print(f, md5sum)
        md5s.append(calc_md5(os.path.join(PIC_PATH, f)))

    # df_test = pd.DataFrame(md5s, index=files, columns=['md5'])
    df_test = pd.DataFrame({'name1': files, 'md5': md5s})
    return df_test


def get_dup_files():
    df_pic = read_df(INFO_FILE)
    df_test = get_files(PIC_PATH)
    print('search duplicated files ...')
    return pd.merge(df_pic, df_test, on=['md5'])


def mov_dup_file(file):
    target_dir = os.path.join(PIC_PATH, DUP_PATH)
    os.makedirs(target_dir, exist_ok=True)
    full_file_name = os.path.join(PIC_PATH, file)
    print('%s ->　%s' % (full_file_name, target_dir))
    try:
        shutil.move(full_file_name, target_dir)
    except Exception as e:
        print(e)


def main():
    df_dup = get_dup_files()
    for file in df_dup['name1']:
        mov_dup_file(file)

    wait_any_key()


if __name__ == '__main__':
    main()
