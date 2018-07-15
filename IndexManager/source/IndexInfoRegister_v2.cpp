/***
 V2 ，通过解析文件进行注册
 */
#include <stdio.h>
#include "IndexMng.h"
#include <stdarg.h>
#include <string>
#include <fstream>
using namespace std;

extern map<unsigned int, PostingList> Index;
extern map<unsigned int, unsigned int> DocInfoTable;
extern map<unsigned int, WikiDocInfo> DocInfoTableWiki;

extern void ExcuteTfIDF();

int GetDocInfoFromStr(const string & docInfo, unsigned int &docId, unsigned int &tf, vector<int> &poses)
{
    int docidPosEnd = docInfo.find(',');  //放置出现
    string docIdStr = docInfo.substr(0, docidPosEnd);
    int tfPosEnd = docInfo.find(',', docidPosEnd + 1);
    string tfStr = docInfo.substr(docidPosEnd + 1, tfPosEnd - docidPosEnd);
    docId = stoi(docIdStr, 0, 16);
    tf = stoi(tfStr);
    //poses.resize(tf);
    int posPosBegin = docInfo.find('<') + 1;
    int posPosEnd = posPosBegin;
    for (int posIndex = 0; posIndex < tf; posIndex++)
    {
        posPosEnd = docInfo.find(',',posPosBegin);
        string posStr = docInfo.substr(posPosBegin, posPosEnd - posPosBegin);
        int pos = stoi(posStr);
        poses.push_back(pos);
        posPosBegin = posPosEnd + 1;
    }
    
    return 0;
}

int ConvertStrToIndexMem(string wordIdStr, string dfStr, vector<string> &DocInfo)
{
    unsigned int wordId = stoi(wordIdStr);
    unsigned int df = stoi(dfStr);
    
    PostingList info;
    info.DF = df;
    unsigned int docId = 0;
    unsigned int Tf = 0;
    for (int i =0 ; i < df; i++)
    {
        vector<int> poses;
        (void)GetDocInfoFromStr(DocInfo[i], docId, Tf, poses);
        info.DocIDList.push_back(docId);
        info.TFList.push_back(Tf);
        info.DocPosition.push_back(poses);
        info.Weight.push_back(0);
    }
    Index[wordId] = info;
    return 0;
}

int ParserPostingList(const string &PostingList)
{
    //    /*c++*/    Index[870] = AllocIndexInfo(3,0x1000071,6,<1,212,241,1626,1670,1701,>,0x1000073,6,<0,247,275,512,540,1437,>,0x1000074,111,<0,45,148,595,1266,1970,2730,2964,2973,5536,5553,5596,5642,5682,5730,5766,5802,5849,5896,5934,5981,6028,6065,6105,6142,6184,6230,6278,6330,6372,6405,6446,6489,6525,6567,6600,6636,6665,6727,6762,6791,6815,6844,6875,6914,6969,7004,7030,7055,7079,7103,7128,7156,7184,7208,7236,7262,7286,7314,7347,7386,7458,7530,7569,7610,7654,7694,7736,7768,7802,7885,7913,7948,7987,8026,8105,8134,8174,8208,8236,8337,8381,8409,8431,8457,8485,8537,8563,8599,8635,8678,8722,8745,8769,8834,8862,8888,8916,8974,9046,9092,9150,9223,9271,9332,9422,9519,9594,9632,9955,10058,>);
    //wordid
    int posBegin = PostingList.find("*/");
    int wordIdPosBegin = PostingList.find('[', posBegin);
    int wordIdPosEnd = PostingList.find(']');
    string wordId = PostingList.substr(wordIdPosBegin + 1, wordIdPosEnd - wordIdPosBegin - 1);
    cout << "wordId:" << wordId << endl;
    int dfPosBegin = PostingList.find('(', wordIdPosEnd);
    int dfPosEnd = PostingList.find(',',dfPosBegin);
    string dfStr = PostingList.substr(dfPosBegin + 1, dfPosEnd - dfPosBegin -1);
    cout << "dfStr:" << dfStr << endl;
    //开始查找df个Doc
    int df = stoi(dfStr);
    int docBegin = dfPosEnd + 1;
    int docEnd = dfPosEnd;
    vector<string> docInfo;
    for (int docIndex = 0; docIndex < df; docIndex++)
    {
        docEnd = PostingList.find('>', docBegin);
        string tmpDocStr = PostingList.substr(docBegin, docEnd - docBegin + 1);
        cout << tmpDocStr << endl;
        docInfo.push_back(tmpDocStr);
        docBegin = docEnd + 2;  //跳过 >,
    }
    int Ret = ConvertStrToIndexMem(wordId, dfStr, docInfo);
    return Ret;
}

int ParserDocInfo(const string &docInfo)
{
    //    DocInfoTable[0x1000072] = 10334,17,100,10217 ;
    int docidPB = docInfo.find('[') + 1;
    int docidPE = docInfo.find(']');
    string docidStr = docInfo.substr(docidPB, docidPE - docidPB);
    unsigned int docid = stoi(docidStr, 0, 16); //16进制
    int totalLenPB = docInfo.find('=') + 2;
    int totalLenPE = docInfo.find(',', totalLenPB);
    string totalLenStr = docInfo.substr(totalLenPB, totalLenPE - totalLenPB);
    unsigned int totalLen = stoi(totalLenStr);

    int titleLenPB = totalLenPE + 1;
    int titleLenPE = docInfo.find(',', titleLenPB);
    string titleLenStr = docInfo.substr(titleLenPB, titleLenPE - titleLenPB);
    unsigned int titleLen = stoi(titleLenStr);

    int abstractLenPB = titleLenPE + 1;
    int abstractLenPE = docInfo.find(',', abstractLenPB);
    string abstractLenStr = docInfo.substr(abstractLenPB, abstractLenPE - abstractLenPB);
    unsigned int abstractLen = stoi(abstractLenStr);

    int contentLenPB = abstractLenPE + 1;
    int contentLenPE = docInfo.find(';', contentLenPB);
    string contentLenStr = docInfo.substr(contentLenPB, contentLenPE - contentLenPB);
    unsigned int contentLen = stoi(contentLenStr);

    DocInfoTable[docid] = totalLen;
    WikiDocInfo info;
    info.totalLen = totalLen;
    info.titleLen = titleLen;
    info.abstractLen = abstractLen;
    info.contentLen = contentLen;
    DocInfoTableWiki[docid] = info;
    return 0;
}

int ParserOneLine(const string &info)
{
    if (info.find("DocInfoTable[") == 0)
    {
        return ParserDocInfo(info);
    }
    else if (info.find("/*") == 0)
    {
        return ParserPostingList(info);
    }
    else
    {
        return -1;
    }
}

int ParserInvertedFile(string path)
{
    ifstream InvertedFile;
    InvertedFile.open(path);
    if (!InvertedFile.is_open())
    {
        return 0;
    }
    string tmpStr;
    while(!InvertedFile.eof())
    {
        getline(InvertedFile,tmpStr);
        int Ret = ParserOneLine(tmpStr);
        if (Ret != 0)
        {
            
        }
    }
    InvertedFile.close();
    ExcuteTfIDF();
    return 0;
}

int ParserInvertedFile_ForPython()
{
    ParserInvertedFile("/Users/kinmioliu/Develop/Python/assistant/assistant/inverted_file.txt");
    return 0;
}
