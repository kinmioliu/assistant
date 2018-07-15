#-*-coding:utf-8-*-
import jieba
from util.conf import *
from base_assistant.models import HashTag, MMLCmdInfo, EVTCmdInfo, IndexInfo, WikiInfo, HashTag
import os
from util import conf
#from assistant.settings import IndexDllObj
from ctypes import *
#0001 0010 0100 1000
ID_MASK = 0x00ffffff
TYPE_MASK = 0xff000000
WIKI_TYPE =  0x01000000
MML_TYPE = 0x02000000
EVT_TYPE = 0x04000000
INTRES_TYPE = 0x08000000

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

    def update(self, docid, position):
        if docid in self.postinginfo:
            #增加1
            self.postinginfo[docid].tf += 1
        else:
            #新增一个，tf初始化为1
            self.postinginfo[docid] = PostingInfo(1)
            #文档频率+1
            self.df += 1;
        #更新position
        print(position)
        self.postinginfo[docid].position.append(position)

    def __str__(self):
        new_str = str(self.df)# + ','
        for postinfo in self.postinginfo:
            new_str += ','
            new_str += hex(postinfo) #docid
            new_str += ','
            new_str += str(self.postinginfo[postinfo].tf)   #tf
            new_str += ',<'
            for position in self.postinginfo[postinfo].position: #position
                new_str += str(position)
                new_str += ','
            new_str += '>'
        return new_str

class DocInfo:
    def __init__(self, doc_len, title_len, abstract_len, content_len):
        self.doc_len = doc_len
        self.title_len = title_len
        self.abstract_len = abstract_len
        self.content_len = content_len

    def __str__(self):
        new_str = str(self.doc_len) + ',' + str(self.title_len) + ',' + str(self.abstract_len) + ',' + str(self.content_len)
        return new_str

class IndexBuilder:
    def __init__(self):
        self.created_records = 0
        self.updated_records = 0
        base_dir = os.path.dirname(os.path.abspath(__name__))
        stopwords_filepath = os.path.join(base_dir, 'static', conf.STOP_WORDS_LIST_PATH);
        self.stopwords = self.load_stop_words(stopwords_filepath)
        self.InvertedMap = dict()
        #初始化自定义词
        hashobjs = HashTag.objects.all()
        tdswords_filepath = os.path.join(base_dir, 'static', conf.TDS_WORDS_LIST_PATH);
        tdsword_file = open(tdswords_filepath, 'w', encoding='utf-8')
        for obj in hashobjs:
            tdsword_file.write(obj.name + '\n')
        tdsword_file.close()
        self.tdswords_filepath = tdswords_filepath
        self.DocTable = dict()
        jieba.load_userdict(tdswords_filepath)

    def invertedmap_to_txt(self):
        inverted_file = open('inverted_file.txt', 'w', encoding='utf-8')
        for postinfo in self.InvertedMap:
            print(postinfo)
            objs = IndexInfo.objects.get(word = postinfo)
            dbid = objs.id
            new_str = '/*' + postinfo + '*/\tIndex[' + str(dbid) + '] = AllocIndexInfo(' + str(self.InvertedMap[postinfo]) + ');\n'
            print(new_str)
            inverted_file.write(new_str)

        #TODO 需要按照文档的类别进行一次分类
        all_doc_cont = len(self.DocTable)
        new_str = 'const unsigned int MMLDocCounts = ' + str(all_doc_cont) + ' ;'

        for doc in self.DocTable:
            new_str = 'DocInfoTable[' + hex(doc) + '] = ' + str(self.DocTable[doc]) + ' ;\n'
            inverted_file.write(new_str)

        inverted_file.close()


    def load_stop_words(self, filepath):
        stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
        return stopwords

    def update_doc_len(self, docid, doc_len, title_len = 0, abstract_len = 0, content_len = 0):
        doc_info = DocInfo(doc_len, title_len, abstract_len, content_len)
        self.DocTable[docid] = doc_info
        pass

    def update_or_create_indexinfo_v2(self, token, position, docid):
        if token in self.stopwords:
            print("token '" + token + "'in stop words，跳过")
            return 0
        if token == '\r\n' or token == '\t' or token == '\n' or token == ' ':
            print("token '" + token + "'in stop words，跳过")
            return 0

        #同一转换成小写
        token = token.lower()
        #从IndexMap中查找是否存在这个Token，如果存在,那么只需要跟新对应的PostingList
        #如果不存在，那么就在map中新建，然后数据库中CreateOrIndex
        if token in self.InvertedMap:
            self.InvertedMap[token].update(docid, position)
        else:
            self.InvertedMap[token] = PostingList()
            self.InvertedMap[token].update(docid, position)
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

    def build_wiki_info(self):
        all_wiki_info = WikiInfo.objects.all()
        for wikiinfo in all_wiki_info:
            wiki_id = wikiinfo.id
            titile = wikiinfo.title
            content = wikiinfo.content
            abstract = wikiinfo.abstract
            docid = self.allocate_docid(WIKI_TYPE, wiki_id)

            titile_len = len(titile)
            abstract_len = len(abstract)
            content_len = len(content)

            #使用扩展列表的方式进行存储position
            words = jieba.tokenize(titile, mode='search')
            for word in words:
                self.update_or_create_indexinfo_v2(word[0], word[1], docid)

            words = jieba.tokenize(abstract, mode='search')
            for word in words:
                self.update_or_create_indexinfo_v2(word[0], word[1] + titile_len, docid)

            words = jieba.tokenize(content, mode='search')
            for word in words:
                self.update_or_create_indexinfo_v2(word[0], word[1] + titile_len + abstract_len, docid)
            self.update_doc_len(docid, titile_len + abstract_len + content_len, titile_len, abstract_len, content_len)

        pass

    def build_mml_info(self):
        all_mml_info = MMLCmdInfo.objects.all()
        for mmlinfo in all_mml_info:
            mml_id = mmlinfo.id
            name = mmlinfo.cmdname
            func = mmlinfo.cmd_func
            attention = mmlinfo.cmd_attention
            mark = mmlinfo.cmd_mark
            docid = self.allocate_docid(MML_TYPE, mml_id)

            #使用扩展列表的方式进行存储position
            words = jieba.tokenize(name + func + attention + mark, mode='search')
            for word in words:
                self.update_or_create_indexinfo_v2(word[0], word[1], docid)

            self.update_doc_len(docid, len(name + func + attention + mark), 0, 0, 0)
        pass


    def build_evt_info(self):
        all_mml_info = EVTCmdInfo.objects.all()
        for mmlinfo in all_mml_info:
            mml_id = mmlinfo.id
            name = mmlinfo.cmdname
            func = mmlinfo.cmd_func
            attention = mmlinfo.cmd_attention
            mark = mmlinfo.cmd_mark
            docid = self.allocate_docid(MML_TYPE, mml_id)

            #使用扩展列表的方式进行存储position
            words = jieba.tokenize(name + func + attention + mark, mode='search')
            for word in words:
                self.update_or_create_indexinfo_v2(word[0], word[1], docid)

            self.update_doc_len(docid, len(name + func + attention + mark), 0, 0, 0)
        pass


    def run(self):
        DUMP("Build Index Begin")

        # DUMP("Build Index for MML CMD Begin")
        # all_mmlcmdinfos = MMLCmdInfo.objects.all()
        # for mmlcmdinfo in all_mmlcmdinfos:
        #     mml_id = mmlcmdinfo.id
        #     mml_name = mmlcmdinfo.cmdname
        #     mml_func = mmlcmdinfo.cmd_func
        #     mml_mark = mmlcmdinfo.cmd_mark
        #     content = mml_name + ' ' + mml_func + ' ' + mml_mark
        #     words = jieba.cut_for_search(content)
        #     docid = self.allocate_docid(MML_TYPE, mml_id)
        #     self.update_doc_len(docid, len(content))
        #     for word in words:
        #         self.update_or_create_indexinfo(word, docid)
        # DUMP("Build Index for MML CMD End")

        self.build_wiki_info()
        self.build_mml_info()
        self.build_evt_info()

        self.invertedmap_to_txt()

        return 0