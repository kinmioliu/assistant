#-*-coding:utf-8-*-
from itertools import chain
import json
import os
import re
import string
from base_assistant.models import MMLCmdInfo
from util import assistant_errcode, conf

class CommonRecord:
    def __init__(self):
        return

    def set_attr(self, attrs):
        return

    def __str__(self):
        return

    def update_or_create(self):
        return


class CommonParser:
    def __init__(self, lines, identifiers, regex_str):
        self.lines = lines
        self.linecount = len(lines)
        self.split_identifiers = identifiers
        self.regex_str = regex_str
        self.updated_records = 0
        self.created_records = 0
        self.same_records = 0
        self.failed_records = []


    #返回第一条记录的起始位置
    """返回值是行号，当没有找到位置时，返回-1"""
    def locate_to_first(self):
        for line in range(self.linecount):
            if self.lines[line].find(self.split_identifiers[0]) >= 0:
                return line
        return assistant_errcode.LOCATE_FIRST_RECORD_ERR

    #返回下一条记录的位置(开始+结束)
    # locate[0]：成功或失败
    # locate[1]：起始行号
    # locate[2]：结束行号
    def get_next_record_location(self, begin):
        locate = dict()
        locate[0] = assistant_errcode.SUCCESS
        locate[1] = begin
        if begin >= self.linecount:
            locate[0] = assistant_errcode.LOCATE_NEXT_RECORD_ERR
            return locate
        if self.lines[begin].find(self.split_identifiers[0]) < 0:
            locate[0] = assistant_errcode.LOCATE_NEXT_RECORD_ERR
            return locate

        for line in range(begin, self.linecount):
            if self.lines[line].find(self.split_identifiers[len(self.split_identifiers) -1]) >= 0:
                locate[2] = line
                return locate

        locate[0] = assistant_errcode.LOCATE_NEXT_RECORD_ERR
        return locate

    def get_record_from_oneline(self, line):
        return re.findall(self.regex_str, line)
    #        return re.findall(r'MMLBEGIN:\[(.+?)\]MMLEND\tFUNCBEGIN:\[(.+?)\]FUNCEND\tSAMPLEBEGIN:\[(.+?)\]SAMPLEEND\tATTENTIONBEGIN:\[(.+?)\]ATTENTIONEND\tMARKBEGIN:\[(.+?)\]MARKEND', self.lines[line])

    def parser_one_record_oneline(self, line):
        if (line >= self.linecount or line < 0):
            return ([])
        return self.get_record_from_oneline(self.lines[line])

    def split(self, begin_coordinate, end_coordinate):
        if begin_coordinate[0] == end_coordinate[0]:
            return self.lines[begin_coordinate[0]][begin_coordinate[1]:end_coordinate[1]]

        record = self.lines[begin_coordinate[0]][begin_coordinate[1]:]
        for index in range(begin_coordinate[0]+1, end_coordinate[0]):
            record = record + self.lines[index]

        record = record + self.lines[end_coordinate[0]][:end_coordinate[1]]
        return record

    def parser_one_record_multiline(self, begin, end):
        comb_line = ''
        for index in range(begin, end + 1):
            comb_line += self.lines[index]
        conf.DUMP(comb_line)
        comb_line = comb_line.replace('\n', '')
        return self.get_record_from_oneline(comb_line)

    #'MMLBEGIN:[cfg-delay-time1]MMLEND	FUNCBEGIN:[执行延时操作1]FUNCEND	SAMPLEBEGIN:[cfg-delay-time:1]SAMPLEEND	ATTENTIONBEGIN:[无1]ATTENTIONEND	MARKBEGIN:[无1]MARKEND',
    def parser_one_record(self, begin, end, record):
        conf.DUMP("parser_record:" + str(begin)+','+str(end))
        result = self.parser_one_record_multiline(begin, end)
        conf.DUMP(result)
        if (len(result) != 1):
            return assistant_errcode.PARSER_RECORD_ERR
        record.set_attrs(result[0])
        return assistant_errcode.SUCCESS

    def init_record(self):
        record = CommonRecord()
        return record

    def run(self, update_or_create_flag):
        curline = self.locate_to_first()
        conf.DUMP("curline" + hex(curline))
        if curline == assistant_errcode.LOCATE_FIRST_RECORD_ERR:
            return assistant_errcode.LOCATE_FIRST_RECORD_ERR
        locate = self.get_next_record_location(begin=curline)

        while locate[1] <= self.linecount and locate[0] == assistant_errcode.SUCCESS:
            record = self.init_record()
            ret = self.parser_one_record(begin=locate[1], end=locate[2], record=record)
            if ret != assistant_errcode.SUCCESS:
                return ret

            if (update_or_create_flag == True):
                ret = record.update_or_create()
                if ret == assistant_errcode.DB_CREATED:
                    self.created_records += 1
                if ret == assistant_errcode.DB_UPDATED:
                    self.updated_records += 1
                if ret == assistant_errcode.DB_SAME:
                    self.same_records += 1

            #指向下一条记录
            locate = self.get_next_record_location(begin=locate[2] + 1)

#        mml_records["mmls"] = records
        return assistant_errcode.SUCCESS
