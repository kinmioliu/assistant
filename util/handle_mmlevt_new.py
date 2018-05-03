#-*-coding:utf-8-*-
from itertools import chain
import json
import os
import re
import string
from util import assistant_errcode, conf
from util.common_parser import CommonRecord, CommonParser
from base_assistant.models import MMLCmdInfo, HashTag, ResponsibilityField, EVTCmdInfo


class MMLRecord(CommonRecord):
    def __init__(self, groupname):
        super(MMLRecord, self).__init__()
        self.group = groupname
        self.name = ''
        self.func = ''
        self.sample = ''
        self.attention = ''
        self.mark = ''

    def set_attrs(self, attrs):
        if len(attrs) != 5:
            return assistant_errcode.INVALID_MML_FORMAT
        return self.set_attr(attrs[0], attrs[1], attrs[2], attrs[3], attrs[4])

    def set_attr(self, name, func, sample, attention, mark):
        self.name = name
        self.func = func
        self.sample = sample
        self.attention = attention
        self.mark = mark

    def update_or_create(self):
        responsefield_obj = ResponsibilityField.objects.filter(groupname=self.group)
        if len(responsefield_obj) == 0:
            return assistant_errcode.INVALID_MML_FORMAT

        defaults = {'cmdname': self.name, 'cmd_func':self.func, 'cmd_sample':self.sample, 'cmd_attention':self.attention, 'cmd_mark':self.mark, 'responsefield':responsefield_obj[0]}

        try:
            obj = MMLCmdInfo.objects.get(cmdname = self.name)
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
        except MMLCmdInfo.DoesNotExist:
            obj = MMLCmdInfo(cmdname=self.name, cmd_func = self.func, cmd_sample = self.sample, cmd_attention = self.attention, cmd_mark = self.mark, responsefield = responsefield_obj[0])
            obj.save()
            hashtag_obj, created = HashTag.objects.get_or_create(name= self.name)
            obj.tags.add(hashtag_obj)
            obj.save()
            return assistant_errcode.DB_CREATED

    def __str__(self):
        return self.name

    def to_module(self):
        return


class EVTRecord(CommonRecord):
    def __init__(self, groupname):
        super(EVTRecord, self).__init__()
        self.group = groupname
        self.name = ''
        self.func = ''
        self.attention = ''
        self.mark = ''

    def set_attrs(self, attrs):
        if len(attrs) != 4 :
            return assistant_errcode.INVALID_MML_FORMAT
        return self.set_attr(attrs[0], attrs[1], attrs[2], attrs[3])

    def set_attr(self, name, func, attention, mark):
        self.name = name
        self.func = func
        self.attention = attention
        self.mark = mark


    def update_or_create(self):
        responsefield_obj = ResponsibilityField.objects.filter(groupname=self.group)
        if len(responsefield_obj) == 0:
            return assistant_errcode.INVALID_MML_FORMAT
        print(self.__str__())
        defaults = {'cmdname': self.name, 'cmd_func':self.func, 'cmd_attention':self.attention, 'cmd_mark':self.mark, 'responsefield':responsefield_obj[0]}
        try:
            obj = EVTCmdInfo.objects.get(cmdname = self.name)
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
        except EVTCmdInfo.DoesNotExist:
            obj = EVTCmdInfo(cmdname=self.name, cmd_func = self.func, cmd_attention = self.attention, cmd_mark = self.mark, responsefield = responsefield_obj[0])
            obj.save()
            hashtag_obj, created = HashTag.objects.get_or_create(name= self.name)
            obj.tags.add(hashtag_obj)
            obj.save()
            return assistant_errcode.DB_CREATED

        return assistant_errcode.DB_CREATED

    def __str__(self):
        return self.name

    def to_module(self):
        return


#WIKILINKBEGIN[http://xgag4.HUAWEI.COM]WIKILINKENDWIKITITLEBEGIN[VxWORKTITLE0]WIKITITLEENDWIKIABSTRACTBEGIN[sg]WIKIABSTRACTENDWIKITAGBEGIN[tag4]WIKITAGENDWIKICLASSESBEGIN[GROUP[KERNEL]FEATURE[VOS]classes[VOS]]WIKICLASSESEND
#WIKILINKBEGIN[http://xgag5.HUAWEI.COM]WIKILINKENDWIKITITLEBEGIN[产品注册差异文档整理-传送软件开发社区（内源&软件能力中心）-3ms知识管理社区]WIKITITLEENDWIKIABSTRACTBEGIN[Summary:框架模块mml和适配层注册产品过多，如RTN产品类型繁多……]WIKIABSTRACTENDWIKITAGBEGIN[MML,适配层]WIKITAGENDWIKICLASSESBEGIN[GROUP[KERNEL]FEATURE[VOS]classes[VOS]]WIKICLASSESEND
MML_IDENTIFIERS = ['MMLBEGIN:[', ']MMLEND\tFUNCBEGIN:[', ']FUNCEND\tSAMPLEBEGIN:[',']SAMPLEEND\tATTENTIONBEGIN:[', ']ATTENTIONEND\tMARKBEGIN:[', ']MARKEND',]
MML_REGEX_STR = r'MMLBEGIN:\[(.+?)\]MMLEND\tFUNCBEGIN:\[(.+?)\]FUNCEND\tSAMPLEBEGIN:\[(.+?)\]SAMPLEEND\tATTENTIONBEGIN:\[(.+?)\]ATTENTIONEND\tMARKBEGIN:\[(.+?)\]MARKEND'

class MMLParser(CommonParser):
    def __init__(self, group, lines):
        super(MMLParser, self).__init__(lines, MML_IDENTIFIERS, MML_REGEX_STR)
        self.group = group

    def init_record(self):
        record = MMLRecord(self.group)
        return record

    def run(self):
        return super(MMLParser, self).run(True)

#EVTBEGIN:[FRAMEMCSP	PER	STATE3]EVTEND	FUNCBEGIN:[跨设备同步协议通道状态改变事件3]FUNCEND	ATTENTIONBEGION:[-]ATTENTIONEND	MARKBEGIN:[-]MARKEND
EVT_IDENTIFIERS = ['EVTBEGIN:[', ']EVTEND\tFUNCBEGIN:[', ']FUNCEND\tATTENTIONBEGION:[',']ATTENTIONEND\tMARKBEGIN:[',']MARKEND',]
EVT_REGEX_STR = r'EVTBEGIN:\[(.+?)\]EVTEND\tFUNCBEGIN:\[(.+?)\]FUNCEND\tATTENTIONBEGION:\[(.+?)\]ATTENTIONEND\tMARKBEGIN:\[(.+?)\]MARKEND'
class EVTParser(CommonParser):
    def __init__(self, group, lines):
        super(EVTParser, self).__init__(lines, EVT_IDENTIFIERS, EVT_REGEX_STR)
        self.group = group

    def init_record(self):
        record = EVTRecord(self.group)
        return record

    def run(self):
        return super(EVTParser, self).run(True)

class MMLEVTParserManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.files = []
        for root, dirs, files in os.walk(file_path):
            for file in files:
                self.files.append(file)
        self.created_records = 0
        self.updated_records = 0

    def AllocParser(self, filename, lines):
        print(filename)
        filename_tokens = filename.split('_')
        if len(filename_tokens) < 2:
            return None

        #匹配group
        group = filename_tokens[0].lower()
        match_group = False
        for groupconf in conf.RESPONSIBILITY_FIELD_CONF:
            if group == groupconf[0]:
                match_group = True
                break
        if match_group == False:
            return None

        filetype = filename_tokens[1]
        if filetype == 'MML':
            return MMLParser(group, lines)
        elif filetype == 'EVT':
            return EVTParser(group, lines)

        return None

    def run(self):
        for file in self.files:
            mmlevtinfo_file = open(self.file_path + file, 'r', encoding='UTF-8')
            lines = mmlevtinfo_file.readlines()
            parser = self.AllocParser(file, lines)
            if parser == None:
                mmlevtinfo_file.close
                return assistant_errcode.INVALID_MML_FORMAT
            result = parser.run()
            mmlevtinfo_file.close()
            conf.DUMP('parser file' + self.file_path + file + ' ' + str(result))
            if result != assistant_errcode.MML_PARSE_SUCCESS:
                return result
            self.created_records += parser.created_records
            self.updated_records += parser.updated_records

        return assistant_errcode.MML_PARSE_SUCCESS
