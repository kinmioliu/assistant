import re
import os
from ctypes import *

tempstr = r"类和对象的定义    面向对象             面向对象是一种程序设计范型，" \
          "  同时也" \
          "   是程 " \
          "             序开发的一种方法。   对象是指类的实例，将对象作为程序的基本单元，将程序和数据封装其中，以提高软件的重用性、灵活性和扩展性。  需要明确的是：C语言是面向过程语言，而C++不是纯粹的面向对象语言，而是基于面向对象的语言，因为C++包含C语言的部分。 "
print(tempstr)
# 1. 将所有的空白字符转换成' '
new_content =  tempstr.replace('\s', ' ').replace('\r\n', ' ').replace('\t', ' ')
# 2. 将连续的空格转换成单个' '
while new_content.find('  ') >= 0:
    new_content = new_content.replace('  ', ' ')

print(new_content)

test = cdll.LoadLibrary(r"F:\pyhton\project\site\assistant\IndexDLL\x64\Debug\IndexDLL.dll")
#test = WinDLL(r"F:\pyhton\project\site\assistant\util\IndexDLL.dll")
print(test)
print(test.add(1,2))

myb = cdll.LoadLibrary(r"F:\pyhton\project\site\assistant\IndexDLL\x64\Debug\IndexDLL.dll")
#test = WinDLL(r"F:\pyhton\project\site\assistant\util\IndexDLL.dll")
print(myb.add(6,2))


HexPattern = r'(\b|\s.)0x[0-9a-fA-F]+(\b|\s.)'
HexPattern = r'(\b|\s.)0x[0-9a-fA-F]+(\b|\s.)'

TestInPut = ['0x124 0x5','0x123a ','0xagag','7899', '  0x13']

for TestElem in TestInPut:
    Match = re.match(HexPattern, TestElem)
    if Match:
        print(Match.group(0))
    else:
        print(TestElem + " Not match")

TestFileInput = ['daga.h', 'dalgjlag.cpp', 'agagkjge.cos', 'agagegag']

for TestElem in TestFileInput:
    if os.path.isfile(TestElem):
        print(TestElem + " is a file")
    else:
        print(TestElem + " Not match")


str1 = 'mslajgajlgjag\n'
str2 = 'gagelgjaige'
comb_s = str1 + str2
print(comb_s)

line = 'MMLBEGIN:[cfg-delay-time1]MMLEND	FUNCBEGIN:[执行延时操作1]FUNCEND	SAMPLEBEGIN:[cfg-delay-time:1]SAMPLEEND	ATTENTIONBEGIN:[无1]ATTENTIONEND	MARKBEGIN:[无1]MARKEND'
print(line)
result = re.findall(r'MMLBEGIN:\[(.+?)\]MMLEND\tFUNCBEGIN:\[(.+?)\]FUNCEND\tSAMPLEBEGIN:\[(.+?)\]SAMPLEEND\tATTENTIONBEGIN:\[(.+?)\]ATTENTIONEND\tMARKBEGIN:\[(.+?)\]MARKEND', line)
print(result)


line = 'WIKILINKBEGIN[http://xgag0.HUAWEI.COM]WIKILINKENDWIKITITLEBEGIN[VxWORKTITLE0]WIKITITLEENDWIKIABSTRACTBEGIN[1d]WIKIABSTRACTENDWIKICLASSESBEGIN[GROUP[KERNEL]FEATURE[VOS]CLASSES[VOS]]WIKICLASSESEND'
#line =       'WIKILINKBEGIN[gageggags]WIKILINKENDWIKITITLEBEGIN[VxWORKTITLE0]WIKITITLEENDWIKIABSTRACTBEGIN[1d]WIKIABSTRACTENDWIKICLASSESBEGIN[dagagsgdd]WIKICLASSESEND'
regex_str = r'WIKILINKBEGIN\[(. +?)\]WIKILINKENDWIKITITLEBEGIN\[(. +?)\]WIKITITLEENDWIKIABSTRACTBEGIN\[(. +?)\]WIKIABSTRACTENDWIKICLASSESBEGIN\[(. +?)\]WIKICLASSESEND'
regex_str = r'(WIKILINKBEGIN\[(. +?)\]WIKILINKENDWIKITITLEBEGIN\[(. +?)\]WIKITITLEENDWIKIABSTRACTBEGIN\[(. +?)\]WIKIABSTRACTENDWIKICLASSESBEGIN\[(. +?)\]WIKICLASSESEND)'
ret =  re.findall(r'WIKILINKBEGIN\[(.+?)\]WIKILINKENDWIKITITLEBEGIN\[(.+?)\]WIKITITLEENDWIKIABSTRACTBEGIN\[(.+?)\]WIKIABSTRACTENDWIKICLASSESBEGIN\[(.+?)\]WIKICLASSESEND', line)
print(ret)

classes_regex = r'GROUP\[(.+?)\]FEATURE\[(.+?)\]classes\[(.+?)\]'
line = 'GROUP[KERNEL]FEATURE[VOS]classes[VOS]'
classes = re.findall(classes_regex, line)
print(classes)