#-*- coding:utf-8 -*-
import sys
from HTMLParser import HTMLParser
from bs4 import BeautifulSoup
from PyQt4.QtWebKit import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
class Render(QWebPage):
    def __init__(self,url):
        self.app = QApplication(sys.argv)
        QWebPage.__init__(self)
        self.loadFinished.connect(self._loadFinished)
        self.mainFrame().load(QUrl(url))
        self.app.exec_()
    def _loadFinished(self, result):
        self.frame = self.mainFrame()
        self.app.quit()

url = 'https://2018.qconshanghai.com//presentation/1278'
r = Render(url)
html = r.frame.toHtml()
html = html.toUtf8()
print(html)