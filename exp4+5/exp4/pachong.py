# -*- coding:utf-8 -*-
import threading
import Queue
import time
import os
import urlparse
import urllib2
import re
import sys
import string
from bs4 import BeautifulSoup


def valid_filename(s):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    s = ''.join(c for c in s if c in valid_chars)
    return s


def get_page(page):
    try:
        response = urllib2.urlopen(page, timeout=25)
        HttpMessage = response.info()
        ContentType = HttpMessage.gettype()
        if "text/html" != ContentType:
            return None
        else:
            print 'downloading page %s' % page
            content = response.read()
    except(urllib2.URLError, UnicodeEncodeError):
        print("Error!")
    else:
        return content


def get_all_links(content, page):
    links = []
    soup = BeautifulSoup(content, features="html.parser")
    for i in soup.findAll('a', {'href': re.compile('^http|^/')}):
        url = i['href']
        newUrl = urlparse.urljoin(page, url)
        links.append(newUrl)

    return links


def add_page_to_folder(page, content):  # 将网页存到文件夹里，将网址和对应的文件名写入index.txt中
    index_filename = 'index_hhh_zhihu.txt'  # index.txt中每行是'网址 对应的文件名'
    folder = 'html_hhh_zhihu'  # 存放网页的文件夹
    filename = valid_filename(page)  # 将网址变成合法的文件名
    index = open(index_filename, 'a')
    index.write(page.encode('ascii', 'ignore') + '\t' + filename + '\n')
    index.close()
    if not os.path.exists(folder):  # 如果文件夹不存在则新建
        os.mkdir(folder)
    f = open(os.path.join(folder, filename), 'w')
    f.write(content)  # 将网页存入文件
    f.close()


def working():
    while True and len(crawled) <= 5000:
        page = q.get()
        if page not in crawled:
            try:
                content = get_page(page)
            except:
                print("Error!")
            else:
                if content != None:
                    add_page_to_folder(page, content)
                    outlinks = get_all_links(content, page)
                    for link in outlinks:
                        q.put(link)
                    if varLock.acquire():
                        crawled.append(page)
                        varLock.release()
                    q.task_done()


start = time.clock()
NUM = 20
crawled = []

varLock = threading.Lock()
q = Queue.Queue()
q.put('https://www.zhihu.com')
thread_list = []
for i in range(NUM):
    t = threading.Thread(target=working)
    thread_list.append(t)

print(thread_list)
for t in thread_list:
    t.setDaemon(True)
    t.start()
for t in thread_list:
    t.join()

end = time.clock()
print end - start
