# history:
# 2019/06/26  v1.0  initial
# 2019/07/04  v1.1  format to jpg automatically


import os
import msvcrt
import shutil
import glob
import cv2
import numpy as np

VERSION = '1.1'

PIC_PATH = r'.'
MOV_PATH = '4'
# TMP_FILE = 'tmp.png'

# df_pic = pd.DataFrame(columns=['name', 'md5'])


def wait_any_key():
    print('press any key to exit...')
    msvcrt.getch()


def is_jpg(file):
    f = open(file, 'rb')
    ret = (f.read(2) == b'\xff\xd8')
    f.close()
    return ret


def mov_wrong_file(file):
    target_dir = os.path.join(PIC_PATH, MOV_PATH)
    os.makedirs(target_dir, exist_ok=True)
    full_file_name = os.path.join(PIC_PATH, file)
    # print('%s ->　%s' % (full_file_name, target_dir))
    try:
        shutil.move(full_file_name, target_dir)
    except Exception as e:
        print(e)


def format_to_jpg(file):
    # img = cv2.imread(file)
    img = cv2.imdecode(np.fromfile(file, dtype=np.uint8), -1)
    jpg_file = os.path.splitext(file)[0]+'_tojpg.jpg'
    cv2.imwrite(jpg_file, img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
    print('%s -> %s' % (file, jpg_file))


def main():
    files = glob.glob(PIC_PATH + '\\*.jpg')
    for f in files:
        if not is_jpg(f):
            # print('%s [not jpg]' % f)
            format_to_jpg(f)
            mov_wrong_file(f)
        else:
            print(f)

    wait_any_key()


if __name__ == '__main__':
    main()
