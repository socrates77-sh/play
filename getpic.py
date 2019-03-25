# move a picture file from pic directory

# history:
# 2019/03/25  v1.0  initial


import os
import sys
import msvcrt
import shutil


VERSION = '1.0'

PIC_PATH = r'd:\pic'
DST_PATH = r'.\1'


def wait_any_key():
    print('press any key to exit...')
    msvcrt.getch()


def input_file_name():
    print('input file name (without .jpg), q to quit:')
    input_line = sys.stdin.readline().strip()
    if input_line is 'q':
        return False
    file_name = input_line + '.jpg'
    full_file_name = os.path.join(PIC_PATH, file_name)
    if(not os.path.exists(full_file_name)):
        print('%s not found' % full_file_name)
    else:
        os.makedirs(DST_PATH, exist_ok=True)
        shutil.move(full_file_name, DST_PATH)
        print('%s -> %s' % (full_file_name, DST_PATH))
    return True


def main():
    while(input_file_name()):
        pass
    # wait_any_key()


if __name__ == '__main__':
    main()
