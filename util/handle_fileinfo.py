from itertools import chain
import json
import os
import re
import string
from util import assistant_errcode, conf

class FileRecord:
    def __init__(self, filename, introduce, path, responsefield):
        self.filename = filename
        self.introduce = introduce
        self.path = path
        self.responsefield = responsefield

    def set_attr(self, filename, introduce, path, responsefield):
        self.filename = filename
        self.introduce = introduce
        self.path = path
        self.responsefield = responsefield

    def __str__(self):
        return self.filename + "path:" + self.path + "res:" + self.responsefield

class FileInfoParser:
    def __init__(self, lines):
        self.lines = lines
        self.linecount = len(lines)

    def parser_one_line(self, line, record):
        for responsefield in conf.FILE_PATH_CONF:
            for pathconf in conf.FILE_PATH_CONF[responsefield]:
                pos = line.find(pathconf)
                conf.DUMP(pos)
                if pos > -1:
                    record.set_attr("", "", line[pos:], responsefield)
                    return assistant_errcode.SUCCESS

        return assistant_errcode.INVALID_MML_FORMAT

    def run(self, records):
        for line in self.lines:
            record = FileRecord(filename = "", introduce = "", path = "", responsefield = "")
            ret = self.parser_one_line(line, record)
            if ret == assistant_errcode.SUCCESS:
                records.append(record)

        return assistant_errcode.SUCCESS
