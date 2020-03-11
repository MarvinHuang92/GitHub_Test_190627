#include <stdio.h>
/* copy input to output; 1st version 将输入重新输出一遍*/
int main()
{
	int c;
	
	while ((c = getchar()) != EOF) 
		putchar(c);
}