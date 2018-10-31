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

def getPath(title, folder):
    fn = '%s' % title
    pa = os.path.dirname(__file__) + '/' + 'netease/'
    # check and create folder
    if not os.path.exists(pa):
        os.mkdir(pa)
    return pa + '/' + fn + '.flv'

def getLink(url):
    req = urllib.request.Request(url)
    # req.add_header('Referer', 'http://www.flvcd.com/')
    req.add_header(
        'User-Agent', 'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0')
    res = urllib.request.urlopen(req)
    res = urllib.request.urlopen(req)
    html = res.read()
    # print html
    selector = etree.HTML(html)
    xp_link = '//a[@target="_self"]//@href'
    link_list = selector.xpath(xp_link)
    return link_list

def getFlv(cons, title):

    pa = os.path.dirname(os.path.realpath(__file__)) + '/' + 'netease/'
    print("storage path:"+pa)
    # check and create folder
    if not os.path.exists(pa):
        os.mkdir(pa)
    fl = pa + '/'+title+'.flv'
    r = requests.get(cons)
    with open(fl, "wb") as code:
        code.write(r.content)

def getFlvInfo(flvurl):
    url = 'http://www.flvcd.com/parse.php?kw=' + \
        urllib.parse.quote(flvurl) + '&format=' + format
    print(url)
    req = urllib.request.Request(url)
    req.add_header('Referer', 'http://www.flvcd.com/')
    req.add_header(
        'User-Agent', 'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0')
    res = urllib.request.urlopen(req)

    html = res.read()
    # print html
    selector = etree.HTML(html)

    # get flv title 
    xp_title = '//td[@class="mn STYLE4"]/text()'
    content = selector.xpath(xp_title)
    title = content[1].strip()
    print("title:"+title)

    # get flv href
    xp = '//*[@class="mn STYLE4"]//@href'
    content = selector.xpath(xp)

    for con in content:
        if 'http://mov.bn.netease.com/' in con:
            print(con)
            getFlv(con, title)

# = = = = = = #
videourl = 'https://open.163.com/movie/2011/3/R/1/M8O9BOGDE_M8OEETAR1.html'
format = 'super'  # 'high'  'normal'  'super'

link_list=getLink(videourl)
#去重复
link_list = list(set(link_list))

for link in link_list:
    if '//open.163.com/' in link:
        print(link)
        getFlvInfo(link)