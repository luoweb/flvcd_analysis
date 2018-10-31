# -*- coding:utf-8 -*-
from lxml import etree
import urllib
import os
import requests


def getHtml(url):
    html = requests.get(url).content
    selector = etree.HTML(html)
    return selector


def getContent(htm, xpathStr):
    selector = htm
    content = selector.xpath(xpathStr)
    return content


def callbackfunc(a, b, c):
    '''''
    a:已经下载的数据块
    b:数据块的大小
    c:远程文件的大小
   '''
    per = 100.0 * a * b / c
    if per > 100:
        per = 100
    print('%.2f%%' % per)


def getPath(title, folder):
    fn = '%s' % title
    pa = os.path.dirname(__file__) + '/' + 'netease/'
    # check and create folder
    if not os.path.exists(pa):
        os.mkdir(pa)
    return pa + '/' + fn + '.flv'


def getFlv(cons, title, folder):
    fn = '%s' % title
    pa = os.path.dirname(__file__) + '/' + 'youku/' +  folder
    # check and create folder
    if not os.path.exists(pa):
        os.mkdir(pa)
    fl = pa + '/%s.flv' % fn
    r = requests.get(cons)
    with open(fl, "wb") as code:
        code.write(r.content)


# = = = = = = #
videourl = 'https://open.163.com/movie/2018/1/C/3/MD806VN3U_MD80773C3.html'
format = 'super'  # 'high'  'normal'  'super'

url = 'http://www.flvcd.com/parse.php?kw=' + \
    urllib.parse.quote(videourl) + '&format=' + format
print(url)
req = urllib.request.Request(url)
req.add_header('Referer', 'http://www.flvcd.com/')
req.add_header(
    'User-Agent', 'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0')
res = urllib.request.urlopen(req)

html = res.read()
# print html
selector = etree.HTML(html)

# get flv title /html/body/table/tbody/tr[4]/th/table[1]/tbody/tr/td/text()

xp_title = '//td[@class="mn STYLE4"]'
xp_title = '//td'

htm0 = getHtml(videourl)
content = selector.xpath('//td[@class="mn STYLE4"]/text()')
# cons=getContent(htm0,xp_title)

title = content[1].strip()
# title="hello"
print(title)

# get flv href
xp = '//*[@class="mn STYLE4"]//@href'
content = selector.xpath(xp)
print('%s' % len(content))

x = 0
for con in content:
    if 'http://mov.bn.netease.com/' in con:
        print(con)
        getFlv(con,  '%s' % x, title)
        # urllib.urlretrieve(con, getPath('%s' % x, title))# , callbackfunc)
        x += 1
