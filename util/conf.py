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

ResponsibilityField
RESPONSIBILITY_FIELD_CONF =
{
    ['frame','https://baike.baidu.com/item/FRAME/1867206?fr=aladdin','chenxin223391'],
    ['srv','https://baike.baidu.com/item/SRV','chenxin223391'],
    ['ker','https://baike.baidu.com/item/内核','杨发森'],
    ['app','https://baike.baidu.com/item/手机软件/7973966?fromtitle=APP&fromid=6133292','fengxun'],
    ['com','https://baike.baidu.com/item/com/5662997','zhangkang'],
    ['libm','https://baike.baidu.com/item/FRAME/1867206?fr=aladdin','chenxin223391'],
    ['lim','https://baike.baidu.com/item/lim','chenxin223391'],
    ['l1','https://baike.baidu.com/item/FRAME/1867206?fr=aladdin','chenxin223391'],
    ['l2','https://baike.baidu.com/item/FRAME/1867206?fr=aladdin','chenxin223391'],

    ['pkt','https://baike.baidu.com/item/FRAME/1867206?fr=aladdin','chenxin223391'],
}

#责任田
class ResponsibilityField(models.Model):
    groupname = models.CharField(max_length=50, unique=True)
    introduce = models.URLField()
    plname = models.CharField(max_length=50)