#-*-coding:utf-8-*-
from itertools import chain
import json
import os
import re
import string
from util import assistant_errcode, conf

class MMLRecord:
    def __init__(self, name, func, attention, sample, mark):
        self.name = name
        self.func = func
        self.sample = sample
        self.attention = attention
        self.mark = mark

    def set_attr(self, name, func, sample, attention, mark):
        self.name = name
        self.func = func
        self.sample = sample
        self.attention = attention
        self.mark = mark

    def __str__(self):
        return ("[" + self.name + "],["+ self.func +  "],[" + self.sample + "],["+self.attention + "],["+self.mark+"]")

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
        return re.findall(r'MMLBEGIN:\[(.+?)\]MMLEND\tFUNCBEGIN:\[(.+?)\]FUNCEND\tSAMPLEBEGIN:\[(.+?)\]SAMPLEEND\tATTENTIONBEGIN:\[(.+?)\]ATTENTIONEND\tMARKBEGIN:\[(.+?)\]MARKEND', self.lines[line])

    def split(self, begin_coordinate, end_coordinate):
        if begin_coordinate[0] == end_coordinate[0]:
            return self.lines[begin_coordinate[0]][begin_coordinate[1]:end_coordinate[1]]

        record = self.lines[begin_coordinate[0]][begin_coordinate[1]:]
        for index in range(begin_coordinate[0]+1, end_coordinate[0]):
            record = record + self.lines[index]

        record = record + self.lines[end_coordinate[0]][:end_coordinate[1]]
        return record

    # 'MMLBEGIN:[cfg-delay-time20]MMLEND	FUNCBEGIN:[执行延',
    # '时操作测试20]FUNCEND	SAMPLEBEGIN:[cfg-delay-time:20]SAMPLEEND	ATTENTIONBEGIN:[无特殊测试2',
    # '20]ATTENTIONEND	MARKBEGIN:[无特殊测试20]MARKEND',
    def parser_one_record_multiline(self, begin, end, record):
        #TODO 重复度太高，需要适当优化
        begin_coordinate = [0, 0]
        end_coordinate = [0, 0]
#        record = list()
        conf.DUMP("parser_one_record_multiline" + str(begin) + str(end))

        state = conf.MML_NAME_BEGIN
        pre_row = begin
        row = begin

        while ((row <= end) and (state != conf.MML_PARSE_END)):
            conf.DUMP("cur row:" + str(row) + state)
            if state == conf.MML_NAME_BEGIN:
                begin_col = self.lines[row].find(conf.MML_NAME_BEGIN)
                if begin_col != -1:
                    begin_coordinate[0] = row
                    begin_coordinate[1] = begin_col + len(conf.MML_NAME_BEGIN)
                    state = conf.MML_NAME_END
                    continue
                row += 1

            if state == conf.MML_NAME_END:
                end_col = self.lines[row].find(conf.MML_NAME_END)
                if end_col != -1:
                    end_coordinate[0] = row
                    end_coordinate[1] = end_col
                    state = conf.MML_FUNC_BEGIN
                    record.append(self.split(begin_coordinate, end_coordinate))
                    conf.DUMP(record)
                    continue
                row += 1

            if state == conf.MML_FUNC_BEGIN:
                begin_col = self.lines[row].find(conf.MML_FUNC_BEGIN)
                if begin_col != -1:
                    begin_coordinate[0] = row
                    begin_coordinate[1] = begin_col + len(conf.MML_FUNC_BEGIN)
                    state = conf.MML_FUNC_END
                    continue
                row += 1

            if state == conf.MML_FUNC_END:
                end_col = self.lines[row].find(conf.MML_FUNC_END)
                if end_col != -1:
                    end_coordinate[0] = row
                    end_coordinate[1] = end_col
                    state = conf.MML_SAMPLE_BEGIN
                    record.append(self.split(begin_coordinate, end_coordinate))
                    conf.DUMP(record)
                    continue
                row += 1

            if state == conf.MML_SAMPLE_BEGIN:
                begin_col = self.lines[row].find(conf.MML_SAMPLE_BEGIN)
                if begin_col != -1:
                    begin_coordinate[0] = row
                    begin_coordinate[1] = begin_col + len(conf.MML_SAMPLE_BEGIN)
                    state = conf.MML_SAMPLE_END
                    continue
                row += 1

            if state == conf.MML_SAMPLE_END:
                end_col = self.lines[row].find(conf.MML_SAMPLE_END)
                if end_col != -1:
                    end_coordinate[0] = row
                    end_coordinate[1] = end_col
                    state = conf.MML_ATTENTION_BEGIN
                    record.append(self.split(begin_coordinate, end_coordinate))
                    conf.DUMP(record)
                    continue
                row += 1

            if state == conf.MML_ATTENTION_BEGIN:
                begin_col = self.lines[row].find(conf.MML_ATTENTION_BEGIN)
                conf.DUMP("attention" + str(begin_col))
                if begin_col != -1:
                    begin_coordinate[0] = row
                    begin_coordinate[1] = begin_col + len(conf.MML_ATTENTION_BEGIN)
                    state = conf.MML_ATTENTION_END
                    continue
                row += 1

            if state == conf.MML_ATTENTION_END:
                end_col = self.lines[row].find(conf.MML_ATTENTION_END)
                conf.DUMP("attention" + str(begin_col))
                if end_col != -1:
                    end_coordinate[0] = row
                    end_coordinate[1] = end_col
                    state = conf.MML_MARK_BEGIN
                    record.append(self.split(begin_coordinate, end_coordinate))
                    conf.DUMP(record)
                    continue
                row += 1
            if state == conf.MML_MARK_BEGIN:
                begin_col = self.lines[row].find(conf.MML_MARK_BEGIN)
                if begin_col != -1:
                    begin_coordinate[0] = row
                    begin_coordinate[1] = begin_col + len(conf.MML_MARK_BEGIN)
                    state = conf.MML_MARK_END
                    continue
                row += 1

            if state == conf.MML_MARK_END:
                end_col = self.lines[row].find(conf.MML_MARK_END)
                if end_col != -1:
                    end_coordinate[0] = row
                    end_coordinate[1] = end_col
                    state = conf.MML_PARSE_END
                    record.append(self.split(begin_coordinate, end_coordinate))
                    conf.DUMP(record)
                    continue
                row += 1

        conf.DUMP(record)
        if state != conf.MML_PARSE_END:
            return assistant_errcode.INVALID_MML_FORMAT

        return assistant_errcode.SUCCESS

    #'MMLBEGIN:[cfg-delay-time1]MMLEND	FUNCBEGIN:[执行延时操作1]FUNCEND	SAMPLEBEGIN:[cfg-delay-time:1]SAMPLEEND	ATTENTIONBEGIN:[无1]ATTENTIONEND	MARKBEGIN:[无1]MARKEND',
    def parser_one_record(self, begin, end, record):
        conf.DUMP("parser_record:" + str(begin)+','+str(end))
        if (begin == end):
            result = self.parser_one_record_oneline(begin)
            conf.DUMP(result)
            #TODO 这个地方实现不够好
            if (len(result) != 1 ):
                return assistant_errcode.INVALID_MML_FORMAT
            record.set_attr(result[0][0], result[0][1], result[0][2], result[0][3], result[0][4])
            conf.DUMP(str(record))
        else:
            tmp_record = list()
            result = self.parser_one_record_multiline(begin, end, tmp_record)
            if (result != assistant_errcode.SUCCESS):
                return result
            record.set_attr(tmp_record[0], tmp_record[1], tmp_record[2], tmp_record[3], tmp_record[4])
            conf.DUMP(str(record))

        return assistant_errcode.SUCCESS

    def run(self, records):
        curline = self.location_to_first()
        conf.DUMP("curline" + hex(curline))
        if curline == assistant_errcode.INVALID_MML_FILE:
            return assistant_errcode.INVALID_MML_FILE

        locate = self.get_next_mml(begin=curline)
        conf.DUMP(locate)
        #records = list()
        while locate[1] <= self.linecount and locate[0] == assistant_errcode.SUCCESS:
            record = MMLRecord(name="", func="", sample="", attention="", mark="")
            ret = self.parser_one_record(begin=locate[1], end=locate[2], record=record)
            if ret != assistant_errcode.SUCCESS and ret != assistant_errcode.MML_TO_DO:
                return ret
            if ret == assistant_errcode.SUCCESS:
                records.append(record)
            #指向下一条记录
            locate = self.get_next_mml(begin=locate[2] + 1)

#        mml_records["mmls"] = records
        return assistant_errcode.SUCCESS

