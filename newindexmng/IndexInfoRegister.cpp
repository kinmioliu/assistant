//
//  IndexInfoRegister.cpp
//  IndexMng
//
//  Created by 刘进谋 on 2018/6/6.
//  Copyright © 2018年 刘进谋. All rights reserved.
//

#include <stdio.h>
#include "IndexMng.h"
#include <stdarg.h>

map<unsigned int, PostingList> Index;

class IndexInitializer
{
public:
    static PostingList AllocIndexInfo(int fk, int count, ...)
    {
        va_list args;
        va_start(args, count);
        PostingList info;
        info.DF = fk;
        for (int i = 0; i < count; i+=2)
        {
            info.DocIDList.push_back(va_arg(args, unsigned int));
            info.TFList.push_back(va_arg(args, unsigned int));
            info.Weight.push_back(0);
        }
        va_end(args);
        return info;
    }


    static void InitializeGroup1()
    {
        Index[5] = AllocIndexInfo(4,8,1,2,3,4,5,6,7,1);
        Index[6] = AllocIndexInfo(3,6,3,4,5,6,7,3);
        Index[3] = AllocIndexInfo(3,6,5,3,5,6,7,8);
        Index[6] = AllocIndexInfo(3,6,12,1,44,6,7,8);

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

