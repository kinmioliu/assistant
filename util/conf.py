#-*-coding:utf-8-*-

DEBUG = True

def DUMP(input):
    if DEBUG:
        print(input)


MML_ERR             = 0
MML_NAME            = 1
MML_FUNC            = 2
MML_SAMPLE          = 3
MML_ATTENTION       = 4
MML_MARK            = 5

MML_NAME_BEGIN = 'MMLBEGIN:['
MML_NAME_END = ']MMLEND'
MML_FUNC_BEGIN = 'FUNCBEGIN:['
MML_FUNC_END = ']FUNCEND'
MML_SAMPLE_BEGIN = 'SAMPLEBEGIN:['
MML_SAMPLE_END = ']SAMPLEEND'
MML_ATTENTION_BEGIN = 'ATTENTIONBEGIN:['
MML_ATTENTION_END = ']ATTENTIONEND'
MML_MARK_BEGIN = 'MARKBEGIN:['
MML_MARK_END = ']MARKEND'
MML_PARSE_END = 'END'

FILE_PATH_CONF = {
    'frame': [
              'llvm\llvm\docs\_static',],
    'ker':['llvm\llvm\docs\_themes',
           'llvm\llvm\docs\Proposals',],
    'com':['llvm\llvm\lib\CodeGen',
           'llvm\llvm\lib\Fuzzer',],
}
