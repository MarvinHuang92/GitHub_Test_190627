//s04_pointer_lesson_56.cpp

#include <iostream>
#include <stdlib.h>
#include <ctime>  // 用于time函数
#include <cmath>  // 用于数学计算
#include <string>

using namespace std;

/* P55 也可以再看一下，头文件和源文件的格式范例，当然以后想起来再看亦可以 */

// lesson 56
// 定义指针
int def_pointer ()
{
    int a = 10;

    int * p; // * 定义指针
    
    // 将指针与数据进行链接。注意这里赋值时，不用加*
    p = &a; 

    // & 表示对于数据取址，对于数组不需要取址，默认就是地址
    // * 表示解引用，p表示地址，*p表示该地址中存储的数据，也就是a

    *p = 1000; // 修改*p的值和直接修改a的值是等价的
    cout << "a = " << a << endl;
    cout << "*p = " << *p << endl;
    cout << "p = " << p << endl;

    a = 2000; // 修改*p的值和直接修改a的值是等价的
    cout << "a = " << a << endl;
    cout << "*p = " << *p << endl;
    cout << "p = " << p << endl;

    // 在32位操作系统下，所有的指针都是4个字节
    // 在64位操作系统下，所有的指针都是8个字节，无论 int *, double *
    cout << "size of int *:    " << sizeof(int *) << endl;
    cout << "size of double *: " << sizeof(double *) << endl;
    
}

// 空指针和野指针
int empty_wild_pointer ()
{
    // 空指针通常用于指针初始化，但一定要链接数据，不然会报错
    // 地址编号为0-255的内存空间，是系统禁止访问的

    // 定义空指针
    int * p0 = NULL; // * 定义指针, NULL表示空指针（地址编号为0x0）
    int * p1 = (int *)0x0;
    // 定义野指针
    int * p2 = (int *)0x1100;  // 未经申请，手动分配了一个内存地址

    // 以下代码是错误的，运行会直接闪退。空指针/野指针指向非法地址无法访问
    cout << "see what is here: " << *p0 << endl;
    cout << "see what is here: " << *p1 << endl;
    cout << "see what is here: " << *p2 << endl;
}

// 常量指针/指针常量
int coust_pointer () 
{
    int a = 10;

    // 常量指针（英文直译，看下面定义式的顺序即可，int * 表示指针）
    const int * p0 = &a;  // 这样定义，*p0即指向的具体数据值不可修改

    // 指针常量
    int * const p1 = &a;  // 这样定义，p1即内存地址不可修改，不能指向其他地址

    // 两个const，则数据值不可改，且内存地址也不可改
    const int * const p2 = &a;
}

// p61
// 指针遍历数组时，直接对指针++即可。具体它偏移多少字节取决于定义时是 int* 还是 double* 等，例如 int* 会偏移4字节， double* 会偏移8字节
// 所以指针的类型要和数据类型匹配，这里与“所有的指针本身都占用8字节”没关系
int pointer_for_array ()
{
    int arr0[10] = {0,1,2,3,4,5,6,7,8,9};
    int * p0 = arr0;  // 数组不用&取址，直接写数组名即表示首地址
    cout << "starting address: " << p0 << endl;
    p0++;
    cout << "2nd item address: " << p0 << endl;

    double arr1[10] = {0,1,2,3,4,5,6,7,8,9};
    double * p1 = arr1;  // 数组不用&取址，直接写数组名即表示首地址
    cout << "starting address: " << p1 << endl;
    p1++;
    cout << "2nd item address: " << p1 << endl;
}

int main () {
    pointer_for_array();

    system("pause");  // System: send a DOS command, which requires including stdlib.h
    return 0;
}





