//
//  main.cpp
//  IndexMng
//
//  Created by 刘进谋 on 2018/5/22.
//  Copyright © 2018年 刘进谋. All rights reserved.
//
#include "IndexMng.h"
#include "BM25Score.h"
#include <iostream>
#include <map>
#include <set>
#include <vector>
#include <math.h>

using namespace std;

// tokenid|count|<docid,fk>,<docid,fk>,<docid,fk>
map<unsigned int, PostingList> Index;
map<unsigned int, unsigned int> DocInfoTable;
map<unsigned int, WikiDocInfo> DocInfoTableWiki;

unsigned int WIKI_TYPE = 0x01000000;
unsigned int MML_TYPE = 0x02000000;
unsigned int EVT_TYPE = 0x04000000;
unsigned int INTRES_TYPE = 0x08000000;
unsigned int ID_MASK = 0x00ffffff;

float g_AverageDocLen = 0;

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
    map<unsigned int, unsigned int>::iterator DocItr = DocInfoTable.begin();
    unsigned int TotalDocLen = 0;
    for (; DocItr != DocInfoTable.end(); DocItr++)
    {
        TotalDocLen += DocItr->second;
    }
    g_AverageDocLen = (float)TotalDocLen / (float)DocInfoTable.size();
}

typedef struct TF_WEI
{
    unsigned int TF;
    double weight;
}TF_WEI;

void CalcQDWeight(vector<unsigned int> &QWordIdList,map<unsigned int, TF_WEI> &QWordPostInfo)
{
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


// doctid,score
typedef pair<unsigned int, double> PAIR;
int compare(const PAIR& x, const PAIR& y)
{
    return  y.second < x.second;
}

typedef pair<unsigned int, unsigned int> DocWord;
// doctid,score
typedef pair<DocWord, double> PAIR_V2;
int compare_v2(const PAIR_V2& x, const PAIR_V2& y)
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

bool MatchedQueryClass(unsigned int queryClass, unsigned int docId)
{
	if (docId & queryClass)
	{
		return true;
	}
	return false;
}

//使用向量空间算法
int QueryDocIdByTokensImpl_V2(vector<unsigned int> &Tokens, unsigned int Page, unsigned int PageSize, unsigned int QueryClass, unsigned int &ResultCnts, vector<unsigned int> &Result)
{
    //容器中始终保存最大的这个值
    map<unsigned int, TF_WEI> QWordPostInfo;
    CalcQDWeight(Tokens, QWordPostInfo);
    map<unsigned int, VectorSpaceDocInfo> DocVectorSpace;
    map<unsigned int, TF_WEI>::iterator TokenIter = QWordPostInfo.begin();
    //为了方便计算,将被查单词的每个Token的权重依次放在Weights数组中
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
			if (!MatchedQueryClass(QueryClass, TmpDocId))
			{
				//如果不是要查询的类别，跳过
				continue;
			}
            DocVectorSpace[TmpDocId].Weights[TokenIndexInQPMap - 1] = IndexIter->second.Weight[i];
        }
    }
    unsigned int TokenCount = QWordPostInfo.size();
	vector<PAIR> DocResult;
    //计算Consine 相似性        
    map<unsigned int, VectorSpaceDocInfo>::iterator AimDocItr = DocVectorSpace.begin();
    for (; AimDocItr != DocVectorSpace.end(); AimDocItr++)
    {
        //分子
        double dividend = 0;        
        for( int i = 0; i < TokenCount; i++)
        {
			dividend += (AimDocItr->second.Weights[i] * QDocVS.Weights[i]);
        }

		double divisorAim = 0;

		for (int i = 0; i < TokenCount; i++)
		{
			divisorAim += (AimDocItr->second.Weights[i] * AimDocItr->second.Weights[i]);
		}
		double divisorQW = 0;
		for (int i = 0; i < TokenCount; i++)
		{
			divisorQW += (AimDocItr->second.Weights[i] * AimDocItr->second.Weights[i]);
		}
		double divisor = sqrt(divisorAim * divisorQW);
		AimDocItr->second.Score = dividend / divisor;
		DocResult.push_back(PAIR(AimDocItr->first, AimDocItr->second.Score));
    }

    
    //打印结果
    //按照得分高者进行排序
    cout << "sorted by score result\n";
    sort(DocResult.begin(), DocResult.end(), compare);
    for (int i = 0 ; i < DocResult.size(); i++)
    {
        cout << DocResult[i].first << ":" << DocResult[i].second << endl;
    }
    
    ResultCnts = DocResult.size();
    
    //提取出对应Page的数据
    unsigned int ResultSize = DocResult.size();
    unsigned int ResultIndex = PageSize * Page;
    unsigned int ResultIndexEnd = ResultIndex + PageSize;
    for (; ResultIndex < ResultSize && ResultIndex < ResultIndexEnd ; ResultIndex++)
    {
        Result.push_back(DocResult[ResultIndex].first);
    }
    return 0;
}
int CalculateLocation(unsigned int docId, unsigned int wordId)
{
    //判断这个单词是否在索引当中，若不存在，就跳过
    map<unsigned int, PostingList>::iterator IndexIter = Index.find(wordId);
    if (IndexIter == Index.end())
    {
        //若找不到，那么就从0开始显示
        return 0;
    }
    //从这个postlist中找到对应的docid
    unsigned int DF = IndexIter->second.DF;
    for(unsigned int docIndex = 0; docIndex < DF; docIndex++)
    {
        unsigned int indexDocId = IndexIter->second.DocIDList[docIndex];
        //判断是否匹配
        if (docId == indexDocId)
        {
            //暂时先返回第一个位置
            //
            return IndexIter->second.DocPosition[docIndex][0];
        }
    }
    return 0;
}

typedef struct QueryScore
{
    unsigned int wordId;
    unsigned int contnetPos;
    float curWordScore;
    float totalScore;
}QueryScore;

bool IsInContent(const PostingList& postingList, int DocIndex, unsigned int queryClass, int &contentPos)
{
    const vector<int> & position = postingList.DocPosition[DocIndex];
    if (queryClass != WIKI_TYPE)
    {
        return false;
    }
    const WikiDocInfo& docInfo = DocInfoTableWiki[postingList.DocIDList[DocIndex]];
    int contentbegin = docInfo.titleLen + docInfo.abstractLen;
    for (int posIndex = 0; posIndex < position.size(); posIndex++)
    {
        if (position[posIndex] >= contentbegin)
        {
            contentPos =  position[posIndex] - contentbegin;
            return true;
        }
    }
    return false;
}

int QueryDocIdByTokensImpl_BM25(vector<unsigned int> &Tokens, unsigned int Page, unsigned int PageSize, unsigned int QueryClass, unsigned int &ResultCnts, vector<unsigned int> &Result, vector<int> &Loc)
{
    map<unsigned int, QueryScore > QueryDocScore;
    vector<unsigned int>::iterator TermItr = Tokens.begin();
    //遍历每个单词
    for (;TermItr != Tokens.end(); TermItr++)
    {
        //判断这个单词是否在索引当中，若不存在，就跳过
        map<unsigned int, PostingList>::iterator IndexIter = Index.find(*TermItr);
        if (IndexIter == Index.end())
        {
            continue;
        }
        
        //该word在DF个文档中出现了
        unsigned int DF = IndexIter->second.DF;
        for(unsigned int docIndex = 0; docIndex < DF; docIndex++)
        {
            unsigned int docId = IndexIter->second.DocIDList[docIndex];
            if (!MatchedQueryClass(QueryClass, docId))
            {
                //如果不是要查询的类别，跳过
                continue;
            }
            //查询这个词的TF
            unsigned int tf = IndexIter->second.TFList[docIndex];
            unsigned int DltLen = DocInfoTable.size(); //文档总数量
            unsigned int DocLen = DF;//文档频率
            unsigned int TotalDicSize = Index.size();
            unsigned int CurDocLen = DocInfoTable[docId];
            float Score = CalculateBM25(DocLen, tf, 1, 0, DltLen, CurDocLen, g_AverageDocLen);
            
            int contentPos = 0;
            if (QueryDocScore.find(docId) == QueryDocScore.end())
            {
                //还需要判断该单词是否在content中，是content中才赋值
                QueryScore QS;
                QS.totalScore = Score;
                if (IsInContent(IndexIter->second, docIndex, QueryClass, contentPos))
                {
                    
                    QS.wordId = *TermItr;
                    QS.curWordScore = Score;
                    QS.contnetPos = contentPos;
                }
                else
                {
                    QS.wordId = 0;
                    QS.curWordScore = 0;
                    QS.contnetPos = 0;
                }
                QueryDocScore[docId] = QS;
            }
            else
            {
                if (Score > QueryDocScore[docId].curWordScore
                    && IsInContent(IndexIter->second, docIndex, QueryClass, contentPos))
                {
                    QueryDocScore[docId].wordId = *TermItr;
                    QueryDocScore[docId].curWordScore = Score;
                    QueryDocScore[docId].contnetPos = contentPos;
                }
                QueryDocScore[docId].totalScore += Score;
            }
        }
    }
    vector<PAIR_V2> DocResult;
    map<unsigned int, QueryScore>::iterator itr = QueryDocScore.begin();
    for (; itr != QueryDocScore.end(); itr++)
    {
        DocResult.push_back(PAIR_V2(DocWord(itr->first, itr->second.contnetPos), itr->second.totalScore));
    }
    
    //打印结果
    //按照得分高者进行排序
    cout << "sorted by score result\n";
    sort(DocResult.begin(), DocResult.end(), compare_v2);
    for (int i = 0 ; i < DocResult.size(); i++)
    {
        cout << hex<< DocResult[i].first.first << ":" << DocResult[i].second << endl;
    }
    
    ResultCnts = DocResult.size();
    
    vector<DocWord> Result_V2;
    //提取出对应Page的数据
    unsigned int ResultSize = DocResult.size();
    Page = (Page == 0) ? 0 : Page - 1;
    unsigned int ResultIndex = PageSize * Page;
    unsigned int ResultIndexEnd = ResultIndex + PageSize;
    for (; ResultIndex < ResultSize && ResultIndex < ResultIndexEnd ; ResultIndex++)
    {
        Result.push_back(DocResult[ResultIndex].first.first);
        //Result_V2.push_back(DocResult[ResultIndex].first);
        //计算显示的位置
        //int loc = CalculateLocation(DocResult[ResultIndex].first.first, DocResult[ResultIndex].first.second);
        Loc.push_back(DocResult[ResultIndex].first.second);
    }
    return 0;
}


StructResutlPointer QueryDocIdByTokens(unsigned int Docid1, unsigned int Docid2, unsigned int Docid3, unsigned int Docid4, unsigned int Docid5, unsigned int Docid6, unsigned int Docid7, unsigned int Docid8, unsigned int Docid9, unsigned int Docid10, unsigned int Docid11, unsigned int Docid12, unsigned int Docid13, unsigned int Docid14, unsigned int Docid15, unsigned int Docid16, unsigned int Docid17, unsigned int Docid18, unsigned int Docid19, unsigned int Docid20, unsigned int Page, unsigned int PageSize, unsigned int QueryClass)
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
    vector<int> Loc;
    unsigned int ResultCnts = 0;
    unsigned int Ret = QueryDocIdByTokensImpl_BM25(Tokens, Page, PageSize, QueryClass, ResultCnts, Result, Loc);
    StructResutlPointer st = (StructResutlPointer)malloc(sizeof(StructResut));
    st->ResultCnts = ResultCnts; //搜索总结果
    st->PageCnt = Result.size();    //本次搜索结果中的数据
    
    //搜索结果
    cout << "搜索结果如下\n";
    unsigned int TmpResult[10] = {0,};
    int tmpLoc[10] = {0,};
    for (int i = 0 ; i < Result.size() && i < 10 ; i++)
    {
        TmpResult[i] = Result[i];
        tmpLoc[i] = Loc[i];
        cout << Result[i] << ":loc" << tmpLoc[i] << endl;
    }
    //转移到struct中
    st->Result1 = TmpResult[0];
    st->Result2 = TmpResult[1];
    st->Result3 = TmpResult[2];
    st->Result4 = TmpResult[3];
    st->Result5 = TmpResult[4];
    st->Result6 = TmpResult[5];
    st->Result7 = TmpResult[6];
    st->Result8 = TmpResult[7];
    st->Result9 = TmpResult[8];
    st->Result10 = TmpResult[9];
    st->Loc1 = tmpLoc[0];
    st->Loc2 = tmpLoc[1];
    st->Loc3 = tmpLoc[2];
    st->Loc4 = tmpLoc[3];
    st->Loc5 = tmpLoc[4];
    st->Loc6 = tmpLoc[5];
    st->Loc7 = tmpLoc[6];
    st->Loc8 = tmpLoc[7];
    st->Loc9 = tmpLoc[8];
    st->Loc10 = tmpLoc[9];
    return st;
}

//g++ BM25Score.cpp IndexInfoRegister.cpp main.cpp -I ../pubh -fPIC -shared -o IndexMng.so


int sum(int a, int b) {
	return a + b;
}
