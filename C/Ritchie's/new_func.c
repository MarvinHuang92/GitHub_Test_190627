#include <stdio.h>
/* 自己写一个求幂的函数 */


/* 这个是通常的写法

int power(int base, int n) //在声明函数的时候，也要声明形参的类型；第一个int是函数自身的返回值类型（即ruturn power）
{
	int i, power;		   //这里面声明的是局部变量
	power = 1;
	for (i=1; i <= n; ++i) //如果开始就不满足第二个条件，for是可以一次都不执行的
		power = power * base;
	return power;
}
*/

//给出一个新的power函数，好处是，利用传递进来的n值自减来计数，而不用一个额外的int i
//注意这里的n是传递后的值（相当于power()中的局部变量），不会改变主调函数的n值

int power(int base, int n)
{
	int power;		   //这里面不再声明用于计数的i

	for (power = 1; n > 0; --n) //注意可以直接在这里给power赋值，for的三段中涉及的参数可以互相无关，第一个是power，后两个是n
		power = power * base;
	return power;
}
	
int main()
{
	int p1 = power(2, 0), p2 = power(2, 1), p3 = power(2, 2);
	printf("%d %d %d", p1, p2, p3);
	getchar();
}	