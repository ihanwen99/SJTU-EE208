#!/usr/bin/env python
# encoding=utf-8
INDEX_DIR = "IndexFiles.index"

import sys, os, lucene

from java.io import File
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.util import Version
from org.apache.lucene.search import BooleanQuery
from org.apache.lucene.search import BooleanClause
import jieba


def parseCommand(command):
    allowed_opt = ['site']
    command_dict = {}
    opt = 'contents'
    for i in command.split(' '):
        if ':' in i:
            opt, value = i.split(':')[:2]
            opt = opt.lower()
            if opt in allowed_opt and value != '':
                command_dict[opt] = command_dict.get(opt, '') + ' ' + value
        else:
            command = " ".join(jieba.cut(i))
            command_dict[opt] = command_dict.get(opt, '') + ' ' + i
    return command_dict


def run_txt(valueFromOut, searcher, analyzer):
    command = valueFromOut

    seg_list = jieba.cut(command)
    command = " ".join(seg_list)
    if command == '':
        return
    result = []
    command_dict = parseCommand(command)
    querys = BooleanQuery()
    for k, v in command_dict.iteritems():
        query = QueryParser(Version.LUCENE_CURRENT, k,
                            analyzer).parse(v)
        querys.add(query, BooleanClause.Occur.MUST)
    scoreDocs = searcher.search(querys, 10).scoreDocs
    print "%s total matching documents." % len(scoreDocs)

    for scoreDoc in scoreDocs:
        doc = searcher.doc(scoreDoc.doc)
        partResult = {}

        partResult['title'] = doc.get('title')
        partResult['url'] = doc.get('url')
        partResult['keyword'] = doc.get('keyword')

        result.append(partResult)

    return result


def run_pic(valueFromOut, searcher, analyzer):
    command = valueFromOut

    seg_list = jieba.cut(command)
    command = " ".join(seg_list)
    if command == '':
        return

    result = []
    command_dict = parseCommand(command)
    querys = BooleanQuery()
    for k, v in command_dict.iteritems():
        query = QueryParser(Version.LUCENE_CURRENT, k,
                            analyzer).parse(v)
        querys.add(query, BooleanClause.Occur.MUST)
    scoreDocs = searcher.search(querys, 10).scoreDocs
    print "%s total matching documents." % len(scoreDocs)

    for scoreDoc in scoreDocs:
        doc = searcher.doc(scoreDoc.doc)
        partResult = {}

        partResult['title'] = doc.get('urltitle')
        partResult['url'] = doc.get('url')
        partResult['imgurl'] = doc.get('imgurl')

        result.append(partResult)

    return result


STORE_DIR_txt = "lab7_txt_index"
vm_env = lucene.initVM(vmargs=['-Djava.awt.headless=true'])


def lab7txtSearch(valueFromOut):
    vm_env.attachCurrentThread()
    print 'lucene', lucene.VERSION
    # base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    directory = SimpleFSDirectory(File(STORE_DIR_txt))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
    result = run_txt(valueFromOut, searcher, analyzer)
    del searcher
    return result


STORE_DIR_pic = "lab7_pic_index"


def lab7picSearch(valueFromOut):
    vm_env.attachCurrentThread()
    print 'lucene', lucene.VERSION
    # base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    directory = SimpleFSDirectory(File(STORE_DIR_pic))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
    result = run_pic(valueFromOut, searcher, analyzer)
    del searcher
    return result

# a = '旅游文化资源'
# b = lab7txtSearch(a)
# print(b)
# print(len(b))
# for i in range(len(b)):
#    print(b[i]['url'])  # http://you.ctrip.com/travels/wuyuan446.html
#    print(b[i]['title'])  # 婺源旅游游记,婺源游记攻略,婺源精品/热门/最新游记推荐【携程攻略】
#    print(b[i]['keyword'])  # 婺源游记,婺源游记攻略,婺源旅游游记,婺源热门游记,婺源精品游记,婺源游记推荐

# a = '旅游文化资源'
# b = lab7picSearch(a)
# print(b)
# print(len(b))
# for i in range(len(b)):
#    print(b[i]['url'])  # http://weekend.ctrip.com/around/Shenyang
#    print(b[i]['title'])  # 沈阳周末去哪玩,沈阳周末短途游线路,沈阳周边自驾游【携程周末游】
#    print(
#    b[i]['imgurl']) # https://dimg07.c-ctrip.com/images/fd/tg/g1/M05/A0/B5/CghzflWQ-HSAWZLhAABD1cgcfn8514_C_280_150.jpg
