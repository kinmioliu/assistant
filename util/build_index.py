#-*-coding:utf-8-*-
import jieba
from util.conf import *
from base_assistant.models import HashTag, MMLCmdInfo, EVTCmdInfo, IndexInfo
import os
from util import conf
#from assistant.settings import IndexDllObj
from ctypes import *

WIKI_TYPE =  0x01000000
MML_TYPE = 0x02000000
EVT_TYPE = 0x03000000
INTRES_TYPE = 0x04000000

class PostingInfo:
    def __init__(self, tf):
        #词频率
        self.tf = tf
        #出现位置
        self.position = []

class PostingList:
    def __init__(self):
        #文档频率
        self.df = 0
        # key = docid, val = PostingInfo
        self.postinginfo = dict()

    def update(self, docid):
        #文档频率+1
        self.df += 1;
        if docid in self.postinginfo:
            #增加1
            self.postinginfo[docid].tf += 1
        else:
            #新增一个，tf初始化为1
            self.postinginfo[docid] = PostingInfo(1)

    def __str__(self):
        new_str = str(self.df) + ','
        #用于indexMng 的count
        new_str += str(self.df * 2)
        for postinfo in self.postinginfo:
            new_str += ','
            new_str += hex(postinfo)
            new_str += ','
            new_str += str(self.postinginfo[postinfo].tf)
        return new_str

class IndexBuilder:
    def __init__(self):
        self.created_records = 0
        self.updated_records = 0
        base_dir = os.path.dirname(os.path.abspath(__name__))
        stopwords_filepath = os.path.join(base_dir, 'static', conf.STOP_WORDS_LIST_PATH);
        self.stopwords = self.load_stop_words(stopwords_filepath)
        self.InvertedMap = dict()

    def invertedmap_to_txt(self):
        inverted_file = open('inverted_file.txt', 'w', encoding='utf-8')
        for postinfo in self.InvertedMap:
            # /*设置信息*/Index[168] = AllocIndexInfo(3,6,5,3,5,6,7,1);
            print(postinfo)
            objs = IndexInfo.objects.get(word = postinfo)
            dbid = objs.id
            new_str = '/*' + postinfo + '*/\tIndex[' + str(dbid) + '] = AllocIndexInfo(' + str(self.InvertedMap[postinfo]) + ');\n'
            print(new_str)
            inverted_file.write(new_str)

        inverted_file.close()


    def load_stop_words(self, filepath):
        stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
        return stopwords

    def update_or_create_indexinfo(self, token, docid):
        if token in self.stopwords:
            print("token '" + token + "'in stop words，跳过")
            return 0

        #从IndexMap中查找是否存在这个Token，如果存在,那么只需要跟新对应的PostingList
        #如果不存在，那么就在map中新建，然后数据库中CreateOrIndex
        if token in self.InvertedMap:
            self.InvertedMap[token].update(docid)
        else:
            self.InvertedMap[token] = PostingList()
            self.InvertedMap[token].update(docid)
            #写数据库库
            try:
                obj = IndexInfo.objects.get(word = token)
            except IndexInfo.DoesNotExist:
                obj = IndexInfo(word = token)
                obj.save()
        return 0

    def allocate_docid(self, doc_type, dbid):
        if (dbid >= 0x01000000):
            return 0
        return doc_type | dbid

    def run(self):
        DUMP("Build Index Begin")

        DUMP("Build Index for MML CMD Begin")
        all_mmlcmdinfos = MMLCmdInfo.objects.all()
        for mmlcmdinfo in all_mmlcmdinfos:
            mml_id = mmlcmdinfo.id
            mml_name = mmlcmdinfo.cmdname
            mml_func = mmlcmdinfo.cmd_func
            mml_mark = mmlcmdinfo.cmd_mark
            content = mml_name + ' ' + mml_func + ' ' + mml_mark
            words = jieba.cut_for_search(content)
            for word in words:
                self.update_or_create_indexinfo(word, self.allocate_docid(MML_TYPE, mml_id))
        DUMP("Build Index for MML CMD End")

        self.invertedmap_to_txt()

        return 0