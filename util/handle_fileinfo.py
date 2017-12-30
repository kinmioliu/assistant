from itertools import chain
import json
import os
import re
import string
from util import assistant_errcode, conf
#from base_assistant.models import FileInfo, ResponsibilityField

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
        return self.filename + "  path:" + self.path + "  res:" + self.responsefield

    def to_module(self):
        responsefield_obj = ResponsibilityField.objects.filter(groupname__icontains=self.responsefield)
        if len(responsefield_obj) == 0:
            return None
        fileinfo_obj = FileInfo.objects.filter(path=self.path)
        if (len(fileinfo_obj) != 0):
            conf.DUMP(self.path + "already exist")
            return None
        return FileInfo(filename=self.filename, introduce="", path=self.path, responsefield=responsefield_obj)

class FileInfoParser:
    def __init__(self, lines):
        self.lines = lines
        self.linecount = len(lines)

    def get_file_or_dir_name(self, abspath):
        pos = abspath.rfind('\\')
        if pos > -1:
            name = abspath[pos+1:]
            conf.DUMP(name)
            return name
        else:
            return abspath

    def parser_one_line(self, line, record):
        for responsefield in conf.FILE_PATH_CONF:
            for pathconf in conf.FILE_PATH_CONF[responsefield]:
                pos = line.find(pathconf)
                conf.DUMP(pos)
                if pos > -1:
                    name = self.get_file_or_dir_name(line)
                    record.set_attr(name, "", line[pos:], responsefield)
                    return assistant_errcode.SUCCESS

        return assistant_errcode.INVALID_MML_FORMAT

    def run(self, records):
        for line in self.lines:
            record = FileRecord(filename = "", introduce = "", path = "", responsefield = "")
            ret = self.parser_one_line(line, record)
            if ret == assistant_errcode.SUCCESS:
                records.append(record)

        return assistant_errcode.SUCCESS
