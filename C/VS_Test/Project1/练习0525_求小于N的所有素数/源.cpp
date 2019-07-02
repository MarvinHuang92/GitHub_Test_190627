#include <stdio.h>
#include <math.h>

/* 步骤说明：
1. 给定最大范围N，用for循环遍历2~N的所有自然数i

单独定义一个判断函数：
2. 求i的算术平方根，截取整数部分，记作i_sqrt
3. 遍历从2~i_sqrt的所有整数j
4. 看i能否被j整除，如果是，则i为合数，跳出循环；否则i为质数
*/

/* 给定最大范围N，超过6位数可能溢出 */
#define N 200000

/* 定义一个判断函数，输入一个正整数，如果是素数返回1 */
int isprime(unsigned int i)   //C语言在C99标准之前是没有bool类型的，C++则有，这里不使用bool而用int类型返回，效果一样的
{
	int i_sqrt = (int)sqrt(i);   //sqrt函数的输入和输出都是double类型，i定义为int会在输入时自动升级为double，但输出需要手动降级成int（去掉小数部分）
	
	int j;
	for (j = 2; j <= i_sqrt; j++)//对于i=2或3的情况，平方根小于2，不满足第二个条件，直接不执行这个for，并返回1（是素数）
		if (i % j == 0)
			return 0;
	return 1;
}

int main1()  //这是简单的版本，每判断一个数后，就直接打印
{
	printf("不大于%d的素数有：\n", N);

	int i;
	for (i = 2; i <= N; i++)
		if (isprime(i))
			printf("%d\n", i);
}

int main()
//这是稍复杂的的版本，要统计总共有多少个素数（count）
//由于必须等到所有判断都做完才能知道count是多少，但又要把count的值显示在最前面，所以要准备一个数组存放判断结果，留到最后再打印
{
	int prime[N];   //其实素数的总数远远小于N，但数组长度设为N，比较方便
	int count = 0;  //用来计数，同时作为数组存储的下标

	int i;
	for (i = 2; i <= N; i++)
		if (isprime(i)) {
			prime[count++] = i;  //将第count个素数存放进数组的第count个位置（从第0个开始）；第一个素数放在prime[0]，然后++，正好把count加到了1
		}

	printf("不大于%d的素数有%d个，分别是：\n", N, count);

	for (i = 0; i < count; i++)
		printf("%d%c", prime[i] , (i % 10 == 9) || (i == count - 1) ? '\n' : '\t');  //依次打印数组中的素数，每10个一行，且最后一个强制换行
}