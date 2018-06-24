from itertools import chain
import json
import os
import re
import string
from util import assistant_errcode, conf
from base_assistant.models import FileInfo, ResponsibilityField

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

    def get_filename(self):
        return self.filename

    def get_path(self):
        return self.path

    def get_responsefield(self):
        return self.responsefield

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
            return name
        else:
            return abspath

    def parser_one_line(self, line, record):
        name = self.get_file_or_dir_name(line)
        for responsefield in conf.FILE_PATH_CONF:
            for pathconf in conf.FILE_PATH_CONF[responsefield]:
                pos = line.find(pathconf)
                if pos > -1:
                    record.set_attr(name, "", line[pos:], responsefield)
                    return assistant_errcode.SUCCESS

        pos = line.find(conf.FILE_PATH_ROOT_DIR)
        if (pos > -1):
            record.set_attr(name, "", line[pos:], conf.UNKNOW_RESPONSIBILITY)
        else:
            record.set_attr(name, "", line, conf.UNKNOW_RESPONSIBILITY)
        return assistant_errcode.SUCCESS

    def update_or_create(self, record):
        responsefield_obj = ResponsibilityField.objects.filter(groupname=record.get_responsefield())
        if len(responsefield_obj) == 0:
            return assistant_errcode.INVALID_FILE_INFO_NO_RES

        try:
            obj = FileInfo.objects.get(path=record.get_path())
            is_same = True
            if getattr(obj, 'responsefield').groupname != responsefield_obj[0].groupname:
                is_same = False

            if not is_same:
                setattr(obj, 'responsefield', responsefield_obj[0])
            else:
                return assistant_errcode.DB_SAME
            obj.save()
            return assistant_errcode.DB_UPDATED
        except FileInfo.DoesNotExist:
            obj = FileInfo(filename=record.get_filename(), introduce="", path=record.get_path(), responsefield=responsefield_obj[0])
            obj.save()
            return assistant_errcode.DB_CREATED

        return assistant_errcode.INVALID_FILE_INFO_NO_RES

    def fileter_line_break(self, line):
        if line[len(line)-1] == '\n':
            return line[0:len(line)-1]
        else:
            return line

    def run(self):

        result = dict()
        created_records = list()
        updated_records = list()

        for line in self.lines:
            record = FileRecord(filename = "", introduce = "", path = "", responsefield = "")
            filtered_line = self.fileter_line_break(line);
            ret = self.parser_one_line(filtered_line, record)
            if ret != assistant_errcode.SUCCESS:
               # conf.DUMP( filtered_line + " not find res")
                continue

            ret = self.update_or_create(record)
            if ret == assistant_errcode.DB_SAME:
                conf.DUMP(record.__str__() + " is same")
            elif ret == assistant_errcode.DB_UPDATED:
                updated_records.append(record.__str__())
                conf.DUMP(record.__str__() + " is updated")
            elif ret == assistant_errcode.DB_CREATED:
                created_records.append(record.__str__())
                conf.DUMP(record.__str__() + " is created")

        result['created'] = created_records
        result['updated'] = updated_records

        return result
