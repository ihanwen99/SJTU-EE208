#!/usr/bin/env python
# encoding=utf-8

INDEX_DIR = "IndexFiles.index"

import sys, os, lucene, threading, time, jieba
from datetime import datetime
from bs4 import BeautifulSoup
from java.io import File
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version

"""
This class is loosely based on the Lucene (java implementation) demo class 
org.apache.lucene.demo.IndexFiles.  It will take a directory as an argument
and will index all of the files in that directory and downward recursively.
It will index on the file path, the file name and the file contents.  The
resulting Lucene index will be placed in the current directory and called
'index'.
"""

import jieba
from bs4 import BeautifulSoup

set = []

file1 = open("lab5.txt")
for line in file1.readlines():
    a, b = line.strip('\n').split()
    set.append((a, b))


def getinfo(img):
    try:
        contents = img['alt']
    except:
        try:
            contents = img.parent['title']
        except:
            try:
                contents = img.parent.nextSibling.h4.string
            except:
                return None
    return contents


class Ticker(object):

    def __init__(self):
        self.tick = True

    def run(self):
        while self.tick:
            sys.stdout.write('.')
            sys.stdout.flush()
            time.sleep(1.0)


class IndexFiles(object):
    """Usage: python IndexFiles <doc_directory>"""

    def __init__(self, root, storeDir):

        if not os.path.exists(storeDir):
            os.mkdir(storeDir)

        store = SimpleFSDirectory(File(storeDir))
        analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
        analyzer = LimitTokenCountAnalyzer(analyzer, 1048576)
        config = IndexWriterConfig(Version.LUCENE_CURRENT, analyzer)
        config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
        writer = IndexWriter(store, config)

        self.indexDocs(root, writer)
        ticker = Ticker()
        print 'commit index',
        threading.Thread(target=ticker.run).start()
        writer.commit()
        writer.close()
        ticker.tick = False
        print 'done'

    def indexDocs(self, root, writer):

        t1 = FieldType()
        t1.setIndexed(False)
        t1.setStored(True)
        t1.setTokenized(False)

        t2 = FieldType()
        t2.setIndexed(True)
        t2.setStored(False)
        t2.setTokenized(True)
        t2.setIndexOptions(FieldInfo.IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)

        for root, dirnames, filenames in os.walk(root):
            for filename in filenames:
                # if not filename.endswith('.txt'):
                #    continue
                print "adding", filename
                try:
                    path = os.path.join(root, filename)

                    file = open(path)

                    for i in set:
                        if i[1] == filename:
                            url = i[0]

                    soup = BeautifulSoup(file.read())
                    imgurls = soup.findAll('img')
                    title = soup.head.title.string
                    file.close()
                    for img in imgurls:
                        imgurl = img['src']
                        strs = getinfo(img)
                        seg_list = jieba.cut(strs)
                        contents = ' '.join(seg_list)
                        doc = Document()
                        doc.add(Field("imgurl", imgurl, t1))
                        doc.add(Field("urltitle", title, t1))
                        doc.add(Field("url", url, t1))
                        if len(contents) > 0:
                            doc.add(Field("contents", contents, t2))
                        else:
                            print "warning: no content in %s" % filename
                        writer.addDocument(doc)



                except Exception, e:
                    print "Failed in indexDocs:", e


if __name__ == '__main__':
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print 'lucene', lucene.VERSION
    start = datetime.now()
    try:
        IndexFiles('html_lab5', "indeximg")
        end = datetime.now()
        print end - start
    except Exception, e:
        print "Failed: ", e
        raise e
