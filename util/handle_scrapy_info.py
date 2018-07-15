#-*-coding:utf-8-*-
from itertools import chain
import json
import os
import re
import string
from util import assistant_errcode, conf
from util.common_parser import CommonRecord, CommonParser
from base_assistant.models import WikiInfo, HashTag

"""WIKILINKBEGIN[http://xgag0.HUAWEI.COM]WIKILINKENDWIKITITLEBEGIN[VxWORKTITLE0]WIKITITLEENDWIKIABSTRACTBEGIN[]WIKIABSTRACTENDWIKICLASSESBEGIN[GROUP[KERNEL]FEATURE[VOS]CLASSES[VOS]]WIKICLASSESEND"""
"""
class WikiInfo(models.Model):
    filename = models.CharField(max_length=30)
    introduce = models.CharField(max_length=50)
    path = models.CharField(max_length=100)
    responsefield = models.ForeignKey("ResponsibilityField")
    # 相关问题列表
    solutions = models.ManyToManyField("Solution", blank=True, null=True)
    # 相关链接列表
    out_links = models.ManyToManyField("OuterLink", blank=True, null=True)
"""
class WikiRecord(CommonRecord):
#    def __init__(self, Link, Title, Abstract, Group, Feature, Classes):
    def __init__(self):
        super(WikiRecord, self).__init__()
        self.Link = ''
        self.Title = ''
        self.Content = ''
        self.Abstract = ''
        self.tags = []
        self.Group = ''
        self.Feature = ''
        self.Classes = ''

    def set_attrs(self, attrs):
        tags = attrs[4].split(',')
        classes_regex = r'GROUP\[(.+?)\]FEATURE\[(.+?)\]classes\[(.+?)\]'
        classes = re.findall(classes_regex, attrs[5])
        if len(classes) != 1:
            conf.DUMP(attrs)
            return assistant_errcode.INVALID_WIKI_FORMAT

        return self.set_attr(attrs[0], attrs[1], attrs[2], attrs[3], tags, classes[0][0], classes[0][1], classes[0][2])

    def set_attr(self, Link, Title, Content, Abstract, tags ,Group, Feature, Classes):
        #1. 将所有的空白字符转换成' '
        new_content = Content.replace('\s',' ').replace('\r\n', ' ').replace('\t', ' ').replace('\n',' ')
        #2. 将连续的空格转换成单个' ',部分那种比较特殊的字符替换不了
        while new_content.find('  ') >= 0 :
            new_content = new_content.replace('  ', ' ')

        self.Link = Link
        self.Title = Title
        self.Content = new_content
        self.Abstract = Abstract
        self.tags = tags
        self.Group = Group
        self.Feature = Feature
        self.Classes = Classes
        #conf.DUMP(self.__str__())

    def update_or_create(self):

        defaults = {'link': self.Link, 'title': self.Title, 'content':self.Content, 'abstract': self.Abstract, 'group': self.Group,
                'feature': self.Feature, 'classes': self.Classes, 'taglist':self.tags}
        link = self.Link
        WikiInfo.objects.get_or_create(link = link, defaults = defaults)

        return assistant_errcode.DB_CREATED

    def update_or_create2(self):
#        wiki_obj = WikiInfo.objects.filter(link=self.Link)
#       if len(file_obj) == 0:
#            return assistant_errcode.INVALID_FILE_INFO_NO_RES

        defaults = {'link': self.Link, 'title':self.Title, 'abstract':self.Abstract, 'group':self.Group, 'feature':self.Feature, 'classes':self.Classes }
        try:
            obj = WikiInfo.objects.get(link=self.Link)
            is_same = True
            for key, value in defaults.items():
                if (getattr(obj, key) != value):
                    is_same = False

            if not is_same:
                for key, value in defaults.items():
                    setattr(obj, key, value)
                obj.save()
            else:
                return assistant_errcode.DB_SAME
            obj.save()
            #关联hashtag
            for tag in self.tags:
                if tag == 'NULL':
                    continue
                hashtag, created = HashTag.objects.get_or_create(name=tag)
#                if hashtag.wikis.
 #               hashtag.wikis.add(obj)

            hashtag, created = HashTag.objects.get_or_create(name = self.Title)

            return assistant_errcode.DB_UPDATED
        except ResoureInfoInt.DoesNotExist:
            obj = ResoureInfoInt(file = file_obj[0], line = self.line, name = self.name, code = self.code, value = self.value, hexval = hex(self.value))
            obj.save()
            return assistant_errcode.DB_CREATED

    def __str__(self):
        return self.Link + '->' +self.Title + '->' + self.Abstract + '->' + str(self.tags) + '->' + self.Group + '->' + self.Feature + '->' + self.Classes

    def to_module(self):
        return

#WIKILINKBEGIN[http://xgag4.HUAWEI.COM]WIKILINKENDWIKITITLEBEGIN[VxWORKTITLE0]WIKITITLEENDWIKIABSTRACTBEGIN[sg]WIKIABSTRACTENDWIKITAGBEGIN[tag4]WIKITAGENDWIKICLASSESBEGIN[GROUP[KERNEL]FEATURE[VOS]classes[VOS]]WIKICLASSESEND
#WIKILINKBEGIN[http://xgag5.HUAWEI.COM]WIKILINKENDWIKITITLEBEGIN[产品注册差异文档整理-传送软件开发社区（内源&软件能力中心）-3ms知识管理社区]WIKITITLEENDWIKIABSTRACTBEGIN[Summary:框架模块mml和适配层注册产品过多，如RTN产品类型繁多……]WIKIABSTRACTENDWIKITAGBEGIN[MML,适配层]WIKITAGENDWIKICLASSESBEGIN[GROUP[KERNEL]FEATURE[VOS]classes[VOS]]WIKICLASSESEND
WIKI_IDENTIFIERS = [r'WIKILINKBEGIN[', r']WIKILINKENDWIKITITLEBEGIN[', r']WIKITITLEENDWIKICONTENTBEGIN[',']WIKICONTENTENDWIKIABSTRACTBEGIN[', r']WIKIABSTRACTENDWIKITAGBEGIN[',r']WIKITAGENDWIKICLASSESBEGIN[', r']WIKICLASSESEND',]
WIKI_REGEX_STR = r'WIKILINKBEGIN\[(.+?)\]WIKILINKENDWIKITITLEBEGIN\[(.+?)\]WIKITITLEENDWIKIABSTRACTBEGIN\[(.+?)\]WIKIABSTRACTENDWIKITAGBEGIN\[(.+?)\]WIKITAGENDWIKICLASSESBEGIN\[(.+?)\]WIKICLASSESEND'
class WikiParser(CommonParser):
    def __init__(self, lines):
        super(WikiParser, self).__init__(lines, WIKI_IDENTIFIERS, WIKI_REGEX_STR)

    def init_record(self):
        record = WikiRecord()
        return record


    def parser_one_record_multiline(self, begin, end):
        conf.DUMP(begin)
        conf.DUMP(end)
        tag = list()
        next_begin_line = begin
        search_eof_file = False
        for ident in self.split_identifiers:
            conf.DUMP(ident)
            if search_eof_file == True:
                break
            for search_line in range(next_begin_line, end + 1):
                if search_line >= self.linecount:
                    conf.DUMP("error")
                    return assistant_errcode.PARSER_RECORD_ERR
                if self.lines[search_line].find(ident) >= 0:
                    tag.append(search_line)
                    #本次搜索结束，查找下一个Ident
                    next_begin_line = search_line + 1
                    conf.DUMP(next_begin_line)
                    if next_begin_line >= self.linecount:
                        search_eof_file = True
                    break
        print(tag)
        if len(tag) != len(self.split_identifiers):
            return assistant_errcode.PARSER_RECORD_ERR

        result = list()
        tmp_content = ''
        content_begin = tag[0]
        for content_end in tag:
            if content_end == content_begin:
                continue
            tmp_content = ''.join(self.lines[content_begin + 1:content_end])
            # conf.DUMP(tmp_content)
            result.append(tmp_content)
            content_begin = content_end

        ret_result = list()
        ret_result.append(result)
        print(result)
        return ret_result

    def run(self):
        return super(WikiParser, self).run(True)

class WikiParserManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.files = []
        for root, dirs, files in os.walk(file_path):
            for file in files:
                self.files.append(file)
        self.created_records = 0
        self.updated_records = 0

    def run(self):
        for file in self.files:
            wikiinfo_file = open(self.file_path + file, 'r', encoding='UTF-8')
            lines = wikiinfo_file.readlines()
            print(lines)
            parser = WikiParser(lines=lines)
            result = parser.run()
            wikiinfo_file.close()
            conf.DUMP('parser file' + self.file_path + file + ' ' + str(result))
            if result != assistant_errcode.WIKI_PARSE_SUCCESS:
                return result
            self.created_records += parser.created_records
            self.updated_records += parser.updated_records

        return assistant_errcode.WIKI_PARSE_SUCCESS
