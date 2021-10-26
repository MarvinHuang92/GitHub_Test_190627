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

// p62 - 传值和传址
// 两个函数的对比，第一个是普通的传值，形参不影响实参；第二个是传递地址（形参是指针）函数会直接对与实参进行操作
void swap_1 (int a, int b)
{
    int temp = 0;
    temp = a;
    a = b;
    b = temp;

    cout << "swap_1 a = " << a << endl;
    cout << "swap_1 b = " << b << endl;
}

void swap_2 (int * p0, int * p1)
{
    int temp = 0;
    temp = *p0;
    *p0 = *p1;
    *p1 = temp;

    cout << "swap_2 a = " << *p0 << endl;
    cout << "swap_2 b = " << *p1 << endl;
}

void external_swap ()
{
    int a = 10;
    int b = 20;
    swap_1(a, b);
    cout << "external a = " << a << endl;
    cout << "external b = " << b << endl;

    swap_2(&a, &b);
    cout << "external a = " << a << endl;
    cout << "external b = " << b << endl;
}

// P63 - 封装一个函数实现数组的冒泡排序
// 和之前的不同是：这个数组是定义在函数之外，作为参数传递进来的
//用于打印array的内部函数
void printArray(int * arr, int length)
{
    for (int i=0; i< length; i++)
    {
        cout << arr[i] << endl;
    }
}

//用于排序的内部函数
void array_bubble_sorting_with_address_parse (int * arr, int length) // 这个指针是数组的首地址
{
    //如果试图在函数内部获取数组长度，这样是不行的，这样得到的是2（指针本身长度8/int类型的长度4）
    //所以需要在外部传入数组的长度
    // int length = sizeof(arr) / sizeof(arr[0]);
    // cout << "length of array: " << length << endl;

    //开始排序
    int temp = 0;
    for (int i=0; i<length; i++)
    {
        for (int j=0; j<length-i; j++)
        {
            if (arr[j]>arr[j+1])
            {
                temp = arr[j];
                arr[j] = arr[j+1];
                arr[j+1] = temp;
            }
        }
    }
}

//外部函数
void external_array_bubble_sorting_with_address_parse ()
{
    int arr[10] = {250, 350, 400, 750, 600, 900, 120, 95, 0, 520};
    //首先获取数组的长度
    int length = sizeof(arr) / sizeof(arr[0]);
    cout << "length of array: " << length << endl;

    //首先打印数组一次
    cout << "\narray before sorting" << endl;
    printArray(arr, length);

    //排序
    array_bubble_sorting_with_address_parse (arr, length);

    //结束后再打印数组一次
    cout << "\narray after sorting" << endl;
    printArray(arr, length);
}

int main4 () {
    external_array_bubble_sorting_with_address_parse ();

    system("pause");  // System: send a DOS command, which requires including stdlib.h
    return 0;
}





