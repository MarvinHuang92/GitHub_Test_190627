#include <stdio.h>
/* count digits, white space, others 统计输入的0-9各个数字出现的次数*/
int main()
{
	int c, i, nwhite, nother;			//声明变量
	int ndigit[10];
	
	nwhite = nother = 0;				//赋值
	for (i = 0; i < 10; ++i)
		ndigit[i] = 0;
	
	while ((c = getchar()) != EOF)
		if (c >= '0' && c <= '9')
			++ndigit[c-'0'];			//中括号内是重点！！
		else if (c == ' ' || c == '\n' || c == '\t')
			++nwhite;
		else
			++nother;
		
	printf("digits =");
	for (i = 0; i < 10; ++i)
		printf(" %d", ndigit[i]);
	printf(", white space = %d, other = %d\n", nwhite, nother);
	getchar();
}