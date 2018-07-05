//
//  BM25Score.hpp
//  IndexMng
//
//  Created by 刘进谋 on 2018/7/1.
//  Copyright © 2018年 刘进谋. All rights reserved.
//

#ifndef BM25Score_hpp
#define BM25Score_hpp

#include <stdio.h>
float compute_K(int dl, float avdl);
float CalculateBM25(int n, int f, int qf, int r, int N, int dl, float advl);

#endif /* BM25Score_hpp */
