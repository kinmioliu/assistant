#-*-coding:utf-8-*-
from itertools import chain
import json
import os
import re
import string
from util import assistant_errcode, conf

class MMLRecord:
    def __init__(self, name, func, attention, mark):
        self.name = name
        self.func = func
        self.attention = attention
        self.mark = mark

    def set_attr(self, name, func, attention, mark):
        self.name = name
        self.func = func
        self.attention = attention
        self.mark = mark

    def __str__(self):
        return ("[" + self.name + "],["+ self.func + "],["+self.attention + "],["+self.mark+"]")

    def to_module(self):
        return


class MMLParser:

    def __init__(self, lines):
        self.lines = lines
        self.linecount = len(lines)

    #返回第一条MML的起始位置
    def location_to_first(self):
        for line in range(self.linecount):
            if self.lines[line].find(conf.MML_NAME_BEGIN) >= 0:
                return line
        return assistant_errcode.INVALID_MML_FILE

    #返回下一条MML的起始位置
    def get_next_mml(self, begin):
        locate = dict()
        locate[0] = assistant_errcode.SUCCESS
        locate[1] = begin

        if begin > self.linecount:
            locate[0] == assistant_errcode.INVALID_MML_FORMAT
            return locate
        for line in range(begin, self.linecount):
            if self.lines[line].find(conf.MML_MARK_END) >= 0:
                locate[2] = line
                return locate

        locate[0] = assistant_errcode.INVALID_MML_FORMAT
        return locate

    def parser_one_record_oneline(self, line):
        return re.findall(r'CMD_NAME_BEGIN\[(.+?)\]CMD_NAME_END\tCMD_FUNC\[(.+?)\]CMD_FUNC\tATTENTIONS\[(.+?)\]ATTENTIONS\tMARK\[(.+?)\]MARK', self.lines[line])

    def parser_one_record_multiline(self, begin, end):
        # TODO 待实现
        return assistant_errcode.MML_TO_DO

    #'CMD-NAME-BEGIN[cfg-delay-time9]CMD-NAME-END	CMD_FUNC[执行延时操作9]CMD_FUNC	ATTENTIONS[无9]ATTENTIONS	MARK[无9]MARK',
    def parser_one_record(self, begin, end, record):
        conf.DUMP("parser_record:" + str(begin)+','+str(end))
        if (begin == end):
            result = self.parser_one_record_oneline(begin)
            conf.DUMP(result)
            #TODO 这个地方实现不够好
            if (len(result) != 1 ):
                return assistant_errcode.INVALID_MML_FORMAT
            record.set_attr(result[0][0], result[0][1], result[0][2], result[0][3])
            conf.DUMP(str(record))
        else:
            self.parser_one_record_multiline(begin, end)
            return assistant_errcode.MML_TO_DO

        return assistant_errcode.SUCCESS

    def run(self, mml_records):
        curline = self.location_to_first()
        conf.DUMP("curline" + hex(curline))
        if curline == assistant_errcode.INVALID_MML_FILE:
            return assistant_errcode.INVALID_MML_FILE

        locate = self.get_next_mml(begin=curline)
        conf.DUMP(locate)
        records = list()
        while locate[1] <= self.linecount and locate[0] == assistant_errcode.SUCCESS:
            record = MMLRecord(name="", func="", attention="", mark="")
            ret = self.parser_one_record(begin=locate[1], end=locate[2], record=record)
            if ret != assistant_errcode.SUCCESS and ret != assistant_errcode.MML_TO_DO:
                return ret
            if ret == assistant_errcode.SUCCESS:
                records.append(record)
            #指向下一条记录
            locate = self.get_next_mml(begin=locate[2] + 1)

        mml_records["mmls"] = records
        return assistant_errcode.SUCCESS

