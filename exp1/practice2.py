import sys
import urllib2
from bs4 import BeautifulSoup


def parseIMG(content):
    urlset = set()
    soup = BeautifulSoup(content)
    for i in soup.findAll('img'):
        url= i.get('src','')
        print(url)
        urlset.add(url)
    return urlset


def write_outputs(urls, filename):
    with open(filename, 'w') as f:
        for url in urls:
            f.write(url)
            f.write('\n')


def main():
    # url = 'http://www.baidu.com'
    url = 'http://www.sjtu.edu.cn'
    if len(sys.argv) > 1:
        url = sys.argv[1]
    content = urllib2.urlopen(url).read()
    imgs = parseIMG(content)
    write_outputs(imgs, 'res2.txt')


if __name__ == '__main__':
    main()
