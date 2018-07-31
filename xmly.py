# history:
# 2018/07/01  v1.0  initial
# 2018/07/02  v1.1  skip existed file when download
# 2018/07/31  v1.2  delete invalid char of file name


import re
import requests
import json
import sys
import io
import os

VERSION = '1.2'

INVALID_CHAR_OF_FILENAME = ['.', '?']

URL_TRACK = 'http://www.ximalaya.com/revision/play/tracks?trackIds='
# m4a_url = 'http://audio.xmcdn.com/group36/M03/14/33/wKgJTVs1ra7CRKMTAISxdTec9wM851.m4a'
# album_url = 'http://www.ximalaya.com/lishi/3703879/p3/'
# album_url = 'http://www.ximalaya.com/shangye/269179/'


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
}

ERR_WEB_ACCESS_FAIL = 'Cannot access web'
ERR_WEB_EXTRACT_FAIL = 'Cannot extract web'


def print_version(version):
    print('=' * 70)
    print('%s version: %s' % (os.path.basename(__file__), VERSION))
    print('=' * 70)


def usage():
    print('usage:')
    print('    %s xmly_album_url' % os.path.basename(__file__))


def remove_duplicate(input_list):
    return list(set(input_list))


class XmldAlbum():

    def __init__(self, album_url):
        self.__track_list = []
        self.__count_of_tracks = 0
        self.__extract_tracks(album_url)

    @property
    def count_of_tracks(self):
        return self.__count_of_tracks

    @property
    def track_list(self):
        return self.__track_list

    def __extract_tracks(self, album_url):
        res = requests.get(album_url, headers=HEADERS)
        if res.status_code == 200:
            html_text = res.text
            p = re.compile(
                '{"index":(\d+?),"trackId":(\d+?),"isPaid":false,"tag":0,"title":"(.+?)","playCount"', re.S)
            result = re.findall(p, html_text)
            if(result != []):
                self.__track_list = remove_duplicate(result)
                self.__count_of_tracks = len(self.track_list)
                return True
            else:
                print('Error: %s %s' % (ERR_WEB_EXTRACT_FAIL, album_url))
                return False
        else:
            print('Error: %s %s' % (ERR_WEB_ACCESS_FAIL, album_url))
            return False


def save_m4a(url, file_name):
    res = requests.get(url, timeout=60)
    size_of_file = open(file_name, 'wb').write(res.content)
    print('[save] %s (%d bytes)' % (file_name, size_of_file))


def delete_invalid_char(name):
    clean_name = name
    for invalid_char in INVALID_CHAR_OF_FILENAME:
        clean_name = clean_name.replace(invalid_char, '')
    return clean_name


def download_track(track):
    index = track[0]
    track_id = track[1]
    title = track[2].strip()

    url = URL_TRACK + track_id
    res = requests.get(url, headers=HEADERS)

    if res.status_code == 200:
        try:
            response_json = res.json()
            m4a_url = response_json['data']['tracksForAudioPlay'][0]['src']
            # print(m4a_url)
        except Exception as e:
            print('Error: %s %s' % (ERR_WEB_EXTRACT_FAIL, url))
            return False
        clean_title = delete_invalid_char(title)
        file_name = '%03d-%s.m4a' % (int(index), clean_title)

        if os.path.exists(file_name):
            return False
        else:
            save_m4a(m4a_url, file_name)
            # print(file_name)
            return True

    else:
        print('Error: %s %s' % (ERR_WEB_ACCESS_FAIL, url))
        return False


def main():
    # sys.stdout = io.TextIOWrapper(sys.stdout, encoding='gb18030')
    sys.stdout = io.TextIOWrapper(
        sys.stdout.buffer, encoding='gb18030', line_buffering=True)

    print_version(VERSION)
    if len(sys.argv) != 2:
        usage()
        sys.exit(1)

    album_url = sys.argv[1]
    album = XmldAlbum(album_url)

    count_of_download = 0
    for track in album.track_list:
        # print(track)
        if download_track(track):
            count_of_download += 1

    print('=' * 70)
    print('%d files saved' % count_of_download)


if __name__ == '__main__':
    main()
