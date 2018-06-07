//
//  main.cpp
//  IndexMng
//
//  Created by 刘进谋 on 2018/5/22.
//  Copyright © 2018年 刘进谋. All rights reserved.
//
#include "IndexMng.h"
#include <iostream>
#include <map>
#include <set>
#include <vector>
#include <math.h>
using namespace std;

// tokenid|count|<docid,fk>,<docid,fk>,<docid,fk>
extern map<unsigned int, PostingList> Index;


unsigned int GetAllDocNums()
{
    set<unsigned int> Counter;
    map<unsigned int, PostingList>::iterator itr = Index.begin();
    for (; itr != Index.end(); ++itr)
    {
        vector<unsigned int>::iterator DocItr = itr->second.DocIDList.begin();
        for (; DocItr != itr->second.DocIDList.end(); DocItr++)
        {
            Counter.insert(*DocItr);
        }
    }
    
    return Counter.size();
}

void CalcLexiconWeight(unsigned int DocNums)
{
    map<unsigned int, PostingList>::iterator itr = Index.begin();
    for (; itr != Index.end(); ++itr)
    {
        for (int index = 0; index < itr->second.DocIDList.size(); index++)
        {
            //特征权重使用tf*IDF框架
            itr->second.IDF = log10((double)DocNums/(double)(itr->second.DF));
            itr->second.Weight[index] = itr->second.IDF * double(itr->second.TFList[index]);
            cout << "N:" << DocNums << ",nk:" << itr->second.DF << ",Tf:" << itr->second.TFList[index] << "=> log10(N/nk) * Tf => IDFk:" << itr->second.IDF << " => ";
            cout << itr->second.Weight[index] << endl;
        }
    }
}

void ExcuteTfIDF()
{
    unsigned int DocNums = GetAllDocNums();
    cout << "GetAllDocNums(): " << DocNums << endl;
    CalcLexiconWeight(DocNums);
}

typedef struct TF_WEI
{
    unsigned int TF;
    double weight;
}TF_WEI;

void CalcQDWeight(vector<unsigned int> &QWordIdList,map<unsigned int, TF_WEI> &QWordPostInfo)
{
    ;
    for(int index = 0; index < QWordIdList.size(); index++)
    {
        unsigned int CurWordId = QWordIdList[index];
        if (QWordPostInfo.find(CurWordId) != QWordPostInfo.end())
        {
            QWordPostInfo[CurWordId].TF += 1;
        }
        else
        {
            QWordPostInfo[CurWordId].TF = 1;
        }
    }
    map<unsigned int, TF_WEI>::iterator itr = QWordPostInfo.begin();
    //计算weight
    for (; itr != QWordPostInfo.end(); itr++)
    {
        unsigned int CurWordId = itr->first;
        double IDF = 0;
        map<unsigned int, PostingList>::iterator LexWordItr = Index.find(CurWordId);
        if (LexWordItr != Index.end())
        {
            IDF = LexWordItr->second.IDF;
        }
        itr->second.weight = itr->second.TF * IDF;
        
        cout << "QCurId: " << CurWordId << "QCurTF: " << itr->second.TF << "QCurIDF: " << IDF << "QCurWei: " << itr->second.weight << endl;
    }
}



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
        map<unsigned int, PostingList>::iterator IndexIter = Index.find(*TokenIter);
        if (IndexIter == Index.end())
        {
            continue;
        }
        //命中
        unsigned int TmpDocId;
        for (int i = 0; i < IndexIter->second.DocIDList.size(); i++ )
        {
            TmpDocId = IndexIter->second.DocIDList[i];
            //计分算法V1，根据命中的数量来计算
            DocidScores[TmpDocId] += 1 * IndexIter->second.TFList[i];
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

typedef struct VectorSpaceDocInfo
{
    double Score;
    //分别对应20个查询单词的权重
    double Weights[20];
}StVectorSpaceDocInfo;

//使用向量空间算法
int QueryDocIdByTokensImpl_V2(vector<unsigned int> &Tokens, unsigned int Page, unsigned int PageSize,unsigned int &ResultCnts, vector<unsigned int> &Result)
{
    //容器中始终保存最大的这个值
    map<unsigned int, TF_WEI> QWordPostInfo;
    CalcQDWeight(Tokens, QWordPostInfo);
    map<unsigned int, VectorSpaceDocInfo> DocVectorSpace;
    map<unsigned int, TF_WEI>::iterator TokenIter = QWordPostInfo.begin();
    //为了方便计算
    StVectorSpaceDocInfo QDocVS;
    unsigned int TokenIndexInQPMap = 0;
    for (; TokenIter != QWordPostInfo.end(); TokenIter++)
    {
        QDocVS.Weights[TokenIndexInQPMap] = TokenIter->second.weight;
        TokenIndexInQPMap ++;
        map<unsigned int, PostingList>::iterator IndexIter = Index.find(TokenIter->first);
        if (IndexIter == Index.end())
        {
            continue;
        }
        //命中
        unsigned int TmpDocId;
        for (int i = 0; i < IndexIter->second.DocIDList.size(); i++ )
        {
            TmpDocId = IndexIter->second.DocIDList[i];
            DocVectorSpace[TmpDocId].Weights[TokenIndexInQPMap - 1] = IndexIter->second.Weight[i];
            /*map<unsigned int, VectorSpaceDocInfo>::iterator DocVSItr = DocVectorSpace.find(TmpDocId);
            if (DocVSItr != DocVectorSpace.end())
            {
                //说明之前计算过,设置 该单词 在 该文档中的 权重
                DocVSItr->second.Weights[TokenIndexInQPMap] = IndexIter->second.Weight[i];

            }
            else
            {
                //没有计算过，设置一个值
                DocVectorSpace[TmpDocId] = VectorSpaceDocInfo();
            }
            */
        }
    }
    unsigned int TokenCount = QWordPostInfo.size();
    
    //计算Consine 相似性
    
    
    map<unsigned int, VectorSpaceDocInfo>::iterator AimDocItr = DocVectorSpace.begin();
    for (; AimDocItr != DocVectorSpace.end(); AimDocItr++)
    {
        //分子
        double dividend = 0;
        double divisor = 0;
        for( int i = 0; i < TokenCount; i++)
        {
            dividend += (AimDocItr->second.Weights[i] * )
        }
    }
    /*
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
     */
    return 0;
}


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
    unsigned int Ret = QueryDocIdByTokensImpl_V2(Tokens, Page, PageSize, ResultCnts, Result);
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
    return st;
}

int main(int argc, const char * argv[])
{
    ExcuteTfIDF();
    map<unsigned int, PostingList>::iterator itr = Index.begin();
    for (; itr != Index.end(); ++itr)
    {
        cout << itr->first << " val:" << itr->second << endl;
    }
    
    StructResutlPointer p =  QueryDocIdByTokens(0, 3, 4, 8, 0,
                       0, 0, 0, 4, 0,
                       0, 0, 0 , 0, 0,
                       0, 0, 0, 0, 0,
                        1,3);
    cout << p->PageCnt << " "  << p->ResultCnts << endl;
    std::cout << "Hello, World!\n";
    return 0;
}



