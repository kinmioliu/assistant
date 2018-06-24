#include <iostream>
#include "IndexMng.h"
using namespace std;

#pragma comment(lib,"IndexMng.lib")

int main()
{
	cout << "this is IndexMng Tester!\n";
	int testdll = 0;
    testdll = sum(5, 6);
	cout << testdll << endl;

	StructResutlPointer p = QueryDocIdByTokens(0, 3, 4, 8, 0,
		0, 0, 0, 4, 0,
		0, 0, 0, 0, 0,
		0, 0, 0, 0, 0,
		1, 3,0x02000000);
	cout << p->PageCnt << " " << p->ResultCnts << endl;

	system("pause");
	return 0;
}
