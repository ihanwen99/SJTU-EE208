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
    except:
        print("Error!")
    else:
        return content


def get_all_links(content, page):
    links = []
    soup = BeautifulSoup(content, features="html.parser")
    for i in soup.findAll('a', {'href': re.compile('^http|^/')}):
        url = i['href']

        if 'fengjingsheying/2018'.decode() in url:

            if 'li'.decode() in i.parent.name:

                newUrl = urlparse.urljoin(page, url)
                links.append(newUrl)

    return links


def add_page_to_folder(page, content):  # 将网页存到文件夹里，将网址和对应的文件名写入index.txt中
    index_filename = 'fengjingsheying.txt'  # index.txt中每行是'网址 对应的文件名'
    folder = 'fengjingsheying'  # 存放网页的文件夹
    filename = valid_filename(page)  # 将网址变成合法的文件名6
    index = open(index_filename, 'a')
    index.write(page.encode('ascii', 'ignore') + '\t' + filename + '\n')
    index.close()
    if not os.path.exists(folder):  # 如果文件夹不存在则新建
        os.mkdir(folder)
    try:
        f = open(os.path.join(folder, filename), 'w')
    except:
        print("Error!")
    else:
        f.write(content)  # 将网页存入文件
        f.close()


def working():
    """
        page = q.get()

        content = get_page(page)

        if content != None:
            add_page_to_folder(page, content)
            outlinks = get_all_links(content, page)
            for link in outlinks:
                if 'meinvtupian' in link:

                    q.put(link)
            if varLock.acquire():
                crawled.append(page)
                varLock.release()
            q.task_done()
    """

    while True and len(crawled) <= 3999:
        page = q.get()
        if page not in crawled:
            if 'fengjingsheying' in page:
                content = get_page(page)
            else:
                continue

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
# q.put('http://www.27270.com/zt/xinggan/')
q.put('http://www.27270.com/word/fengjingsheying/2018/307027.html')
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
