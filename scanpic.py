# scan PIC_PATH and save md5sum to picinfo.csv

# history:
# 2019/01/16  v1.0  initial
# 2019/02/10  v1.1  add file size
# 2019/04/05  v2.0  modify picinfo.csv for difference


import os
import hashlib
import msvcrt
import pandas as pd

VERSION = '2.0'

# PIC_PATH = r'e:\temp\pic'
PIC_PATH = r'f:\pic'
SAVE_FILE = r'f:\temp\picinfo.csv'

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


# def scan_pic_dir(dir):
#     print('scanning whole pic directory ...')
#     files = os.listdir(dir)
#     # files = []
#     # for l in os.listdir(dir):
#     #     if os.path.isfile(os.path.join(dir, l)):
#     #         files.append(l)
#     md5_size = []
#     for f in files:
#         md5sum = calc_md5(os.path.join(PIC_PATH, f))
#         fsize = get_filesize(os.path.join(PIC_PATH, f))
#         print(f, fsize, md5sum)
#         md5_size.append('%s_%d' % (md5sum, fsize))

#     # df_pic['name'] = files
#     # df_pic['md5'] = md5s
#     df_pic = pd.DataFrame({'name': files, 'md5_size': md5_size})
#     # df_pic = pd.DataFrame(md5s, index=files, columns=['md5'])

#     print('write data to csv file %s ...' % SAVE_FILE)
#     df_pic.to_csv(SAVE_FILE)
#     # print(pd_pic)


def get_csv(info_file):
    if not os.path.exists(info_file):
        return pd.DataFrame(columns=['name', 'md5_size'])
    else:
        print('load data from csv file %s ...' % SAVE_FILE)
        df_csv = pd.read_csv(info_file, usecols=['name', 'md5_size'])
        return df_csv


def get_pic_files(dir):
    print('scanning whole pic directory ...')
    files = os.listdir(dir)
    df_pic = pd.DataFrame({'name': files})
    return df_pic


def fill_md5_by_file(df_files, dir):
    files = df_files['name'].tolist()
    md5_size = []
    for f in files:
        # print(f)
        md5sum = calc_md5(os.path.join(dir, f))
        fsize = get_filesize(os.path.join(dir, f))
        print(f, fsize, md5sum)
        md5_size.append('%s_%d' % (md5sum, fsize))

    # df_test = pd.DataFrame(md5s, index=files, columns=['md5'])
    df_test = pd.DataFrame({'name': files, 'md5_size': md5_size})
    return df_test


def save_csv(df_csv, info_file):
    print('write data to csv file %s ...' % SAVE_FILE)
    df_csv.to_csv(info_file)


def main():
    df_csv = get_csv(SAVE_FILE)
    df_pic_files = get_pic_files(PIC_PATH)

    df_same = pd.merge(df_pic_files, df_csv, on=['name'])

    # df = df_same.append(df_csv, sort=False)
    # df_deleted = df.drop_duplicates(subset=['name'], keep=False)

    df = df_same.append(df_pic_files, sort=False)
    df_new_files = df.drop_duplicates(subset=['name'], keep=False)

    df_new = fill_md5_by_file(df_new_files, PIC_PATH)

    df_updated_csv = pd.merge(df_same, df_new, how='outer')

    # print('csv', len(df_csv))
    # print('pic', len(df_pic_files))
    # print('same', len(df_same))
    # # print('deleted', len(df_deleted))
    # print('new', len(df_new))
    # print('updated', len(df_updated_csv))
    # print(df_updated_csv.columns)
    # print(df_updated_csv)

    save_csv(df_updated_csv, SAVE_FILE)
    wait_any_key()


if __name__ == '__main__':
    main()
