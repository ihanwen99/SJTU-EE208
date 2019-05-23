# -*- coding:utf-8 -*-
import urllib2, cookielib, urllib
from bs4 import BeautifulSoup

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)

postdata_login = urllib.urlencode({
    'id': 'davidstark',
    'pw': 'davidstark',
    'submit': 'login'
})
req = urllib2.Request(url='https://bbs.sjtu.edu.cn/bbslogin', data=postdata_login)
response = urllib2.urlopen(req)

text = 'hellobbs12345'
postdata = urllib.urlencode({
    'text': text,
    'type': 'update'
})

req = urllib2.Request(url='https://bbs.sjtu.edu.cn/bbsplan', data=postdata)
response = urllib2.urlopen(req)

content = urllib2.urlopen('https://bbs.sjtu.edu.cn/bbsplan').read()
soup = BeautifulSoup(content, features="html.parser")
print str(soup.find('textarea').string).strip().decode('utf8')
