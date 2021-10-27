// p89_reference.cpp

#include <iostream>
#include <stdlib.h>
#include <ctime>  // 用于time函数
#include <cmath>  // 用于数学计算
#include <string>

using namespace std;

// P89 引用：给变量起一个别名，二者指向同一地址
void reference () 
{
    int a = 10;
    
    // 创建引用  (&新名字 = 旧名字)，【这个引用关系不可再更改】
    int &b = a;
    // 对此内存重新赋值
    b = 20;

    cout << "a = " << a << endl;
    cout << "b = " << b << endl;

}

// P91 引用传递：第三种函数参数传递方法（可以影响实参，且书写比地址传递简单）
// 地址传递可以看 s04 - P62

// 引用传递，相当于形参中的&a指向了实参a的地址，构建了一个引用 "int (形参)&a = (实参)a"
void swap_3 (int &a, int &b)
{
    int temp = 0;
    temp = a;
    a = b;
    b = temp;

    cout << "swap_3 a = " << a << endl;
    cout << "swap_3 b = " << b << endl;
}

void external_swap ()
{
    int a = 10;
    int b = 20;

    swap_3(a, b);  // 外部调用时的格式和普通的传递一样，但这里的形参会影响实参
    cout << "external a = " << a << endl;
    cout << "external b = " << b << endl;
}


// P92 注意事项：不要传递局部变量引用，静态变量可以
int& parseLocalRef () 
{
    // int a = 0;  // 错误，会闪退，因为a存放在栈区，该函数运行后就被释放
    static int a = 0;  // 正确，a存放在全局区，整个程序结束前都不会释放
    return a;
}

void parseLocalRef_extern ()
{
    int& ref = parseLocalRef();
    cout << ref << endl;
    cout << ref << endl;
    cout << ref << endl;

    // 特别注意，返回值是引用的函数，可以作为左值被赋值，等效于直接将a赋值，因为static int a 和 ref2 指向同一个地址
    int& ref2 = parseLocalRef();
    parseLocalRef() = 1000;
    cout << ref2 << endl;
    cout << ref2 << endl;
    cout << ref2 << endl;

}

// P94 常量引用：用在形参中防止错误的修改实参
// 在形参中加入const，后面如果有修改操作会直接编译报错
void swap_4 (const int &a, const int &b)
{
    int temp = 0;
    temp = a;
    // a = b;  // 这两行无法通过编译，报错 error: assignment of read-only reference 'a'
    // b = temp;

    cout << "swap_4 a = " << a << endl;
    cout << "swap_4 b = " << b << endl;
}




/*********************************************************************************************************/



int main_89 () {
    // 是否需要显示中文？
    bool ChineseDisplay = true;
    // bool ChineseDisplay = false;

    if (ChineseDisplay) system("chcp 936");  // to set CMD active code page for Chinese display (the default code page is "chcp 437")
    system("cls");

    parseLocalRef_extern ();
    
    system("pause");  // System: send a DOS command, which requires including stdlib.h
    return 0;
}


