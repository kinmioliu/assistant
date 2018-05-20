#include"stdafx.h"  //注意不要忘了添加这个头文件
//#include"createdll.h"
#include<iostream>

#define DLLEXPORT extern "C" __declspec(dllexport)
DLLEXPORT int __stdcall add(int a, int b) {
	return a + b;
}