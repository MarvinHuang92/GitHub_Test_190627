#include <stdio.h>

/* 步骤说明：

从0开始，把当前数字+1，然后比较新的数是否大于旧的数
如果不大于，说明已经到了最大限制
例如127 + 1= -128，而判断大小时能知道-128 < 127，于是同时知道了上限和下限

*/

int main()
{
	int a, b;
	long c, d;
	short e, f;

	for (b = (a = 0) + 1; a < b; b = (++a) + 1)  //注意顺序，先将a自加，然后再赋值给b
		;
	for (d = (c = 0) + 1; c < d; d = (++c) + 1)
		;
	for (f = (e = 0) + 1; e < f; f = (++e) + 1)
		;
	printf("int\t上限：%d\t下限：%d\n", a, b); //当a到达上限时，b = a + 1刚好就是下限，不需要另外计算
	printf("long\t上限：%d\t下限：%d\n", c, d);
	printf("short\t上限：%d\t\t下限：%d\n", e, f);
}