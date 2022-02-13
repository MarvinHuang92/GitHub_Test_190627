// p167_func_template.cpp

#include <iostream>
#include <stdlib.h>
#include <ctime>  // 用于time函数
#include <cmath>  // 用于数学计算
#include <string>

using namespace std;

#include <fstream> // 用于文件操作

// P167 - 模板
// 适用于逻辑代码本身可以复用的情况，只有不确定的 返回值 和 形参 类型

// 只能出现一次template<>， 否则会报错 error: too many template-parameter-lists

/*** 函数模板：template 下一行紧跟着一个函数 ***/
// 声明模板，防止后面编译器看到 "T" 以后报错
template<typename T> 

//或者用 class 关键字亦可
// template<class T>

// 功能函数，交换两个数，这两个数的数据类型用T代替
void MySwap(T &a, T &b)
{
    T temp = a;
    a = b;
    b = temp;
}

/*** 函数模板 - 结束 ***/

template<class T>
T MyAdd (T a, T b)
{
    return a + b;
}

// 使用模板函数
void test_167()
{
    // 方法1：实参的类型可以自动传给形参的类型
    int a = 10;
    int b = 20;
    MySwap(a, b);  

    // 方法2：手动指定数据类型，注意这个 <> 指代的是 template<typename T> 在这一次需要表现为 double 类型
    // 这个方法的好处：支持隐式类型转换，例如声明了使用 <int>，参数传入 char 或者 float，依然可以运行
    double c = 10.5;
    double d = 20.5;
    MySwap<double>(c, d);

    int e = 10;
    float f = 70.0;
    char g = 'G';  // ASCII F = 0x47 = 71
    // MyAdd<int>(e, f);

    cout << "a = " << a << endl;
    cout << "b = " << b << endl;

    cout << "c = " << c << endl;
    cout << "d = " << d << endl;

    cout << "e + f = " << MyAdd<int>(e, f) << endl;
    cout << "e + g = " << MyAdd<int>(e, g) << endl;
}

/*** 类模板： template 下一行紧跟着类定义 ***/
template<class T>
class MyClass {

};

/*** 类模板 - 结束 ***/


// P170 利用模板写一个给 int 或者 char 通用的数组降序排序函数

// 用于打印数组的所有元素
template<class T>
void MyPrintArr(T arr[], int len)
{
    for (int i = 0; i < len; i++)
    {
        cout << arr[i] << " ";
    }
    cout << endl;
}

// 用于排序
template<class T>
void MySort(T arr[], int len)  // 第二个参数是数组长度
{
    // “选择排序”算法（就是冒泡方法）
    for (int i = 0; i < len; i++)
    {
        // 从第一个元素开始，先假设它就是最大值，下标记作max（其实就是 i）
        int max = i;
        for (int j = i+1; j < len; j++)
        {
            // 如果认定的最大值比 j 还要小，交换这两个值
            if (arr[max] < arr[j])
            {
                // 这里利用了另一个模板函数，交换两个值
                MySwap(arr[max], arr[j]);
            }
        }
    }
    // 打印排序后的结果
    MyPrintArr(arr, len);
}

// 测试函数： 分别用 int 数组和 char 数组测试
void test_170()
{
    int Arr_1[] = {5,2,3,1,4,4,8,8};
    int length_1 = sizeof(Arr_1) / sizeof(Arr_1[0]);

    char Arr_2[] = "abcdeffgg";
    int length_2 = sizeof(Arr_2) / sizeof(Arr_2[0]);

    MySort(Arr_1, length_1);
    MySort(Arr_2, length_2);
}


/*********************************************************************************************************/



int main_167 () {
    // 是否需要显示中文？
    // bool ChineseDisplay = true;
    bool ChineseDisplay = false;

    if (ChineseDisplay) system("chcp 936");  // to set CMD active code page for Chinese display (the default code page is "chcp 437")
    system("cls");

    test_167 ();
    test_170 ();
    
    system("pause");  // System: send a DOS command, which requires including stdlib.h
    return 0;
}


