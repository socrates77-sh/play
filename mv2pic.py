# history:
# 2018/09/01  v1.0  initial
# 2018/09/01  v1.1  press any key to exit


import os
import glob
import random
import shutil
from msvcrt import getch

VERSION = '1.1'
PIC_DIR = r'd:\pic'


def print_version(version):
    print('=' * 70)
    print('%s version: %s' % (os.path.basename(__file__), VERSION))
    print('=' * 70)


def count_file(dir):
    n_file_all = len(glob.glob(dir + '\\*'))
    n_file_jpg = len(glob.glob(dir + '\\*.jpg'))
    return n_file_all, n_file_jpg


def print_summary(na0, nj0, na1, nj1):
    print('-' * 70)
    print('Before Move')
    print('number of all files: %d' % na0)
    print('number of jpg files: %d\n' % nj0)
    print('After Move')
    print('number of all files: %d' % na1)
    print('number of jpg files: %d\n' % nj1)


def gen_random_name(dest_dir):
    while(1):
        rand_num = random.randint(0, 999999)
        rand_name = '%06d.jpg' % rand_num
        full_name = os.path.join(dest_dir, rand_name)
        # print(rand_name)
        if not os.path.exists(full_name):
            break
    return rand_name


def move_jpg_to_dest(dest_dir):
    jpg_files = glob.glob('*.jpg')
    for f in jpg_files:
        file_name = gen_random_name(dest_dir)
        dest_file = os.path.join(dest_dir, file_name)
        print('%s -> %s' % (f, dest_file))
        shutil.move(f, dest_file)

    print('\n%d file(s) moved\n' % len(jpg_files))


def main():
    print_version(VERSION)

    n_all_0, n_jpg_0 = count_file(PIC_DIR)
    move_jpg_to_dest(PIC_DIR)
    n_all_1, n_jpg_1 = count_file(PIC_DIR)
    print_summary(n_all_0, n_jpg_0, n_all_1, n_jpg_1)
    print('press any key to exit...')
    getch()


if __name__ == '__main__':
    main()
