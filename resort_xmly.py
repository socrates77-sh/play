import glob
import os


def main():
    files = glob.glob('*.m4a')
    sorted_files = sorted(files, reverse=True)

    for i in range(len(sorted_files)):
        name = sorted_files[i]
        # name_without_index = name.split('-')[-1]
        name_without_index = name[4:]
        # print(name_without_index)
        new_name = '%03d-%s' % (i + 1, name_without_index)
        # print(new_name, name)
        os.rename(name, new_name)
        print('%s -> %s' % (name, new_name))

if __name__ == '__main__':
    main()
