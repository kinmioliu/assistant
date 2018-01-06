#from  util.handle_mml import MMLParser
from util.handle_fileinfo import FileInfoParser
# lines = ['CMD-NAME-BEGIN[cfg-delay-time1]CMD-NAME-END	CMD_FUNC[执行延时操作1]CMD_FUNC	ATTENTIONS[无1]ATTENTIONS	MARK[无1]MARK',
# '',
# '',
#          ]
#
# lines2 = [
# 'MMLBEGIN:[cfg-delay-time1]MMLEND	FUNCBEGIN:[执行延时操作1]FUNCEND	SAMPLEBEGIN:[cfg-delay-time:1]SAMPLEEND	ATTENTIONBEGIN:[无1]ATTENTIONEND	MARKBEGIN:[无1]MARKEND',
# 'MMLBEGIN:[cfg-delay-time2]MMLEND	FUNCBEGIN:[执行延时操作2]FUNCEND	SAMPLEBEGIN:[cfg-delay-time:2]SAMPLEEND	ATTENTIONBEGIN:[无2]ATTENTIONEND	MARKBEGIN:[无2]MARKEND',
# 'MMLBEGIN:[cfg-delay-time3]MMLEND	FUNCBEGIN:[执行延时操作3]FUNCEND	SAMPLEBEGIN:[cfg-delay-time:3]SAMPLEEND	ATTENTIONBEGIN:[无3]ATTENTIONEND	MARKBEGIN:[无3]MARKEND',
# 'MMLBEGIN:[cfg-delay-time4]MMLEND	FUNCBEGIN:[执行延时操作4]FUNCEND	SAMPLEBEGIN:[cfg-delay-time:4]SAMPLEEND	ATTENTIONBEGIN:[无4]ATTENTIONEND	MARKBEGIN:[无4]MARKEND',
# 'MMLBEGIN:[cfg-delay-time5]MMLEND	FUNCBEGIN:[执行延时操作5]FUNCEND	SAMPLEBEGIN:[cfg-delay-time:5]SAMPLEEND	ATTENTIONBEGIN:[无5]ATTENTIONEND	MARKBEGIN:[无5]MARKEND',
# 'MMLBEGIN:[cfg-delay-time6]MMLEND	FUNCBEGIN:[执行延时操作6]FUNCEND	SAMPLEBEGIN:[cfg-delay-time:6]SAMPLEEND	ATTENTIONBEGIN:[无6]ATTENTIONEND	MARKBEGIN:[无6]MARKEND',
# 'MMLBEGIN:[cfg-delay-time7]MMLEND	FUNCBEGIN:[执行延时操作7]FUNCEND	SAMPLEBEGIN:[cfg-delay-time:7]SAMPLEEND	ATTENTIONBEGIN:[无7]ATTENTIONEND	MARKBEGIN:[无7]MARKEND',
# 'MMLBEGIN:[cfg-delay-time8]MMLEND	FUNCBEGIN:[执行延时操作8]FUNCEND	SAMPLEBEGIN:[cfg-delay-time:8]SAMPLEEND	ATTENTIONBEGIN:[无8]ATTENTIONEND	MARKBEGIN:[无8]MARKEND',
# 'MMLBEGIN:[cfg-delay-time9]MMLEND	FUNCBEGIN:[执行延时操作9]FUNCEND	SAMPLEBEGIN:[cfg-delay-time:9]SAMPLEEND	ATTENTIONBEGIN:[无9]ATTENTIONEND	MARKBEGIN:[无9]MARKEND',
# 'MMLBEGIN:[cfg-delay-time10]MMLEND	FUNCBEGIN:[执行延时操作10]FUNCEND	SAMPLEBEGIN:[cfg-delay-time:10]SAMPLEEND	ATTENTIONBEGIN:[无10]ATTENTIONEND	MARKBEGIN:[无10]MARKEND',
# 'MMLBEGIN:[cfg-delay-time11]MMLEND	FUNCBEGIN:[执行延时操作11]FUNCEND	SAMPLEBEGIN:[cfg-delay-time:11]SAMPLEEND	ATTENTIONBEGIN:[无11]ATTENTIONEND	MARKBEGIN:[无11]MARKEND',
# 'MMLBEGIN:[cfg-delay-time12]MMLEND	FUNCBEGIN:[执行延时操作12]FUNCEND	SAMPLEBEGIN:[cfg-delay-time:12]SAMPLEEND	ATTENTIONBEGIN:[无12]ATTENTIONEND	MARKBEGIN:[无12]MARKEND',
# 'MMLBEGIN:[cfg-delay-time13]MMLEND	FUNCBEGIN:[执行延时操作13]FUNCEND	SAMPLEBEGIN:[cfg-delay-time:13]SAMPLEEND	ATTENTIONBEGIN:[无13]ATTENTIONEND	MARKBEGIN:[无13]MARKEND',
# 'MMLBEGIN:[cfg-delay-time14]MMLEND	FUNCBEGIN:[执行延时',
#     '政到是d',
# '操作14]FUNCEND	SAMPLEBEGIN:[cfg-delay-time:14]SAMPLEEND	ATTENTIONBEGIN:[无14]ATTENTIONEND	MARKBEGIN:[无14]MARKEND',
# 'MMLBEGIN:[cfg-delay-time15]MMLEND	FUNCBEGIN:[执行延时操作15]FUNCEND	SAMPLEBEGIN:[cfg-delay-time:15]SAMPLEEND	ATTENTIONBEGIN:[无15]ATTENTIONEND	MARKBEGIN:[无15]MARKEND',
# 'MMLBEGIN:[cfg-delay-time16]MMLEND	FUNCBEGIN:[执行延时操作16]FUNCEND	SAMPLEBEGIN:[cfg-delay-time:16]SAMPLEEND	ATTENTIONBEGIN:[无16]ATTENTIONEND	MARKBEGIN:[无16]MARKEND',
# 'MMLBEGIN:[cfg-delay-time17]MMLEND	FUNCBEGIN:[执行延时操作17]FUNCEND	SAMPLEBEGIN:[cfg-delay-time:17]SAMPLEEND	ATTENTIONBEGIN:[无17]ATTENTIONEND	MARKBEGIN:[无17]MARKEND',
# 'MMLBEGIN:[cfg-delay-time18]MMLEND	FUNCBEGIN:[执行延时操作18]FUNCEND	SAMPLEBEGIN:[cfg-delay-time:18]SAMPLEEND	ATTENTIONBEGIN:[无18]ATTENTIONEND	MARKBEGIN:[无18]MARKEND',
# 'MMLBEGIN:[cfg-delay-time19]MMLEND	FUNCBEGIN:[执行延时操作19]FUNCEND	SAMPLEBEGIN:[cfg-delay-time:19]SAMPLEEND	ATTENTIONBEGIN:[无19]ATTENTIONEND	MARKBEGIN:[无19]MARKEND',
# 'MMLBEGIN:[cfg-delay-time20]MMLEND	FUNCBEGIN:[执行延',
# '时操作测试20]FUNCEND	SAMPLEBEGIN:[cfg-delay-time:20]SAMPLEEND	ATTENTIONBEGIN:[无特殊测试2',
#     '大家'
# '20]ATTENTIONEND	MARKBEGIN:[无特殊',
#     '假装',
#     '塑料加工',
#     'da\dg',
#     '测试20]MARKEND',
# ]
#
# def testref(l):
#     l.append(1)
#     l.append(2)
#
# test = list()
# testref(test)
# print(test)
# print("testend")
#
# print(1)
# parser = MMLParser(lines = lines2)
# mml_records = list()
# parser.run(mml_records)
# print(mml_records)
# for mml in mml_records:
#     print(str(mml))

#测试资源文件
files = [
    'F:\Code\llvm\llvm\\bindings',
    'llvm\llvm\docs\\test1',
    'F:llvm\llvm\docs\_static\\test2',
    'llvm\llvm\docs\_themes\dlagla3',
    'llvm\llvm\docs\_themes\dlagla4.txt',
    'F:llvm\llvm\docs\_static\eeeest2.h',
]

fileinfo_parser = FileInfoParser(lines=files)
file_records = list()
fileinfo_parser.run(file_records)
for fileinfo in file_records:
    print(str(fileinfo))

mode = {'name':'frame'}
defa = {'introduct':'daga'}
mode.update(defa)
print(mode)
