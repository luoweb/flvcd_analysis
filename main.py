# -*- coding:utf-8 -*-

import re
import os
import sys
import argparse
from urllib import request, parse, error
import requests
from bs4 import BeautifulSoup
from ffmpeg import (
        ffmpeg_concat_ts_to_mkv,
        ffmpeg_concat_mp4_to_mp4,
        ffmpeg_concat_av,
        ffmpeg_concat_flv_to_mp4,
)
from utils import url_size, url_save


headers = {'Host': 'www.flvcd.com'}
formats = ['super', 'high', 'low', 'normal']
code_reg = re.compile(r'charset=([A-Za-z]+)')
title_reg = re.compile(r'<meta name="title" context="([^"]+)|<title>([^<]+)</title>')
fmt_reg = re.compile('([^\.]+)$')
ffmpeg_method = {
        'ts': (ffmpeg_concat_ts_to_mkv, 'mkv'),
        'mp4': (ffmpeg_concat_mp4_to_mp4, 'mp4'),
        'av': (ffmpeg_concat_av, 'av'),
        'flv':(ffmpeg_concat_flv_to_mp4, 'mp4')
        }


def get_download_urls(url, fmt):
    params = {'format': fmt, 'kw': url}
    r = requests.get('http://www.flvcd.com/parse.php', params=params, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    try:
        table = soup.find_all('td', attrs={'class': 'mn STYLE4', 'align': 'left'})[1]
        parts = []
        for i in table.find_all('a'):
            parts.append(i['href'])
        return parts
    except IndexError:
        return []


def download_video(url, format='super'):
    r = requests.get(url)
    text = r.text
    code = code_reg.search(r.text).groups(0)[0]
    if code:
        text = r.content.decode(code)
    title_1, title_2 = title_reg.search(text).groups()
    title = title_1 or title_2
    for f in formats:
        parts = get_download_urls(url, f)
        if len(parts) > 0:
            break
    try:
        fmt = fmt_reg.search(parts[0]).group(1)
        files = []
        print('total {} parts'.format(len(parts)))
        for i, url in enumerate(parts):
            filename = './{}_{}.{}'.format(title, i, fmt)
            url_save(url,  filename)
            files.append(filename)
        ffmpeg_concat, to_fmt = ffmpeg_method[fmt]
        output = '{}.{}'.format(title, to_fmt)
        ffmpeg_concat(files, output)
        print(output)
        for f in files:
            os.remove(f)
    except AttributeError as e:
        print(e)


def main():
    parser = argparse.ArgumentParser(description='use flvcd to download video')
    parser.add_argument('--format', default='super', metavar='N', help='default is super, hige, low, normal')
    parser.add_argument('url', help='download url')
    args = parser.parse_args()
    download_video(args.url, args.format)

if __name__ == '__main__':
    main()
