#include <stdio.h>
/*显示输入中各个字母，数字，空格的频度直方图，版本1：横向显示*/

int main()
{
	int i, j, c;
	int alphabet[26], num[10], wspace, others;
	
	wspace = others = 0;
	for (i = 0; i < 26; ++i)
		alphabet[i] = 0;
	for (i = 0; i < 10; ++i)
		num[i] = 0;
	
	while ((c = getchar()) != EOF)
		if (c >= 'a' && c <= 'z')
			++alphabet[c-'a'];
		else if (c >= 'A' && c <= 'Z')  //注意大小写都要统计
			++alphabet[c-'A'];
		else if (c >= '0' && c <= '9')
			++num[c-'0'];
		else if (c == ' ' || c == '\t')
			++wspace;
		else if (c == '\n')
			;							//这次不考虑换行符
		else
			++others;
	
	for (i = 0; i < 26; ++i) {
		printf("%c: ", ('A'+i));		//%c可以直接将ASCII码的数字转换成字符，但不要用%s
		for (j = 0; j < alphabet[i]; ++j)//如果开始就不满足第二个条件，即alphabet = 0时，for是可以一次都不执行的
			printf("#");
		printf("\n");
	}
	
	for (i = 0; i < 10; ++i) {
		printf("%c: ", ('0'+i));
		for (j = 0; j < num[i]; ++j)
			printf("#");
		printf("\n");
	}
	
	printf("SPACE: ");
	for (j = 0; j < wspace; ++j)
		printf("#");
	printf("\n");
		
	printf("OTHERS: ");
	for (j = 0; j < others; ++j)
		printf("#");
	printf("\n");

	getchar();
}