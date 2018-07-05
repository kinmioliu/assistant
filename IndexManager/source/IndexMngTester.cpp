#include <iostream>
#include "IndexMng.h"
using namespace std;
#ifdef _WIN64
#pragma comment(lib,"IndexMng.lib")
#endif

int main()
{
	cout << "this is IndexMng Tester!\n";
	int testdll = 0;
    testdll = sum(5, 6);
	cout << testdll << endl;

	StructResutlPointer p = QueryDocIdByTokens(1, 2, 0, 0, 0,
		0, 0, 0, 0, 0,
		0, 0, 0, 0, 0,
		0, 0, 0, 0, 0,
		1, 10, 0x02000000);
	cout << p->PageCnt << " " << p->ResultCnts << endl;

#ifdef _WIN64
	system("pause");
#endif
    
	return 0;
}
