#!/usr/bin/env python
# encoding=utf-8

INDEX_DIR = "IndexFiles.index"

import sys, os, lucene, threading, time, re
from datetime import datetime

from java.io import File
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version

import jieba
from bs4 import BeautifulSoup
from urlparse import urlparse

set = []

file1 = open("lab5.txt")
for line in file1.readlines():
    a, b = line.strip('\n').split()
    set.append((a, b))

"""
This class is loosely based on the Lucene (java implementation) demo class 
org.apache.lucene.demo.IndexFiles.  It will take a directory as an argument
and will index all of the files in that directory and downward recursively.
It will index on the file path, the file name and the file contents.  The
resulting Lucene index will be placed in the current directory and called
'index'.
"""


class Ticker(object):

    def __init__(self):
        self.tick = True

    def run(self):
        while self.tick:
            sys.stdout.write('.')
            sys.stdout.flush()
            # time.sleep(1.0)


class IndexFiles(object):
    """Usage: python IndexFiles <doc_directory>"""

    def __init__(self, root, storeDir, analyzer):

        if not os.path.exists(storeDir):
            os.mkdir(storeDir)

        store = SimpleFSDirectory(File(storeDir))
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

    def getTxtAttribute(self, contents, attr):
        m = re.search(attr + ': (.*?)\n', contents)
        if m:
            return m.group(1)
        else:
            return ''

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

        t3 = FieldType()
        t3.setIndexed(False)
        t3.setStored(True)
        t3.setTokenized(False)

        t4 = FieldType()
        t4.setIndexed(False)
        t4.setStored(True)
        t4.setTokenized(False)

        t5 = FieldType()
        t5.setIndexed(False)
        t5.setStored(True)
        t5.setTokenized(False)

        for root, dirnames, filenames in os.walk(root):
            for filename in filenames:
                # if not filename.endswith('.txt'):
                #    continue
                try:
                    path = os.path.join(root, filename)
                    file = open(path)
                    print "adding", filename
                    for i in set:
                        if i[1] == filename:
                            url = i[0]
                            parsed = urlparse(url)
                            site = parsed.netloc

                    contents = file.read()

                    soup = BeautifulSoup(contents, "html.parser")
                    title = soup.head.title.string

                    contents = ''.join(soup.findAll(text=True))
                    seg_list = jieba.cut(contents)
                    contents = " ".join(seg_list)

                    file.close()
                    doc = Document()
                    doc.add(Field("name", filename, t1))
                    doc.add(Field("path", path, t1))
                    doc.add(Field("title", title, t3))
                    doc.add(Field("url", url, t4))
                    doc.add(Field("site", site, t5))
                    if len(contents) > 0:

                        doc.add(Field("contents", contents, t2))

                    else:
                        print "warning: no content in %s" % filename
                    writer.addDocument(doc)
                except Exception, e:
                    print "Failed in indexDocs:", e


if __name__ == '__main__':
    """
    if len(sys.argv) < 2:
        print IndexFiles.__doc__
        sys.exit(1)
    """
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print 'lucene', lucene.VERSION
    start = datetime.now()
    try:
        """
        base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        IndexFiles(sys.argv[1], os.path.join(base_dir, INDEX_DIR),
                   StandardAnalyzer(Version.LUCENE_CURRENT))
                   """
        analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
        IndexFiles('html_lab5', "lab5_index", analyzer)
        end = datetime.now()
        print end - start
    except Exception, e:
        print "Failed: ", e
        raise e
