from scrapy.http import HtmlResponse

import spynner
import pyquery
import time
import BeautifulSoup
import chardet

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class DownloadWebkitMiddleware( object ):

    def fixCharset(s,to_charset='utf-8'):
        if s == None: 
            return ''
        else:
            try:
                s=str(s)
                charset=chardet.detect(s)['encoding']
                return s.decode(charset,'ignore').encode(to_charset)
            except TypeError:
                return ''

    def process_request( self, request, spider ):
        browser = spynner.Browser()
        browser.create_webview()
        browser.set_html_parser(pyquery.PyQuery)
        browser.load(request.url, 20)
        try:
            browser.wait_load(10)
        except:
            pass
        return HtmlResponse( request.url, body=str(self.fixCharset(browser.html)) )