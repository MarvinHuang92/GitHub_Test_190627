#include <iostream>
using namespace std;

// 全局变量声明
int g = 20;

int func()
{
	g = 5;
	return 0;
}

int main()
{
	// 局部变量声明
	int g; //= 10;

	cout << g;

	return 0;
}