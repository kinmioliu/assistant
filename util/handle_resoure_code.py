#-*-coding:utf-8-*-
from itertools import chain
import json
import os
import re
import string
from base_assistant.models import ResoureInfo, ResoureInfoInt, ResourceInfoStr, ResourceInfoModule, ResourceInfoRud
from util import assistant_errcode, conf

"""
#cout << filename << "\t" << dec << line << "\t" << #var_name << "\t" << endl
class ResoureInfo(models.Model):
    file = models.ForeignKey("FileInfo")
    line = models.IntegerField()
    name = models.CharField(max_length=30)
    code = models.CharField(max_length=200)
    #备注
    cmd_mark = models.CharField(max_length = 500)
    #所属责任田
    responsefield = models.ManyToManyField("ResponsibilityField", blank=True, null=True)
    #相关问题列表
    solutions = models.ManyToManyField("Solution", null=True)
    #相关链接列表
    out_links = models.ManyToManyField("OuterLink", null=True)

    def __str__(self):
        return self.file + self.name + self.code
        
class ResoureInfoInt(ResoureInfo):
    value = models.IntegerField()

class ResourceInfoStr(ResoureInfo):
    value = models.CharField(max_length = 50)

class ResourceInfoRud(ResoureInfoInt):
    domain = models.CharField(max_length = 30)

class ResourceInfoModule(ResoureInfo):
    introduct = models.CharField(max_length = 500)
    out_link = models.URLField()
    """
class ResoureRecord:
    def __init__(self, file, line, name, code):
        self.file = file
        self.line = line
        self.name = name
        self.code = code

    def set_attr(self, file, line, name, code):
        self.file = file
        self.line = line
        self.name = name
        self.code = code

    def __str__(self):
        return ("[" + self.file + "],["+ self.line +  "],[" + self.name + "],["+self.code + "]")

    def to_module(self):
        return
        #return MMLCmdInfo(cmdname=self.name, cmd_func = self.func, cmd_sample = self.sample, cmd_attention = self.attention, cmd_mark = self.mark, responsefield=responsefield_obj)


class IntResouceRecord(ResoureRecord):
    def __init__(self, file, line, name, code, value):
        super(IntResouceRecord, self).__init__(file, line, name, code)
        self.value = value

    def set_attr(self, file, line, name, code, value):
        super(IntResouceRecord, self).set_attr(file, line, name, code)
        self.value = value

    def to_module(self):
        return ResoureInfoInt(file = self.file, line = self.line, name = self.name, code = self.code, value = self.value)

class RudResouceRecord(IntResouceRecord):
    def __init__(self, file, line, name, code, value, domain):
        super(IntResouceRecord, self).__init__(file, line, name, code, value)
        self.domain = domain

    def set_attr(self, file, line, name, code, value, domain):
        super(IntResouceRecord, self).set_attr(file, line, name, code, value)
        self.domain = domain

    def to_module(self):
        return ResourceInfoRud(file = self.file, line = self.line, name = self.name, code = self.code, value = self.value, domain = self.domain)

class ModuleResouceRecord(IntResouceRecord):
    def __init__(self, file, line, name, code, value):
        super(IntResouceRecord, self).__init__(file, line, name, code, value)

    def to_module(self):
        return ResourceInfoModule(file = self.file, line = self.line, name = self.name, code = self.code, value = self.value, introduct = '')


class StrResouceRecord(ResoureRecord):
    def __init__(self, file, line, name, code, value):
        super(ResoureRecord, self).__init__(file, line, name, code)
        self.value = value

    def set_attr(self, file, line, name, code, value):
        super(ResoureRecord, self).set_attr(file, line, name, code)
        self.value =  value

    def to_module(self):
        return ResourceInfoModule(file = self.file, line = self.line, name = self.name, code = self.code, value = self.value, introduct = '')

class ResourceParser:

    def __init__(self, lines):
        self.lines = lines
        self.len = len(lines)

    #这个函数需要不停优化
    def AllocResourceObj(self, ResourceFileName, value):
        if ResourceFileName.find('rud'):
            return RudResouceRecord(ResourceFileName, 0, '', '', 0, '')
        if ResourceFileName == 'ne_modid':
            return ModuleResouceRecord(ResourceFileName, 0, '', '', 0)
        if value.isdigit():
            return IntResouceRecord(ResourceFileName, 0, '', '', 0)
        else:
            return StrResouceRecord(ResourceFileName, 0, '', '', '')

        return None

    def parser_one_record_from_oneline(self, line, record):
        result = line.split('|')
        conf.DUMP(result)
        if len(result) != conf.RESOURCE_FILE_TOKENS:
            return conf.RESOURCE_PARSE_FAIL
        ResoureRecord = self.AllocResourceObj(result[0], result[3])
        



        return assistant_errcode.SUCCESS

    def Parser(self):
        for line in self.lines:
            self.parser_one_record_from_oneline(line = line, record='')
        return conf.RESOURCE_PARSE_SUCCESS



class ResourceParserManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.files = []
        for root, dirs, files in os.walk(file_path):
            for file in files:
                self.files.append(file)

    def run(self):
        for file in self.files:
            ResourceFile = open(self.file_path + file, 'r', encoding='UTF-8')
            lines = ResourceFile.readlines()
            parser = ResourceParser(lines=lines)
            result = parser.Parser()
            ResourceFile.close()
            conf.DUMP('parser file' + self.file_path + file + ' ' + str(result))
            if result != conf.RESOURCE_PARSE_SUCCESS:
                return result


