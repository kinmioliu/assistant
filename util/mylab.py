import re
import os

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