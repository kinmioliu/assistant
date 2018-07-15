#-*-coding:utf-8-*-

import jieba

s = u'我想和女朋友一起去北京故宫博物院参观和闲逛。'
s = 'cfg-add-board'
cut = jieba.cut(s)
print(','.join(jieba.cut(s,cut_all = True)))
print(cut)

result = jieba.tokenize(u'自然语言处理非常有用', mode='search')
for tk in result:
    print("%s\t\t start: %d \t\t end:%d" % (tk[0],tk[1],tk[2]))