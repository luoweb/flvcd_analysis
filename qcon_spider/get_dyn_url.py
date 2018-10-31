# -*- coding:utf-8 -*-
import sys
import codecs
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
import re 

url = sys.argv[1]
findword = r'presentation/.{1,5}'
pattern = re.compile(findword)
page_id = re.search(pattern,url.decode("utf8")).group(0).replace("presentation/","")
print url
print page_id
file_handle=open('2018_' + page_id + '.txt',mode='w')

driver = webdriver.Chrome()
driver.get(url)
page = driver.page_source

print page
file_handle.write(page.encode('utf-8'))
file_handle.close()
driver.quit()