#include <stdio.h>
/* binsearch: find x in v[0] <= v[1] <= ... <= v[n-1] */
// 在升序数组v[]中查找特定的数值x，返回它的数组下标


int elow, ehigh; //声明外部变量，用于存储low和high的结果


int binsearch(int x, int v[], int n) //原始函数
{
	int low, high, mid;

	low = 0;
	high = n - 1;

	while (low <= high) {
		mid = (low + high) / 2;  //自动向下取整
		if (x < v[mid])
			high = mid - 1;
		else if (x > v[mid])
			low = mid + 1;
		else {/* 找到了匹配值，就是v[mid] */
			elow = low;
			ehigh = high;
			return mid;
		}
	}
	// 如果跳出了while循环，一定是low = high + 1（两者大小反过来了）
	elow = low;
	ehigh = high;
	return -1;
	/* 没有匹配值 */
}

int binsearch2(int x, int v[], int n) //自己写的新函数，在while中只是用一个if判断
{
	int low, high, mid;

	low = 0;
	high = n - 1;

	while (low < high) {  //这里去掉等于的条件，否则会无限循环
		mid = (low + high) / 2;  //自动向下取整
		if (x > v[mid])  //这里使用大于条件，而不能用小于条件，因为mid总是向下取整的，反过来可能导致无限循环
			low = mid + 1;
		else
			high = mid;
	}
	// 如果跳出了while循环，一定是low = high，而不可能有low = high + 1
	elow = low;
	ehigh = high;
	if (x == v[low])
		return low;  //这个用low或者high都可以，两者总是相等的
	else
		return -1;
	/* 没有匹配值 */
}

int binsearch3(int x, int v[], int n) //将2中的判断条件颠倒，测试可能的死循环
{
	int low, high, mid;

	low = 0;
	high = n - 1;

	while (low < high) {
		mid = (low + high) / 2;
		if (x < v[mid])  //这里的条件和2相反
			high = mid - 1;
		else             //如果符合这一条件，会出现死循环
			low = mid;
	}

	elow = low;
	ehigh = high;
	if (x == v[low])
		return low;
	else
		return -1;
	/* 没有匹配值 */
}

int main()
{
	int x = 8;
	int v[12];
	int i;

	for (i = 0; i < 12; ++i)
		v[i] = i * 2;  //初始化数组为0,2,4...22

	int pos = binsearch2(x, v, 12);

	printf("position = %d\nlow = %d\nhigh = %d\n", pos, elow, ehigh);

}