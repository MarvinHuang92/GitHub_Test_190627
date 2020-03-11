#include <stdio.h>

int main()
{
	enum MONTH {Jan = 1, Feb, Mar, Apr, May = 1} month;  //第一个MONTH是“人造的”类型名字，后面的month才是变量名字

	month = Jan;
	printf("%d\n", month);

	month = May;
	printf("%d\n", month);
	
	getchar();
	return 0;
}