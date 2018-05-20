#-*-coding:utf-8-*-
import jieba
from util.conf import *
from base_assistant.models import HashTag

class IndexBuilder:
    def __init__(self):
        self.created_records = 0
        self.updated_records = 0

    def run(self):
        DUMP("Build Index Begin")
        tags = HashTag.objects.all()
        lexicon = dict()
        for tag in tags:
            tag_name = tag.name
            DUMP(tag_name)
            splits = jieba.cut(tag_name)
            for obj in splits:
                DUMP(obj)
                val = lexicon.get(obj)
                if val == None:
                    lexicon[obj] = 1
                else:
                    lexicon[obj] = val + 1
#                lexicon[obj] += 1
#            lexicon[]

        DUMP(lexicon)
        DUMP("Build Index End")
        return 0