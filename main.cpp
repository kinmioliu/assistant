//
//  main.cpp
//  IndexMng
//
//  Created by 刘进谋 on 2018/5/22.
//  Copyright © 2018年 刘进谋. All rights reserved.
//

#include <iostream>
#include <map>
#include <set>
#include <vector>
using namespace std;

// token|count|<docid,fk>,<docid,fk>,<docid,fk>

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
        for (int i = 0; i < count; i+=2)
        {
            info.docid.push_back(va_arg(args, unsigned int));
            info.docfk.push_back(va_arg(args, unsigned int));
        }
        va_end(args);
        return info;
    }
    
    IndexInitializer()
    {
        Index["axxxx"] = AllocIndexInfo(4,8,1,2,3,4,5,6,7,8);
        Index["cxxxx"] = AllocIndexInfo(3,6,3,4,5,6,7,8);
        Index["bxxxx"] = AllocIndexInfo(3,6,5,3,5,6,7,8);
    }
};

static IndexInitializer init;

int main(int argc, const char * argv[])
{
    // insert code here...
    map<string, IndexInfo>::iterator itr = Index.begin();
    for (; itr != Index.end(); ++itr)
    {
        cout << itr->first << " val:" << itr->second << endl;
    }
    
    std::cout << "Hello, World!\n";
    return 0;
}
