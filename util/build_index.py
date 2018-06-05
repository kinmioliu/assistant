#-*-coding:utf-8-*-
import jieba
from util.conf import *
from base_assistant.models import HashTag
import os
from util import conf
#from assistant.settings import IndexDllObj
from ctypes import *

WIKI_TYPE =  0x01000000
MML_TYPE = 0x02000000
EVT_TYPE = 0x03000000
INTRES_TYPE = 0x04000000

class IndexBuilder:
    def __init__(self):
        self.created_records = 0
        self.updated_records = 0
        base_dir = os.path.dirname(os.path.abspath(__name__))
        stopwords_filepath = os.path.join(base_dir, 'static', conf.STOP_WORDS_LIST_PATH);
        self.stopwords = self.load_stop_words(stopwords_filepath)

    def load_stop_words(self, filepath):
        stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
        return stopwords

    def update_or_create_indexinfo(self, token, docid):
        print(token)
        print(hex(docid))
        if token in self.stopwords:
            print(token + "in stop words")
            return 0
        str = c_wchar_p(token)
        print(str)
        #ret = IndexDllObj.UpdateOrCreateIndexInfo(str, len(token), docid)
        #print(ret)
        return 0

    def allocate_docid(self, doc_type, dbid):
        if (dbid >= 0x01000000):
            return 0

        return doc_type | dbid

    def run(self):
        DUMP("Build Index Begin")
        tags = HashTag.objects.all()
        for tag in tags:
            tag_name = tag.name
            splits = jieba.cut_for_search(tag_name)
            for obj in splits:
                self.update_or_create_indexinfo(obj, self.allocate_docid(WIKI_TYPE, tag.id))
        #ret = IndexDllObj.InitIndexInfoFromFile()
        #print(ret)
        DUMP("Build Index End")
        return 0