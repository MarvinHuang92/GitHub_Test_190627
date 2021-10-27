// p95_func_enhanced.cpp

#include <iostream>
#include <stdlib.h>
#include <ctime>  // 用于time函数
#include <cmath>  // 用于数学计算
#include <string>

using namespace std;

// P95 函数参数的默认值
int func_default_attr(int a=10, int b=20, int c=30)
{
    return a+b+c;
}

// 错误的例子，如果左边的参数有默认值，右边的也一定要有
// 编译报错 error: default argument missing for parameter 2 of 'int func_default_attr(int, int, int)'
// int func_default_attr(int a=10, int b, int c)
// {
//     return a+b+c;
// }

// 注意：“函数声明”和“函数实现”中最多只有一处默认参数，否则会报错 note: previous specification in 'int func_default_attr2(int, int, int)' here
// 声明中不写默认参数
int func_default_attr2 (int a, int b, int c);

// 外部调用
void func_default_attr_extern ()
{
    int sum = func_default_attr(15);
    cout << sum << endl;

}

// 函数实现写默认参数
int func_default_attr2(int a=10, int b=10, int c=10)
{
    return a+b+c;
}

// 占位参数（形参只写数据类型，不写变量名）仅仅用于占位，确保调用的时候一定传了足够数量的参数进来
// 注意第二个占位参数没有名字，但却可以有默认值
void func_dummy_attr(int a, int = 10) 
{
    cout << "Dummy Func." << endl;
}

// *** P97 函数重载（重要！） *** //  Function Overloading
// 1. 允许重复的函数名称
// 2. 在同一个作用域
// 3. 函数的参数（顺序，类型，数量）不同，并通过调用时传入的参数类型来决定调用哪一种重载
// 4. 函数的返回值类型必须相同

// 重载实例，针对上面的 func_dummy_attr() 函数，将其中一个参数的类型改掉
void func_dummy_attr(int a, string b = "10.0") 
{
    cout << "Dummy Func Overloaded." << endl;
}

// “引用”作为重载条件时，不加const只接受局部变量，加const接受常量
void func_dummy_ref(int & a) 
{
    cout << "Dummy Func Overloaded - Ref without Const." << endl;
}

void func_dummy_ref(const int & a) 
{
    cout << "Dummy Func Overloaded - Ref with Const." << endl;
}

// 外部调用
void func_dummy_attr_overload()
{
    func_dummy_attr (10, 10);
    func_dummy_attr (10, "10");  // 根据参数的类型来识别具体调用哪个函数

    int a = 10; // 局部变量
    func_dummy_ref(a);           // 输入局部变量会调用不加const的函数
    func_dummy_ref(10);          // 输入常量，会调用加const的函数

    // 注意如果函数有默认参数时候，编译经常会遇到“二义性”报错，尽量避免在重载函数中写默认参数

}

/*********************************************************************************************************/



int main_95 () {
    // 是否需要显示中文？
    bool ChineseDisplay = true;
    // bool ChineseDisplay = false;

    if (ChineseDisplay) system("chcp 936");  // to set CMD active code page for Chinese display (the default code page is "chcp 437")
    system("cls");

    func_dummy_attr_overload ();
    
    system("pause");  // System: send a DOS command, which requires including stdlib.h
    return 0;
}


