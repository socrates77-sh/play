import shutil
import os


def move_files(from1, to, prefix):
    files = os.listdir(from1)
    for f in files:
        src = os.path.join(from1, f)
        dst = os.path.join('..', prefix + '_' + f)
        print('%s -> %s' % (src, dst))
        shutil.move(src, dst)


def main():
    dirs = []
    for l in os.listdir('.'):
        if os.path.isdir(l):
            dirs.append(l)

    for i in range(len(dirs)):
        move_files(dirs[i], '.', str(i + 1))


if __name__ == '__main__':
    main()
