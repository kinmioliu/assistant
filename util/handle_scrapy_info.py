#-*-coding:utf-8-*-
from itertools import chain
import json
import os
import re
import string
from util import assistant_errcode, conf
from util.common_parser import CommonRecord, CommonParser

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
        self.Abstract = ''
        self.Group = ''
        self.Feature = ''
        self.Classes = ''

    def set_attr(self, attrs):
        print(attrs)
        return self.set_attr(attrs[0], attrs[1], attrs[2], attrs[3], attrs[4], attrs[5])

    def set_attr(self, Link, Title, Abstract, Group, Feature, Classes):
        self.Link = Link
        self.Title = Title
        self.Abstract = Abstract
        self.Group = Group
        self.Feature = Feature
        self.Classes = Classes

    def update_or_create(self):
        file_obj = FileInfo.objects.filter(filename=self.file)
        if len(file_obj) == 0:
            return assistant_errcode.INVALID_FILE_INFO_NO_RES

        defaults = {'line': self.line, 'name':self.name, 'value':self.value, 'hexval':hex(self.value)}
        try:
            obj = ResoureInfoInt.objects.get(code=self.code)
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
            return assistant_errcode.DB_UPDATED
        except ResoureInfoInt.DoesNotExist:
            obj = ResoureInfoInt(file = file_obj[0], line = self.line, name = self.name, code = self.code, value = self.value, hexval = hex(self.value))
            obj.save()
            return assistant_errcode.DB_CREATED

    def __str__(self):
        return self.Title

    def to_module(self):
        return

#"""WIKILINKBEGIN[http://xgag0.HUAWEI.COM]WIKILINKENDWIKITITLEBEGIN[VxWORKTITLE0]WIKITITLEENDWIKIABSTRACTBEGIN[]WIKIABSTRACTENDWIKICLASSESBEGIN[GROUP[KERNEL]FEATURE[VOS]CLASSES[VOS]]WIKICLASSESEND"""

#WIKI_IDENTIFIERS = [r'WIKILINKBEGIN\[', r'\]WIKILINKENDWIKITITLEBEGIN\[', r'\]WIKITITLEENDWIKIABSTRACTBEGIN\[',r'\]WIKIABSTRACTENDWIKICLASSESBEGIN\[',r'\]WIKICLASSESEND',]
WIKI_IDENTIFIERS = [r'WIKILINKBEGIN[', r']WIKILINKENDWIKITITLEBEGIN[', r']WIKITITLEENDWIKIABSTRACTBEGIN[',r']WIKIABSTRACTENDWIKICLASSESBEGIN[',r']WIKICLASSESEND',]
WIKI_REGE_X
class WikiParser(CommonParser):
    def __init__(self, lines):
        super(WikiParser, self).__init__(lines, WIKI_IDENTIFIERS, reg_ex)

    def init_record(self):
        record = WikiRecord()
        return record

    def run(self):
        return super(WikiParser, self).run(False)



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
            print(parser.created_records)
            print(parser.updated_records)
            self.created_records += len(parser.created_records)
            self.updated_records += len(parser.updated_records)

        return assistant_errcode.WIKI_PARSE_SUCCESS
