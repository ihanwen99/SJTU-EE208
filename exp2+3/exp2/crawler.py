# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import urllib2
import re
import urlparse
import os
import sys
import string


def valid_filename(s):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    s = ''.join(c for c in s if c in valid_chars)
    return s


def get_page(page):
    try:
        content = urllib2.urlopen(page, timeout=100).read()
    except:
        return None

    return content


def get_all_links(content, page):
    links = []
    soup = BeautifulSoup(content, features="html.parser")
    for i in soup.findAll('a', {'href': re.compile('^http|^/')}):
        url = i['href']
        newUrl = urlparse.urljoin(page, url)
        links.append(newUrl)

    return links


def union_dfs(a, b):
    for e in b:
        if e not in a:
            a.append(e)


def union_bfs(a, b):
    for e in b:
        if e not in a:
            a.insert(0, e)


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


def crawl(seed, method, max_page):
    tocrawl = [seed]
    crawled = []
    graph = {}
    count = 0

    while tocrawl and count <= max_page:
        page = tocrawl.pop()
        if page not in crawled:
            content = get_page(page)
            if content != None:
                add_page_to_folder(page, content)
                outlinks = get_all_links(content, page)
                globals()['union_%s' % method](tocrawl, outlinks)

            crawled.append(page)
            count += 1
            print(count,page)
    return graph, crawled


if __name__ == '__main__':
    seed = 'http://www.sjtu.edu.cn'
    method = 'dfs'
    max_page = 10
    if len(sys.argv) > 1:
        seed = sys.argv[1]
        if len(sys.argv) > 2:
            method = sys.argv[2]
            if len(sys.argv) > 3:
                max_page = sys.argv[3]

    graph, crawled = crawl(seed, method, max_page)


