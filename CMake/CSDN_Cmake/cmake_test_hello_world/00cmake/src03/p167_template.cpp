// p167_template.cpp

#include <iostream>
#include <stdlib.h>
#include <ctime>  // 用于time函数
#include <cmath>  // 用于数学计算
#include <string>

using namespace std;

#include <fstream> // 用于文件操作

// P167 - 模板

// 分为函数模板，和类模板 （*** 如果 template 后面紧接着一个函数就是函数模板）

// 声明模板，防止后面编译器看到 "T" 以后报错
template<typename T> 
//或者用 class 关键字亦可
// template<class T2>

// 只能出现一次template<>， 否则会报错 error: too many template-parameter-lists


// *** 函数模板：适用于逻辑代码本身可以复用的情况，只有不确定的 返回值 和 形参 类型
// 功能函数，交换两个数，这两个数的数据类型用T代替
void MySwap(T &a, T &b)
{
    T temp = a;
    a = b;
    b = temp;
}

// 使用模板函数
void test_167()
{
    // 方法1：实参的类型可以自动传给形参的类型
    int a = 10;
    int b = 20;
    MySwap(a, b);  

    // 方法2：手动指定数据类型，注意这个 <> 指代的是 template<typename T> 在这一次需要表现为 double 类型
    double c = 10.5;
    double d = 20.5;
    MySwap<double>(c, d);

    cout << "a = " << a << endl;
    cout << "b = " << b << endl;

    cout << "c = " << c << endl;
    cout << "d = " << d << endl;

}





/*********************************************************************************************************/



int main () {
    // 是否需要显示中文？
    // bool ChineseDisplay = true;
    bool ChineseDisplay = false;

    if (ChineseDisplay) system("chcp 936");  // to set CMD active code page for Chinese display (the default code page is "chcp 437")
    system("cls");

    test_167 ();
    
    system("pause");  // System: send a DOS command, which requires including stdlib.h
    return 0;
}


