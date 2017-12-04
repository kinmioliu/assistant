#-*-coding:utf-8-*-

DEBUG = True

def DUMP(input):
    if DEBUG:
        print(input)


MML_ERR             = 0
MML_NAME            = 1
MML_FUNC            = 2
MML_ATTENTION       = 3
MML_MARK            = 4

MML_NAME_BEGIN = 'CMD_NAME_BEGIN['
MML_NAME_END = ']CMD_NAME_END'
MML_FUNC_BEGIN = 'CMD_FUNC['
MML_FUNC_END = ']CMD_FUNC'
MML_ATTENTION_BEGIN = 'ATTENTIONS['
MML_ATTENTION_END = ']ATTENTIONS'
MML_MARK_BEGIN = 'MARK['
MML_MARK_END = ']MARK'
