#include <stdio.h>
/* 将十六进制转换为相对应的整型数，可能有前缀0x或0X， 允许包含0-9，a-f，A-F */

#define MAX 100

int htoi(char s[])
{
	int i, n, a, c;

	if (s[1] == 'x' || s[1] == 'X')
		a = 2;							//如果有前缀，跳过前两位数
	else a = 0;

	n = 0;
	for (i = a; s[i] >= '0' && s[i] <= '9' || s[i] >= 'A' && s[i] <= 'F' || s[i] >= 'a' && s[i] <= 'f'; ++i) {
		if (s[i] >= '0' && s[i] <= '9')
			c = s[i] - '0';				//c表示当前位转换为十进制的结果
		else if (s[i] >= 'A' && s[i] <= 'F')
			c = s[i] - 'A' + 10;
		else
			c = s[i] - 'a' + 10;
		n = 16 * n + c;
	}
	return n;
}

int main()
{
	int i, c;
	char s[MAX];

	printf("请输入一个十六进制数，以小数点(.)结尾\n\n");

	while (true) {
		for (i = 0; (c = getchar()) != '.'; ++i)
			s[i] = c;
		s[i] = '\0';

		printf("%s对应的十进制数为：%d\n\n",s, htoi(s));  //当前的问题：如果小数点后面有别的数字下一次会出错；从第二次开始输出总是0
	}
}