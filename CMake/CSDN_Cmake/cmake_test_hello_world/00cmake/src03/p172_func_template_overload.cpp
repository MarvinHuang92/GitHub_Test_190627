// p172_func_template_overload.cpp

#include <iostream>
#include <stdlib.h>
#include <ctime>  // 用于time函数
#include <cmath>  // 用于数学计算
#include <string>

using namespace std;

#include <fstream> // 用于文件操作

// P172 - 函数模板的重载规则

/*
1. 优先调用普通函数，而不是函数模板
2. 可以通过“空模板参数 <> ”强制调用函数模板
3. 模板可以重载
4. 如果函数模板可以产生更好的匹配，则优先调用函数模板  【如果类型不匹配，但是普通函数可以隐式类型转换，则模板的优先级高于“隐式类型转换”】
*/

void MyPrint(int a, int b)
{
    cout << "调用普通函数" << endl;
}

template<class T>
void MyPrint(T a, T b)
{
    cout << "调用模板 - 两个参数" << endl;
}

template<class T>
void MyPrint(T a, T b, T c)
{
    cout << "调用模板 - 三个参数" << endl;
}

// 测试函数： 分别用 int 数组和 char 数组测试
void test_172()
{
    int a = 10;
    int b = 20;
    int c = 30;

    char d = 'D';
    char f = 'F';

    MyPrint(a, b);          // 1. 两种都可以实现，则调用普通函数
    MyPrint<>(a, b);        // 2. 空模板参数 <> 强制调用模板
    MyPrint<>(a, b, c);     // 3. 重载后的模板（三个参数）
    MyPrint(d, f);          // 4. 函数模板可以产生更好的匹配，则优先调用函数模板，而不是需要类型转换的普通函数

}


/*********************************************************************************************************/



int main_172 () {
    // 是否需要显示中文？
    // bool ChineseDisplay = true;
    bool ChineseDisplay = false;

    if (ChineseDisplay) system("chcp 936");  // to set CMD active code page for Chinese display (the default code page is "chcp 437")
    system("cls");

    test_172 ();
    
    system("pause");  // System: send a DOS command, which requires including stdlib.h
    return 0;
}


