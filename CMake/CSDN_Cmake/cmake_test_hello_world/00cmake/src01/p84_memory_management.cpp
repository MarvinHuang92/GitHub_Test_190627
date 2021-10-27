// p84_memory_management.cpp

#include <iostream>
#include <stdlib.h>
#include <ctime>  // 用于time函数
#include <cmath>  // 用于数学计算
#include <string>

using namespace std;

// P84 - 程序内存管理
void Hello2 () 
{
    // Dummy Function
    cout << "Hello World Again." << endl;
}

// P85 - 全局变量，局部变量

// 全局变量：写在函数体之外的变量
int g1 = 10;
int g2 = 10;

// 全局常量
const int cg1 = 15;
const int cg2 = 15;

int variables ()
{
    // 局部变量：写在函数体内部的变量
    int a1 = 20;
    int a2 = 20;

    // 局部常量：虽然有const但也在局部内存区
    const int c1 = 30;
    const int c2 = 30;

    // 静态变量：static
    static int s1 = 40;
    static int s2 = 40;

    // 字符串变量
    string str = "hello world";

    cout << "全局变量g1的地址：" << &g1 << endl;
    cout << "全局变量g2的地址：" << &g2 << endl;

    cout << "静态变量s1的地址：" << &s1 << endl;
    cout << "静态变量s2的地址：" << &s2 << endl;

    cout << endl;

    cout << "全局常量cg1的地址：" << &cg1 << endl;
    cout << "全局常量cg2的地址：" << &cg2 << endl;

    cout << "字符串常量的地址：" << &"hello world" << endl; // 字符串常量，不需要提前定义，直接书写即可

    cout << endl;

    cout << "局部常量c1的地址：" << &c1 << endl;
    cout << "局部常量c2的地址：" << &c2 << endl;

    cout << "局部变量a1的地址：" << &a1 << endl;
    cout << "局部变量a2的地址：" << &a2 << endl;

    cout << "字符串变量的地址：" << &str << endl;
    
}

// P86 - 栈区：存放[局部变量]和[形参]
// 注意：不要返回局部变量的地址！

int * func_stack_1() // 注意这个*，表示该函数的返回值是一个地址（可以被指针来接收）
{
    int a = 10;
    // return &a;  // 错误：返回了局部变量的地址，此时编译器会报错

    return 0;  // 注意这里也是错的，返回了空指针，但至少编译不报错
}

void func_stack_2()
{
    // 接收上一个函数返回的值
    int * p = func_stack_1();
    cout << p << endl;  // 显示内存地址
    // cout << *p << endl; // 错误：尝试显示该内存中的数据（在func_stack_1运行结束后此内存就被释放掉了）
}

// P87 - 堆区：类似于栈，但是由程序员自己管理开辟和释放，可以返回其地址

int * func_heap_1() // 注意这个*，表示该函数的返回值是一个地址（可以被指针来接收）
{
    int *p = new int(10);  // 利用 new 来开辟堆区内存，new 的返回值就是开辟的地址本身
    return p;  // 返回堆区变量的地址
}

void func_heap_2()
{
    // 接收上一个函数返回的值
    int * p = func_heap_1();
    cout << p << endl;  // 显示内存地址
    cout << *p << endl; // 尝试显示该内存中的数据

    delete p;  // 释放堆区中的内存

    cout << *p << endl; // 再次尝试显示该内存中的数据，会得到随机的乱码
}

// P88 - new 创建一个堆区的数组
int * func_heap_arr_1() // 注意这个*，表示该函数的返回值是一个地址（可以被指针来接收）
{
    int * arr = new int[10];  // 注意使用数组[]和普通变量()的区别

    for (int i=0; i<10; i++)
    {
        arr[i] = i + 100;  // 给10个元素分别赋值 100 -109
    }

    return arr;  // 返回堆区变量的地址
}

void func_heap_arr_2()
{
    // 接收上一个函数返回的值
    int * arr = func_heap_arr_1();
    cout << arr << endl;  // 显示内存地址
    
    for (int i=0; i<10; i++)
    {
        cout << arr[i] << endl; // 尝试显示该内存中的数据
    }
    
    delete[] arr;  // 释放堆区中的内存 (对于数组，释放时用delete[])

    cout << arr[0] << endl; // 再次尝试显示该内存中的数据，会得到随机的乱码
}


/*********************************************************************************************************/



int main_84 () {
    // 是否需要显示中文？
    bool ChineseDisplay = true;
    // bool ChineseDisplay = false;

    if (ChineseDisplay) system("chcp 936");  // to set CMD active code page for Chinese display (the default code page is "chcp 437")
    system("cls");

    func_heap_arr_2 ();
    
    system("pause");  // System: send a DOS command, which requires including stdlib.h
    return 0;
}


