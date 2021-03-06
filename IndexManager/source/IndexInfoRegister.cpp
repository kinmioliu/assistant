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

extern map<unsigned int, PostingList> Index;
extern map<unsigned int, unsigned int> DocInfoTable;


extern void ExcuteTfIDF();

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
        /*appcfg*/    Index[1] = AllocIndexInfo(20,40,0x2000001,1,0x2000002,1,0x2000003,1,0x2000004,1,0x2000005,1,0x2000006,1,0x2000007,1,0x2000008,1,0x2000009,1,0x200000a,1,0x200000b,1,0x200000c,1,0x200000d,1,0x200000e,1,0x200000f,1,0x2000010,1,0x2000011,1,0x2000012,1,0x2000013,1,0x2000014,1);
        /*delay*/    Index[2] = AllocIndexInfo(40,80,0x2000001,1,0x2000002,1,0x2000003,1,0x2000004,1,0x2000005,1,0x2000006,1,0x2000007,1,0x2000008,1,0x2000009,1,0x200000a,1,0x200000b,1,0x200000c,1,0x200000d,1,0x200000e,1,0x200000f,1,0x2000010,1,0x2000011,1,0x2000012,1,0x2000013,1,0x2000014,1,0x2000015,1,0x2000016,1,0x2000017,1,0x2000018,1,0x2000019,1,0x200001a,1,0x200001b,1,0x200001c,1,0x200001d,1,0x200001e,1,0x200001f,1,0x2000020,1,0x2000021,1,0x2000022,1,0x2000023,1,0x2000024,1,0x2000025,1,0x2000026,1,0x2000027,1,0x2000028,1);
        /*time1*/    Index[3] = AllocIndexInfo(2,4,0x2000001,1,0x2000015,1);
        /* */    Index[4] = AllocIndexInfo(80,160,0x2000001,2,0x2000002,2,0x2000003,2,0x2000004,2,0x2000005,2,0x2000006,2,0x2000007,2,0x2000008,2,0x2000009,2,0x200000a,2,0x200000b,2,0x200000c,2,0x200000d,2,0x200000e,2,0x200000f,2,0x2000010,2,0x2000011,2,0x2000012,2,0x2000013,2,0x2000014,2,0x2000015,2,0x2000016,2,0x2000017,2,0x2000018,2,0x2000019,2,0x200001a,2,0x200001b,2,0x200001c,2,0x200001d,2,0x200001e,2,0x200001f,2,0x2000020,2,0x2000021,2,0x2000022,2,0x2000023,2,0x2000024,2,0x2000025,2,0x2000026,2,0x2000027,2,0x2000028,2);
        /*执行*/    Index[5] = AllocIndexInfo(40,80,0x2000001,1,0x2000002,1,0x2000003,1,0x2000004,1,0x2000005,1,0x2000006,1,0x2000007,1,0x2000008,1,0x2000009,1,0x200000a,1,0x200000b,1,0x200000c,1,0x200000d,1,0x200000e,1,0x200000f,1,0x2000010,1,0x2000011,1,0x2000012,1,0x2000013,1,0x2000014,1,0x2000015,1,0x2000016,1,0x2000017,1,0x2000018,1,0x2000019,1,0x200001a,1,0x200001b,1,0x200001c,1,0x200001d,1,0x200001e,1,0x200001f,1,0x2000020,1,0x2000021,1,0x2000022,1,0x2000023,1,0x2000024,1,0x2000025,1,0x2000026,1,0x2000027,1,0x2000028,1);
        /*延时*/    Index[6] = AllocIndexInfo(38,76,0x2000001,1,0x2000002,1,0x2000003,1,0x2000004,1,0x2000005,1,0x2000006,1,0x2000007,1,0x2000008,1,0x2000009,1,0x200000a,1,0x200000b,1,0x200000c,1,0x200000d,1,0x200000e,1,0x200000f,1,0x2000010,1,0x2000011,1,0x2000012,1,0x2000013,1,0x2000015,1,0x2000016,1,0x2000017,1,0x2000018,1,0x2000019,1,0x200001a,1,0x200001b,1,0x200001c,1,0x200001d,1,0x200001e,1,0x200001f,1,0x2000020,1,0x2000021,1,0x2000022,1,0x2000023,1,0x2000024,1,0x2000025,1,0x2000026,1,0x2000027,1);
        /*操作*/    Index[7] = AllocIndexInfo(40,80,0x2000001,1,0x2000002,1,0x2000003,1,0x2000004,1,0x2000005,1,0x2000006,1,0x2000007,1,0x2000008,1,0x2000009,1,0x200000a,1,0x200000b,1,0x200000c,1,0x200000d,1,0x200000e,1,0x200000f,1,0x2000010,1,0x2000011,1,0x2000012,1,0x2000013,1,0x2000014,1,0x2000015,1,0x2000016,1,0x2000017,1,0x2000018,1,0x2000019,1,0x200001a,1,0x200001b,1,0x200001c,1,0x200001d,1,0x200001e,1,0x200001f,1,0x2000020,1,0x2000021,1,0x2000022,1,0x2000023,1,0x2000024,1,0x2000025,1,0x2000026,1,0x2000027,1,0x2000028,1);
        /*time2*/    Index[8] = AllocIndexInfo(2,4,0x2000002,1,0x2000016,1);
        /*time3*/    Index[9] = AllocIndexInfo(2,4,0x2000003,1,0x2000017,1);
        /*time4*/    Index[10] = AllocIndexInfo(2,4,0x2000004,1,0x2000018,1);
        /*time5*/    Index[11] = AllocIndexInfo(2,4,0x2000005,1,0x2000019,1);
        /*time6*/    Index[12] = AllocIndexInfo(2,4,0x2000006,1,0x200001a,1);
        /*time7*/    Index[13] = AllocIndexInfo(2,4,0x2000007,1,0x200001b,1);
        /*time8*/    Index[14] = AllocIndexInfo(2,4,0x2000008,1,0x200001c,1);
        /*time9*/    Index[15] = AllocIndexInfo(2,4,0x2000009,1,0x200001d,1);
        /*time10*/    Index[16] = AllocIndexInfo(2,4,0x200000a,1,0x200001e,1);
        /*10*/    Index[17] = AllocIndexInfo(4,8,0x200000a,2,0x200001e,2);
        /*time11*/    Index[18] = AllocIndexInfo(2,4,0x200000b,1,0x200001f,1);
        /*11*/    Index[19] = AllocIndexInfo(4,8,0x200000b,2,0x200001f,2);
        /*time12*/    Index[20] = AllocIndexInfo(2,4,0x200000c,1,0x2000020,1);
        /*12*/    Index[21] = AllocIndexInfo(4,8,0x200000c,2,0x2000020,2);
        /*time13*/    Index[22] = AllocIndexInfo(2,4,0x200000d,1,0x2000021,1);
        /*13*/    Index[23] = AllocIndexInfo(4,8,0x200000d,2,0x2000021,2);
        /*time14*/    Index[24] = AllocIndexInfo(2,4,0x200000e,1,0x2000022,1);
        /*14*/    Index[25] = AllocIndexInfo(4,8,0x200000e,2,0x2000022,2);
        /*time15*/    Index[26] = AllocIndexInfo(2,4,0x200000f,1,0x2000023,1);
        /*15*/    Index[27] = AllocIndexInfo(4,8,0x200000f,2,0x2000023,2);
        /*time16*/    Index[28] = AllocIndexInfo(2,4,0x2000010,1,0x2000024,1);
        /*16*/    Index[29] = AllocIndexInfo(4,8,0x2000010,2,0x2000024,2);
        /*time17*/    Index[30] = AllocIndexInfo(2,4,0x2000011,1,0x2000025,1);
        /*17*/    Index[31] = AllocIndexInfo(4,8,0x2000011,2,0x2000025,2);
        /*time18*/    Index[32] = AllocIndexInfo(2,4,0x2000012,1,0x2000026,1);
        /*18*/    Index[33] = AllocIndexInfo(4,8,0x2000012,2,0x2000026,2);
        /*time19*/    Index[34] = AllocIndexInfo(2,4,0x2000013,1,0x2000027,1);
        /*19*/    Index[35] = AllocIndexInfo(4,8,0x2000013,2,0x2000027,2);
        /*time20*/    Index[36] = AllocIndexInfo(2,4,0x2000014,1,0x2000028,1);
        /*延*/    Index[37] = AllocIndexInfo(2,4,0x2000014,1,0x2000028,1);
        /*br*/    Index[38] = AllocIndexInfo(2,4,0x2000014,1,0x2000028,1);
        /*时*/    Index[39] = AllocIndexInfo(2,4,0x2000014,1,0x2000028,1);
        /*测试*/    Index[40] = AllocIndexInfo(4,8,0x2000014,2,0x2000028,2);
        /*120*/    Index[41] = AllocIndexInfo(2,4,0x2000014,1,0x2000028,1);
        /*20*/    Index[42] = AllocIndexInfo(2,4,0x2000014,1,0x2000028,1);
        /*framecfg*/    Index[43] = AllocIndexInfo(20,40,0x2000015,1,0x2000016,1,0x2000017,1,0x2000018,1,0x2000019,1,0x200001a,1,0x200001b,1,0x200001c,1,0x200001d,1,0x200001e,1,0x200001f,1,0x2000020,1,0x2000021,1,0x2000022,1,0x2000023,1,0x2000024,1,0x2000025,1,0x2000026,1,0x2000027,1,0x2000028,1);
    }
    
    static void InitializeGroup2()
    {
        Index[4] = AllocIndexInfo(4,8,1,2,3,4,5,6,7,1);
        Index[8] = AllocIndexInfo(3,6,3,4,5,6,7,2);
        Index[168] = AllocIndexInfo(3,6,5,3,5,6,7,1);
    }
    
    static void InitializeDocTable()
    {
        DocInfoTable[0x2000001] = 28 ;
        DocInfoTable[0x2000002] = 28 ;
        DocInfoTable[0x2000003] = 29 ;
        DocInfoTable[0x2000004] = 29 ;
        DocInfoTable[0x2000005] = 29 ;
        DocInfoTable[0x2000006] = 29 ;
        DocInfoTable[0x2000007] = 29 ;
        DocInfoTable[0x2000008] = 29 ;
        DocInfoTable[0x2000009] = 29 ;
        DocInfoTable[0x200000a] = 32 ;
        DocInfoTable[0x200000b] = 32 ;
        DocInfoTable[0x200000c] = 32 ;
        DocInfoTable[0x200000d] = 32 ;
        DocInfoTable[0x200000e] = 32 ;
        DocInfoTable[0x200000f] = 32 ;
        DocInfoTable[0x2000010] = 32 ;
        DocInfoTable[0x2000011] = 32 ;
        DocInfoTable[0x2000012] = 32 ;
        DocInfoTable[0x2000013] = 32 ;
        DocInfoTable[0x2000014] = 43 ;
        DocInfoTable[0x2000015] = 30 ;
        DocInfoTable[0x2000016] = 30 ;
        DocInfoTable[0x2000017] = 31 ;
        DocInfoTable[0x2000018] = 31 ;
        DocInfoTable[0x2000019] = 31 ;
        DocInfoTable[0x200001a] = 31 ;
        DocInfoTable[0x200001b] = 31 ;
        DocInfoTable[0x200001c] = 31 ;
        DocInfoTable[0x200001d] = 31 ;
        DocInfoTable[0x200001e] = 34 ;
        DocInfoTable[0x200001f] = 34 ;
        DocInfoTable[0x2000020] = 34 ;
        DocInfoTable[0x2000021] = 34 ;
        DocInfoTable[0x2000022] = 34 ;
        DocInfoTable[0x2000023] = 34 ;
        DocInfoTable[0x2000024] = 34 ;
        DocInfoTable[0x2000025] = 34 ;
        DocInfoTable[0x2000026] = 34 ;
        DocInfoTable[0x2000027] = 34 ;
        DocInfoTable[0x2000028] = 45 ;
    }
   
    
    IndexInitializer()
    {
        InitializeGroup1();
        InitializeGroup2();
        InitializeDocTable();
		ExcuteTfIDF();
    }
};

static IndexInitializer init;

