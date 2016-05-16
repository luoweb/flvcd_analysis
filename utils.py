# -*- coding:utf-8 -*-

import os
from urllib import request, parse, error
from bs4 import BeautifulSoup
from tqdm import tqdm


def url_size(url, faker = False, headers = {}):
    if faker:
        response = request.urlopen(request.Request(url, headers = fake_headers), None)
    elif headers:
        response = request.urlopen(request.Request(url, headers = headers), None)
    else:
        response = request.urlopen(url)

    size = response.headers['content-length']
    return int(size) if size!=None else float('inf')


def url_save(url, filepath, force=True, refer = None, is_part = False, faker = False, headers = {}):
    file_size = url_size(url, faker = faker, headers = headers)
    pbar = tqdm(total=file_size, unit='B', unit_scale=True)
    if os.path.exists(filepath):
        if not force and file_size == os.path.getsize(filepath):
            if not is_part:
                pbar.close()
                print('Skipping %s: file already exists' % tr(os.path.basename(filepath)))
            else:
                pbar.update(file_size)
            return
        else:
            if not is_part:
                pbar.close()
                print('Overwriting %s' % os.path.basename(filepath), '...')
    elif not os.path.exists(os.path.dirname(filepath)):
        os.mkdir(os.path.dirname(filepath))

    temp_filepath = filepath + '.download' if file_size!=float('inf') else filepath
    received = 0
    if not force:
        open_mode = 'ab'

        if os.path.exists(temp_filepath):
            received += os.path.getsize(temp_filepath)
            pbar.update_received(os.path.getsize(temp_filepath))
    else:
        open_mode = 'wb'

    if received < file_size:
        if faker:
            headers = fake_headers
        elif headers:
            headers = headers
        else:
            headers = {}
        if received:
            headers['Range'] = 'bytes=' + str(received) + '-'
        if refer:
            headers['Referer'] = refer

        response = request.urlopen(request.Request(url, headers = headers), None)
        try:
            range_start = int(response.headers['content-range'][6:].split('/')[0].split('-')[0])
            end_length = end = int(response.headers['content-range'][6:].split('/')[1])
            range_length = end_length - range_start
        except:
            content_length = response.headers['content-length']
            range_length = int(content_length) if content_length!=None else float('inf')

        if file_size != received + range_length:
            received = 0
            pbar.close = 0
            open_mode = 'wb'

        with open(temp_filepath, open_mode) as output:
            while True:
                buffer = response.read(1024 * 256)
                if not buffer:
                    if received == file_size: # Download finished
                        break
                    else: # Unexpected termination. Retry request
                        headers['Range'] = 'bytes=' + str(received) + '-'
                        response = request.urlopen(request.Request(url, headers = headers), None)
                output.write(buffer)
                received += len(buffer)
                pbar.update(len(buffer))

    assert received == os.path.getsize(temp_filepath), '%s == %s == %s' % (received, os.path.getsize(temp_filepath), temp_filepath)

    if os.access(filepath, os.W_OK):
        os.remove(filepath) # on Windows rename could fail if destination filepath exists
    os.rename(temp_filepath, filepath)
