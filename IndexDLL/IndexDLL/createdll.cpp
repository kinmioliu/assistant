//#pragma execution_character_set("utf-8")

#include"stdafx.h"  //注意不要忘了添加这个头文件
#include <iostream>
#include <map>
#include <set>
#include <vector>
#include <stdarg.h>
#include <string>
#include <fstream>
#include <regex>
using namespace std;

#define DLLEXPORT extern "C" __declspec(dllexport)
DLLEXPORT int __stdcall add(int a, int b) {
	return a + b;
}

// token|count|<docid,fk>,<docid,fk>,<docid,fk>

class IndexInfo
{
public:
	unsigned int fk;
	vector<unsigned int> docid;
	vector<unsigned int> docfk;
	friend ostream& operator<< (ostream & os, const IndexInfo & Info)
	{
		os << "fk:" << Info.fk << "{";
		for (int i = 0; i < Info.docfk.size(); i++)
		{
			os << "<" << Info.docid[i] << "," << Info.docfk[i] << ">,";
		}
		os << "}";
		return os;
	}
};


static map<string, IndexInfo> Index;

class IndexInitializer
{
public:
	static IndexInfo AllocIndexInfo(int fk, int count, ...)
	{
		va_list args;
		va_start(args, count);
		IndexInfo info;
		info.fk = fk;
		for (int i = 0; i < count; i += 2)
		{
			info.docid.push_back(va_arg(args, unsigned int));
			info.docfk.push_back(va_arg(args, unsigned int));
		}
		va_end(args);
		return info;
	}

	IndexInitializer()
	{
		static int CallCount = 0;
		Index["axxxx"] = AllocIndexInfo(4, 8, 1, 2, 3, 4, 5, 6, 7, 8);
		Index["cxxxx"] = AllocIndexInfo(3, 6, 3, 4, 5, 6, 7, 8);
		Index["bxxxx"] = AllocIndexInfo(3, 6, 5, 3, 5, 6, 7, 8);
		cout << "init Index Called :" << CallCount << " times" << endl;
		CallCount++;
	}
};

static IndexInitializer init;

#define DLLEXPORT extern "C" __declspec(dllexport)
DLLEXPORT int __stdcall sum(int a, int b) {
	return a + b;
}

#define DLLEXPORT extern "C" __declspec(dllexport)
DLLEXPORT unsigned int __stdcall UpdateOrCreateIndexInfo(char * Token, int len, unsigned int DocID)
{
	char * tmpstr;
	cout << "hello\n";
	for (int i = 0; i< len * 2; i++)
		cout << Token[i];
	cout << endl;
//	cout << Token << endl;
	cout << len << endl;
	cout << DocID << endl;
	cout << "C++ end\n";
/*
	for (int i = 0; i< len * 2; i++)
		cout << Token[i];
	cout << endl;

	cout << "token:" << Token << " docid:" << DocID << endl;
	cout << "hello\n";
*/
	return 0;
}

unsigned int UpdateOrCreateIndexInfo(string Line)
{
	string dict;
	string fk;
	string docid;
	regex DictRegex("{.*}{.*}{.*}");
	smatch MatchResult;
	if (regex_match(Line, MatchResult, DictRegex))
	{
		cout << "match" << endl;
	}
	return 0;
}

#define DLLEXPORT extern "C" __declspec(dllexport)
DLLEXPORT unsigned int __stdcall InitIndexInfoFromFile()
{
	string line;
	ifstream dict_txt;
//	dict_txt.open("F:\\pyhton\\project\\site\\assistant\\static\\upload\\stopwords\\tds_stopwords_list.txt");
	dict_txt.open("F:\\pyhton\\project\\site\\assistant\\static\\upload\\stopwords\\dict.txt");
	while (!dict_txt.eof())
	{
		dict_txt >> line;
		cout << line << endl;
	}
	dict_txt.close();
	return 0;
}

