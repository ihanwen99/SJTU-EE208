import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import re
import urllib2
import urlparse
from bs4 import BeautifulSoup

agent = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}

def parseQiushibaikePic(content):

    soup = BeautifulSoup(content)
    for i in soup.findAll('div', {'id': re.compile('^qiushi_tag_\d+')}):
        global tag
        tag = i.get('id','')
        print(tag)
    for j in soup.body.findAll('div', {'class': re.compile('^content$')}):
        for k in soup.body.findAll('div', {'class': re.compile('^thumb$')}):
            log = 'http://www.'
            img = urlparse.urljoin(log, k.img['src'])
            docs = {tag.split('_')[-1]: {'content': j.text.replace("\n", ""), 'imgurl': img}}
            print(docs)
    for t in soup.body.findAll('input', {'id': re.compile('^articleNextLink')}):
        nextpage = t.get('value')
        url = 'http://www.qiushibaike.com/pic'
        nextpage = urlparse.urljoin(url, nextpage)
        return docs, nextpage


def write_outputs(urls, filename):
    with open(filename, 'w') as f:
        urls = list(urls)
        f.write(((urls[0])[tag.split('_')[-1]])['imgurl'] + '\t' + ((urls[0])[tag.split('_')[-1]])['content'] + '\n' + urls[1])


def main():
    url = urllib2.Request('https://www.qiushibaike.com/article/112782870', headers=agent)
    if len(sys.argv) > 1:
        url = sys.argv[1]
    content = urllib2.urlopen(url).read()
    Info = parseQiushibaikePic(content)

    write_outputs(Info, 'res3.txt')


if __name__ == '__main__':
    main()
