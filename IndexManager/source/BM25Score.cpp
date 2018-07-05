//
//  BM25Score.cpp
//  IndexMng
//
//  Created by 刘进谋 on 2018/7/1.
//  Copyright © 2018年 刘进谋. All rights reserved.
//

#include "BM25Score.h"
#include <math.h>

const int k2 = 100;
const float k1 = 1.2;
const float b = 0.75;
const float R = 0.0;

float compute_K(int dl, float avdl)
{
    return k1 * ((1-b) + b * (float(dl)/float(avdl)) );
}

//def compute_K(dl, avdl):
//return k1 * ((1-b) + b * (float(dl)/float(avdl)) )


float CalculateBM25(int n, int f, int qf, int r, int N, int dl, float advl)
{
    float K = compute_K(dl, advl);
    float mi =   ( (r + 0.5) / (R - r + 0.5) ) / ( (n - r + 0.5) / (N - n - R + r + 0.5));
    
    float first = log( ( (r + 0.5) / (R - r + 0.5) ) / ( (n - r + 0.5) / (N - n - R + r + 0.5)));
    float second = ((k1 + 1) * f) / (K + f);
    float third = ((k2+1) * qf) / (k2 + qf);
    return first * second * third;
}
//
//float score_BM25(n, f, qf, r, N, dl, avdl):
//K = compute_K(dl, avdl)
//first = log( ( (r + 0.5) / (R - r + 0.5) ) / ( (n - r + 0.5) / (N - n - R + r + 0.5)) )
//second = ((k1 + 1) * f) / (K + f)
//third = ((k2+1) * qf) / (k2 + qf)
//return first * second * third

