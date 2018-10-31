#encoding:UTF-8
import sys
import urllib
import urllib3.request
# data是一个字典，然后通过urllib.parse.urlencode()将data转换为'wd = 904727147'的字符串
#最后和url合并为full_url
# urllib.request是一个库,隶属urllib,urllib是一个收集了很多处理url的包，开放网址的可扩展库。
# urllib.request模版定义了很多功能函数和类，这些类和函数帮助以文档的形式打开urls
# requests package被公认为是更高级别的HTTP客户端界面
# urllib.request定义了如下的函数功能：
# urllib.reuqest.urlopen(url,data=None,[timeout,]*,cafile = None,cadefault = False,context = None)
# 打开网址，它可以是一个字符串或一个请求对象。参数data必须是一个字节对象，
#发送给服务器的附加数据，如果不需要附加数据，这个参数也可以是空的。这个data也可以一个迭代对象，
#内容长度值必须在头文件中指定。目前http请求是唯一需要使用数据data的。当data参数被提供的时候，http请求将会是一个post而不是get型请求。
# 对于http和https地址，这个函数返回一个 http.client.HTTPResponse对象，
#这个对象有 HTTPResponse Objects 方法
# HTTPResponse.read([amt])读取并返回响应体，或到下一个AMT字节
# data={}
# data['wd'] = '904727147'
 
# url_values = urllib.parse.urlencode(data)
# url = "http://www.baidu.com/s?"
url = sys.argv[1]
data = urllib.urlopen(url).read()
# data = urllib3.request
data = data.decode('UTF-8')
print(data)