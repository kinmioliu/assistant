//
//  IndexMng.h
//  IndexMng
//
//  Created by 刘进谋 on 2018/6/6.
//  Copyright © 2018年 刘进谋. All rights reserved.
//

#ifndef IndexMng_h
#define IndexMng_h
#include <vector>
#include <map>
#include <set>
#include <algorithm>
#include <iostream>
using namespace std;

class PostingList
{
public:
    double IDF;
    unsigned int DF;
    vector<unsigned int> DocIDList; //
    vector<unsigned int> TFList;
    vector<double> Weight;
    friend ostream& operator<< (ostream & os , const PostingList & Info)
    {
        os << "fk:" << Info.DF << "{" ;
        for (int i = 0; i < Info.TFList.size(); i++)
        {
            os << "<" << Info.DocIDList[i] << "," << Info.TFList[i] << ">,";
        }
        os << "}";
        return os;
    }
};

typedef struct StructResut
{
    unsigned int ResultCnts;
    unsigned int PageCnt;
    unsigned int Result1;
    unsigned int Result2;
	unsigned int Result3;
	unsigned int Result4;
	unsigned int Result5;
	unsigned int Result6;
	unsigned int Result7;
	unsigned int Result8;
	unsigned int Result9;
	unsigned int Result10;
}StructResut, *StructResutlPointer;


// for windows and linux
#ifdef _WIN64

	extern "C" __declspec(dllexport) StructResutlPointer QueryDocIdByTokens(unsigned int Docid1, unsigned int Docid2, unsigned int Docid3, unsigned int Docid4, unsigned int Docid5, unsigned int Docid6, unsigned int Docid7, unsigned int Docid8, unsigned int Docid9, unsigned int Docid10, unsigned int Docid11, unsigned int Docid12, unsigned int Docid13, unsigned int Docid14, unsigned int Docid15, unsigned int Docid16, unsigned int Docid17, unsigned int Docid18, unsigned int Docid19, unsigned int Docid20, unsigned int Page, unsigned int PageSize, unsigned int QueryClass);
	// for dll test
	extern "C" 	__declspec(dllexport) int sum(int a, int b);

#else

	extern "C" StructResutlPointer QueryDocIdByTokens(unsigned int Docid1, unsigned int Docid2, unsigned int Docid3, unsigned int Docid4, unsigned int Docid5, unsigned int Docid6, unsigned int Docid7, unsigned int Docid8, unsigned int Docid9, unsigned int Docid10, unsigned int Docid11, unsigned int Docid12, unsigned int Docid13, unsigned int Docid14, unsigned int Docid15, unsigned int Docid16, unsigned int Docid17, unsigned int Docid18, unsigned int Docid19, unsigned int Docid20, unsigned int Page, unsigned int PageSize, unsigned int QueryClass);
	// for dll test
	extern "C" int sum(int a, int b);

#endif

#endif /* IndexMng_h */
