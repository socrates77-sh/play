# check duplicated files in pic directory
# move duplitcated files to DUP_PATH
# need picinfo.csv first

# history:
# 2019/02/03  v1.0  initial


import os
import hashlib
import msvcrt
import shutil
import glob
import pandas as pd

VERSION = '1.0'

INFO_FILE = r'd:\temp\picinfo.csv'
WORK_DIR = r'.'
PIC_DIR = r'd:\pic'
DUP_PATH = '5'


def wait_any_key():
    print('press any key to exit...')
    msvcrt.getch()


 def read_df(csv_file):
    print('load data from csv file %s ...' % INFO_FILE)
    df_pic = pd.read_csv(csv_file)
    # print(pd_pic)
    return df_pic


def get_dup_files():
    df_pic = read_df(INFO_FILE)
    # df_test = get_files(PIC_PATH)
    print('search duplicated files ...')
    # df_dup = df_pic[df_pic.duplicated('md5', keep=False)]
    df_dup = df_pic[df_pic.duplicated('md5')]
    print(df_dup)
    return df_dup


def mov_dup_file(file):
    target_dir = os.path.join(WORK_DIR, DUP_PATH)
    os.makedirs(target_dir, exist_ok=True)
    full_file_name = os.path.join(PIC_DIR, file)
    print('%s ->　%s' % (full_file_name, target_dir))
    try:
        shutil.move(full_file_name, target_dir)
    except Exception as e:
        print(e)


def main():
    df_dup = get_dup_files()
    for file in df_dup['name']:
        mov_dup_file(file)

    wait_any_key()


if __name__ == '__main__':
    main()
