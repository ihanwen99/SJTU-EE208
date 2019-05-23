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
        content = urllib2.urlopen(page, timeout=100).read()
        print 'downloading page %s' % page
        time.sleep(0.5)
    except(urllib2.URLError):
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
    index_filename = 'index.txt'  # index.txt中每行是'网址 对应的文件名'
    folder = 'html'  # 存放网页的文件夹
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
    while True and len(crawled) <= 10:
        page = q.get()
        if page not in crawled:
            content = get_page(page)
            if content != None:
                add_page_to_folder(page, content)
                outlinks = get_all_links(content, page)
                for link in outlinks:
                    q.put(link)
                if varLock.acquire():
                    graph[page] = outlinks
                    crawled.append(page)
                    varLock.release()
                q.task_done()


start = time.clock()
NUM = 2
crawled = []
graph = {}
varLock = threading.Lock()
q = Queue.Queue()
q.put('http://www.sjtu.edu.cn')
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
print(graph)
