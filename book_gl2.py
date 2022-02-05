import os
import re


ROOT_DIR = r'E:\useful\gl2'
INDEX_FILE = 'index.html'


# def search_index(dirname):
#     all_index = []
#     for (thisdir, subs, files) in os.walk(dirname):
#         for f in files:
#             # if f == 'index.txt':
#             # if f.endswith('.txt') and f != 'index.txt':
#             if f.endswith('.htm'):
#                 all_index.append(os.path.join(thisdir, f))
#     return all_index


# def read_first_line(file):
#     s = ''
#     with open(file, 'r', encoding='utf-8') as f:
#         try:
#             s = f.readline()
#         except Exception as e:
#             print(e)
#         finally:
#             return s


def clean_content(txt):
    txt1 = txt.replace('<BR>', ' \n')
    # txt1 = txt.replace(chr(0xa1), ' ')
    lines = txt1.split('\n')
    rt = ''
    for i in range(len(lines)-1):
        next_line = lines[i+1]
        if next_line.startswith(' '):
            rt = rt + lines[i] + '\n'
        else:
            rt = rt + lines[i]
    rt = rt + lines[-1]

    return rt


def clean_title(txt):
    rt = txt.replace('\u3000', ' ')
    rt = rt.replace('&nbsp;', ' ')
    return rt


def extract_txt(file):
    with open(file, 'r', errors='ignore') as f:
        htm_txt = f.read()

    # p = re.compile(
    #     # '<FONT style="FONT-SIZE: 12pt" COLOR="#FF6666" FACE="楷体_GB2312"><B>(.*?)</B></center></FONT>', re.S)
    #     '<head><title>黄金书屋---(.*?)</title></head>', re.S)
    # p = re.compile('<title>(.*?)</title>', re.S)
    # m = re.search(p, htm_txt)
    # title = m.group(1).strip() if m else ''
    title = ''
    p = re.compile(
        '<FONT style="FONT-SIZE: 16.5pt" COLOR="#FF6666" FACE="楷体_GB2312"><B>(.*?)</B></center></FONT>', re.S)
    m = re.search(p, htm_txt)
    if m:
        title = m.group(1).strip()

    p = re.compile(
        '<FONT style="FONT-SIZE: 16.5pt" COLOR="#FF6666" FACE="楷体_GB2312">(.*?)</FONT></B></center>', re.S)
    m = re.search(p, htm_txt)
    if m:
        title = m.group(1).strip()

    p = re.compile('<pre>(.*)</pre>', re.S)
    m = re.search(p, htm_txt)
    if m:
        content = m.group(1).strip()

    p = re.compile(
        '<hr color="#EE9B73" size="1" width="94%">(.*)<hr color="#EE9B73" size="1" width="94%">', re.S)
    m = re.search(p, htm_txt)
    if m:
        content = m.group(1).strip()

    p = re.compile(
        '<tr><td><pre><span class="text1">(.*)</td></tr></table>', re.S)
    m = re.search(p, htm_txt)
    if m:
        content = m.group(1).strip()

    if content:
        rt = title + 3*'\n' + clean_content(content)
        # rt = clean_content(content)

    else:
        rt = ''
    return rt


def get_books():
    all_books = []
    for (root, dirs, files) in os.walk(ROOT_DIR):
        for d in dirs:
            # print(os.path.join(root, d))
            all_books.append(d)
    return all_books

    # full_name_index = os.path.join(ROOT_DIR, INDEX_FILE)
    # with open(full_name_index, 'r', errors='ignore') as f:
    #     index_text = f.read()
    # p = re.compile('<td><a href="(.*?)".*?>(.*?)</a>', re.S)
    # result = re.findall(p, index_text)
    # return result


def is_single_file(book_file):
    rt = False if book_file.find('/') > 1 else True
    return rt


def save_file(title, txt):
    out_file = os.path.join(ROOT_DIR, title + '.txt')
    # print(out_file)
    with open(out_file, 'w+') as f:
        f.write(txt)
    print('(F) %s' % title)


def do_single_file(file_name):
    # full_name = os.path.join(ROOT_DIR, file)
    if not os.path.exists(file_name):
        print('File %s not found' % file_name)
        return ''

    txt = extract_txt(file_name)
    if txt == '':
        print('File %s format error' % file_name)
        return ''

    # save_file(title, txt)
    return 3*'\n' + txt


def get_files(dirname):
    all_index = []
    for (thisdir, subs, files) in os.walk(dirname):
        for f in files:
            if f.endswith('.htm'):
                all_index.append(os.path.join(thisdir, f))
    return all_index


def do_multi_file(b):
    full_path = os.path.join(ROOT_DIR, b)
    if not os.path.exists(full_path):
        print('File %s not found' % full_path)
        return ''

    files = get_files(full_path)
    if not files:
        print('File %s format error' % full_path)
        return ''
    # print(files, len(files))
    # print(len(files))

    whole_txt = ''
    for f in files:
        txt = do_single_file(f)
        if not txt == '':
            whole_txt += txt
        whole_txt += 3*'\n'

    #
    # for (f, title) in files:
    #     # clean_title = title.replace('\u3000', ' ')
    #     # clean_title = clean_title.replace('&nbsp;', ' ')
    #     # print(f, clean_title)
    #     full_name = os.path.join(full_path+r'\..', f)
    #     # print(full_name)
    #     # whole_txt += clean_title(title) + 3*'\n'
    #     txt = do_single_file(full_name, title)
    #     if not txt == '':
    #         whole_txt += txt
    #     whole_txt += 3*'\n'

    return whole_txt


def main():
    books = get_books()
    for b in books:
        txt = do_multi_file(b)
        if not txt == '':
            save_file(b, txt)

    # count = 0
    # for (file, title) in books:
    #     if is_single_file(file):
    #         # pass
    #         full_name = os.path.join(ROOT_DIR, file)
    #         txt = do_single_file(full_name, title)
    #         if not txt == '':
    #             save_file(title, txt)
    #             count += 1
    #     else:
    #         # pass
    #         # print(title)
    #         txt = do_multi_file(file, title)
    #         if not txt == '':
    #             save_file(title, txt)
    #             count += 1

    # print(70*'=')
    # print('got %d books' % count)

    # l_all_txt = search_index(dirname)

    # out_file = os.path.join(dirname, outname + '.txt')
    # with open(out_file, 'w+') as f:
    #     for l in l_all_txt:
    #         htm = read_htm(l)
    #         f.write(extract_txt(htm))
    #         print('[Read]', l)


if __name__ == '__main__':
    main()
