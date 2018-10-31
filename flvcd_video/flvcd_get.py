# -*- coding:utf-8 -*-

import re
import sys
import urllib
# import urllib2
import datetime
# from win32clipboard import *
# from win32con import CF_TEXT
import flvcd_client


def get_Clipboard():
        #  OpenClipboard()
        #  text = GetClipboardData(CF_TEXT)
    text = "https://open.163.com/movie/2018/1/C/3/MD806VN3U_MD80773C3.html"
    #  CloseClipboard()
    return text


class CFlvcd(object):
    def __init__(self):
        self.url = ""
        self.pattern = re.compile(
            r"<a *target=\"_self\" *href *= *\"(https://open\.163\.com/movie/2018/*\.html)\">")
        self.headers = {
            # "Accept": "*/*", "Accept-Language": "zh-CN", "": "",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
            # "Accept-Encoding":"gzip, deflate",
            "Content-Encoding": "gzip"
            # "Connection": "Keep-Alive"
        }

    def parse(self, url):
        self.url = "http://www.flvcd.com/parse.php?kw=" + url + "&format=super"
        print("self.url:"+self.url)
        # print("self.headers:"+self.headers)
        req = urllib.request.Request(url=self.url, headers=self.headers)
        res = urllib.request.urlopen(req)
        data = res.read()
        re_res = self.pattern.findall(data)
        # print("re_res:")
        if re_res != None:
            filename = datetime.datetime.now().strftime("%Y%m%d-%H%M%S.lst")
            fhandle = open(filename, "w")
            for url in re_res:
                # 注意是\r\n还是\n
                fhandle.write(url + "\r\n")
            fhandle.close()
            print("Parse URL Done!")
        else:
            print("URL Not Found")


def main():
    flvcd = CFlvcd()
    print("你要下载的视频地址是:")
    print(get_Clipboard())
    print("确定获取请按1")
    a = input()
    if (a == '1'):
        # flvcd_client = flvcd_client()
        flvcd.parse(get_Clipboard())


if __name__ == "__main__":
    main()
