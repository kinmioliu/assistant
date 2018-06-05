
#include <iostream>
#include <map>
#include <set>
#include <vector>
using namespace std;
#ifdef __cplusplus
extern "C" {
#endif
#include "IndexMng.h"

#ifdef __cplusplus
}
#endif

// tokenid|count|<docid,fk>,<docid,fk>,<docid,fk>

class IndexInfo
{
public:
    unsigned int fk;
    vector<unsigned int> docid;
    vector<unsigned int> docfk;
    friend ostream& operator<< (ostream & os , const IndexInfo & Info)
    {
        os << "fk:" << Info.fk << "{" ;
        for (int i = 0; i < Info.docfk.size(); i++)
        {
            os << "<" << Info.docid[i] << "," << Info.docfk[i] << ">,";
        }
        os << "}";
        return os;
    }
};


static map<unsigned int, IndexInfo> Index;

class IndexInitializer
{
public:
    static IndexInfo AllocIndexInfo(int fk, int count, ...)
    {
        va_list args;
        va_start(args, count);
        IndexInfo info;
        info.fk = fk;
        for (int i = 0; i < count; i+=2)
        {
            info.docid.push_back(va_arg(args, unsigned int));
            info.docfk.push_back(va_arg(args, unsigned int));
        }
        va_end(args);
        return info;
    }
    
    static void InitializeGroup1()
    {
        Index[5] = AllocIndexInfo(4,8,1,2,3,4,5,6,7,1);
        Index[6] = AllocIndexInfo(3,6,3,4,5,6,7,3);
        Index[3] = AllocIndexInfo(3,6,5,3,5,6,7,8);
    }
    
    static void InitializeGroup2()
    {
        Index[4] = AllocIndexInfo(4,8,1,2,3,4,5,6,7,1);
        Index[8] = AllocIndexInfo(3,6,3,4,5,6,7,2);
        Index[168] = AllocIndexInfo(3,6,5,3,5,6,7,1);
    }
    
    
    IndexInitializer()
    {
        InitializeGroup1();
        InitializeGroup2();
    }
};



static IndexInitializer init;

typedef pair<unsigned int, unsigned int> PAIR;
int compare(const PAIR& x, const PAIR& y)
{
    return  y.second < x.second;
}


int QueryDocIdByTokensImpl(vector<unsigned int> &Tokens, unsigned int Page, unsigned int PageSize,unsigned int &ResultCnts, vector<unsigned int> &Result)
{
    //容器中始终保存最大的这个值

    map<unsigned int, unsigned int> DocidScores;
    //1. 分别查出每个Token的索引信息
    //2. 分析权重信息
    //3. 按照得分高者进行排序，
    //4. 假设Tokens为4&5，那么Tokens
    //5. 求所有索引信息的并集。
    vector<unsigned int>::iterator TokenIter = Tokens.begin();
    for (; TokenIter != Tokens.end(); TokenIter++)
    {
        map<unsigned int, IndexInfo>::iterator IndexIter = Index.find(*TokenIter);
        if (IndexIter == Index.end())
        {
            continue;
        }
        //命中
        unsigned int TmpDocId;
        for (int i = 0; i < IndexIter->second.docid.size(); i++ )
        {
            TmpDocId = IndexIter->second.docid[i];
            //计分算法V1，根据命中的数量来计算
            DocidScores[TmpDocId] += 1 * IndexIter->second.docfk[i];
        }
    }
    map<unsigned int, unsigned int>::iterator DocidScoreResult = DocidScores.begin();
    for (; DocidScoreResult != DocidScores.end(); DocidScoreResult++)
    {
        cout << DocidScoreResult->first << ":" << DocidScoreResult->second << endl;
    }

    //打印结果
    //按照得分高者进行排序
    cout << "sorted by score result\n";
    vector<PAIR> ScoreDocidVec(DocidScores.begin(), DocidScores.end());
    sort(ScoreDocidVec.begin(), ScoreDocidVec.end(), compare);
    for (int i = 0 ; i < ScoreDocidVec.size(); i++)
    {
        cout << ScoreDocidVec[i].first << ":" << ScoreDocidVec[i].second << endl;
    }

    ResultCnts = ScoreDocidVec.size();

    //提取出对应Page的数据
    unsigned int ResultSize = ScoreDocidVec.size();
    unsigned int ResultIndex = PageSize * Page;
    unsigned int ResultIndexEnd = ResultIndex + PageSize;
    for (; ResultIndex < ResultSize && ResultIndex < ResultIndexEnd ; ResultIndex++)
    {
        Result.push_back(ScoreDocidVec[ResultIndex].first);
    }
    return 0;
}
/*
struct StructResut
{
    unsigned int ResultCnts;
    unsigned int PageCnt;
    unsigned int Result1;
    unsigned int Result2;
};

int QueryDocIdByTokens(unsigned int Docid1, unsigned int Docid2, unsigned int Docid3, unsigned int Docid4, unsigned int Docid5, unsigned int Docid6, unsigned int Docid7, unsigned int Docid8, unsigned int Docid9, unsigned int Docid10, unsigned int Docid11, unsigned int Docid12, unsigned int Docid13, unsigned int Docid14, unsigned int Docid15, unsigned int Docid16, unsigned int Docid17, unsigned int Docid18, unsigned int Docid19, unsigned int Docid20, unsigned int Page, unsigned int PageSize, StructResut  st)
{
    vector<unsigned int> Tokens;
    Tokens.push_back(Docid1);
    Tokens.push_back(Docid2);
    Tokens.push_back(Docid3);
    Tokens.push_back(Docid4);
    Tokens.push_back(Docid5);
    Tokens.push_back(Docid6);
    Tokens.push_back(Docid7);
    Tokens.push_back(Docid8);
    Tokens.push_back(Docid9);
    Tokens.push_back(Docid10);
    Tokens.push_back(Docid11);
    Tokens.push_back(Docid12);
    Tokens.push_back(Docid13);
    Tokens.push_back(Docid14);
    Tokens.push_back(Docid15);
    Tokens.push_back(Docid16);
    Tokens.push_back(Docid17);
    Tokens.push_back(Docid18);
    Tokens.push_back(Docid19);
    Tokens.push_back(Docid20);
    vector<unsigned int> Result;
    unsigned int ResultCnts = 0;
    unsigned int Ret = QueryDocIdByTokensImpl(Tokens, Page, PageSize, ResultCnts, Result);
    st.ResultCnts = ResultCnts;
    st.PageCnt = Result.size();

    //搜索结果
    cout << "搜索结果如下\n";
    unsigned int TmpResult[10] = {0,};
    for (int i = 0 ; i < Result.size() && i < 10 ; i++)
    {
        TmpResult[i] = Result[i];
        cout << Result[i] << endl;
    }
    //转移到struct中
    st.Result1 = TmpResult[0];
    st.Result2 = TmpResult[1];
    cout << st.ResultCnts << " " << st.PageCnt << " " << st.Result1 << " " << st.Result2 << endl;
	return Ret;
}
*/

StructResutlPointer QueryDocIdByTokens(unsigned int Docid1, unsigned int Docid2, unsigned int Docid3, unsigned int Docid4, unsigned int Docid5, unsigned int Docid6, unsigned int Docid7, unsigned int Docid8, unsigned int Docid9, unsigned int Docid10, unsigned int Docid11, unsigned int Docid12, unsigned int Docid13, unsigned int Docid14, unsigned int Docid15, unsigned int Docid16, unsigned int Docid17, unsigned int Docid18, unsigned int Docid19, unsigned int Docid20, unsigned int Page, unsigned int PageSize)
{
    vector<unsigned int> Tokens;
    Tokens.push_back(Docid1);
    Tokens.push_back(Docid2);
    Tokens.push_back(Docid3);
    Tokens.push_back(Docid4);
    Tokens.push_back(Docid5);
    Tokens.push_back(Docid6);
    Tokens.push_back(Docid7);
    Tokens.push_back(Docid8);
    Tokens.push_back(Docid9);
    Tokens.push_back(Docid10);
    Tokens.push_back(Docid11);
    Tokens.push_back(Docid12);
    Tokens.push_back(Docid13);
    Tokens.push_back(Docid14);
    Tokens.push_back(Docid15);
    Tokens.push_back(Docid16);
    Tokens.push_back(Docid17);
    Tokens.push_back(Docid18);
    Tokens.push_back(Docid19);
    Tokens.push_back(Docid20);
    vector<unsigned int> Result;
    unsigned int ResultCnts = 0;
    unsigned int Ret = QueryDocIdByTokensImpl(Tokens, Page, PageSize, ResultCnts, Result);
    StructResutlPointer st = (StructResutlPointer)malloc(sizeof(StructResut));
    st->ResultCnts = ResultCnts;
    st->PageCnt = Result.size();

    //搜索结果
    cout << "搜索结果如下\n";
    unsigned int TmpResult[10] = {0,};
    for (int i = 0 ; i < Result.size() && i < 10 ; i++)
    {
        TmpResult[i] = Result[i];
        cout << Result[i] << endl;
    }
    //转移到struct中
    st->Result1 = TmpResult[0];
    st->Result2 = TmpResult[1];
	cout << "point" << hex << st << ":" << endl;
    return st;
}
