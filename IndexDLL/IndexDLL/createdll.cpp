#include"stdafx.h"  //ע�ⲻҪ����������ͷ�ļ�
//#include"createdll.h"
#include<iostream>

#define DLLEXPORT extern "C" __declspec(dllexport)
DLLEXPORT int __stdcall add(int a, int b) {
	return a + b;
}