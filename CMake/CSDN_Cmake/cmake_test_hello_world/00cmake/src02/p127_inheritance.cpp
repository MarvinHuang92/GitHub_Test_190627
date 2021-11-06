// p127_inheritance.cpp

#include <iostream>
#include <stdlib.h>
#include <ctime>  // 用于time函数
#include <cmath>  // 用于数学计算
#include <string>

using namespace std;


// P127 继承 - 基本语法

/*
有三种继承方式：
继承方式         父类的内容       子类的内容        父类权限的前两项在子类中不变，父类的private在子类中不可访问 【即便不可访问但也会被继承，占用子类的内存】
public          public          public
                protected       protected
                private         不可访问

继承方式         父类的内容       子类的内容        父类权限的前两项在子类中变成 protected，父类的private在子类中不可访问
protected       public          protected
                protected       protected
                private         不可访问

继承方式         父类的内容       子类的内容        父类权限的前两项在子类中变成 private，父类的private在子类中不可访问
private         public          private
                protected       private
                private         不可访问
*/

// 父类/基类
class BaseClass
{
public:
    int m_base_num;
    static int m_A;  // 静态成员变量，需要类外初始化，可以通过类名直接访问，不借助对象

    BaseClass()
    {
        cout << "父类的构造函数" << endl;
    }
    ~ BaseClass()
    {
        cout << "父类的析构函数" << endl;
    }

    void func()
    {
        cout << "父类的成员函数" << endl;
    }
    static void func2()
    {
        cout << "父类的成员函数2" << endl;
    }
};
int BaseClass::m_A = 100;

// 子类/派生类
class SubClass : public BaseClass // 用：表示继承即可，后面的 public 称为【继承方式】
{
public:
    int m_sub_num;
    static int m_A;  // 静态成员变量，需要类外初始化，可以通过类名直接访问，不借助对象

    SubClass()
    {
        cout << "子类的构造函数" << endl;
    }
    ~ SubClass()
    {
        cout << "子类的析构函数" << endl;
    }

    // 和父类同名的成员函数
    void func()
    {
        cout << "子类的成员函数" << endl;
    }
    static void func2()
    {
        cout << "子类的成员函数2" << endl;
    }
};
int SubClass::m_A = 200;

void test_127_00()
{
    SubClass sc;
    sc.m_base_num = 0;
    sc.m_sub_num = 1;

    cout << sc.m_base_num << endl;
    cout << sc.m_sub_num << endl;

}

/*
一个新鲜玩法：【通过VS开发者cmd工具，显示 class 布局】
首先开始菜单打开“Developer Command Prompt for VS2015”，然后cd到源文件所在路径
cl /d1 reportSingleClassLayoutSubClass "p127_inheritance.cpp"
其中 SubClass 是需要查看的类名【注意连着写】，后面跟着源文件名称
结果如下：

p127_inheritance.cpp
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE\xlocale(341): warning C4530: C++ exception handler used, but unwind semantics are not enabled. Specify /EHsc

class SubClass  size(8):
        +---
 0      | +--- (base class BaseClass)
 0      | | m_base_num
        | +---
 4      | m_sub_num
        +---
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE\exception(359): warning C4577: 'noexcept' used with no exception handling mode specified; termination on exception is not guaranteed. Specify /EHsc
Microsoft (R) Incremental Linker Version 14.00.24213.1
Copyright (C) Microsoft Corporation.  All rights reserved.

/out:p127_inheritance.exe
p127_inheritance.obj

【可以得出结论：继承来的private内容，虽然在子类中不可访问，但依然占用子类的内存】

*/

// P130 - 父类/子类 构造和析构的顺序
/*
总结：先构造父类，先析构子类

父类的构造
子类的构造
运行调用函数 test_127_00()
子类的析构
父类的析构
*/

// P131 - 继承的同名成员
/* 
子类的直接用.连接即可，父类的需要增加【作用域】 例子： sc.BaseClass::func(); 
注意，如果子类有【同名成员函数】，则父类中的【重载成员函数】也将被子类覆盖！即使父类的【重载函数】能够从参数识别，也需要加作用域 
*/

// P132 - 继承的同名静态成员
/* 
如果通过对象访问，则和【非静态成员】规则一样
如果通过【类名】直接访问，会出现【两层双冒号】
*/
void test_132_00()
{
    SubClass sc;
    // 通过对象访问
    cout << sc.m_A << endl;                    // 子类的成员变量
    cout << sc.BaseClass::m_A << endl;         // 父类的成员变量
    // 通过类名访问
    cout << SubClass::m_A << endl; 
    cout << SubClass::BaseClass::m_A << endl;  // 两层双冒号，前面是子类类名，后面是父类作用域

    // 非静态成员函数：只能通过对象访问（因为不能保证它不使用非静态成员变量，所以必须先有一个对象）
    sc.func();              // 访问子类 自己的 成员函数
    sc.BaseClass::func();   // 通过子类 访问 继承来的 同名成员函数（需要增加父类的作用域）
    // 静态成员函数：可以通过类名访问
    SubClass::func2();
    SubClass::BaseClass::func2();  // 两层双冒号，前面是子类类名，后面是父类作用域
}

// P133 - 多继承（多个父类） - 不建议使用
class Base1 {
public:
    int m_A = 100;
};
class Base2 {
public:
    int m_A = 200;
};
class Son: public Base1, public Base2   // 两个父类之间用逗号连接，如果有同名的属性，需要加作用域
{
public:
    void show_m_A()
    {
        cout << Base1::m_A << endl;
        cout << Base2::m_A << endl;
    }
};

void test_133_00()
{
    Son s;
    s.show_m_A();
}

// P134 - 菱形继承
/*
会导致最底下那个子类有两份来自不同父类的同名属性，导致资源浪费
解决方法：在两个父类继承同一个祖父类的时候，使用虚继承，例如：
class GrandFather
class Father1: virtual public GrandFather
class Father2: virtual public GrandFather
class Son: public Father1, public Father2

这样，在两个Father类中就不再有实际的 m_A 属性，而是变成一个 vbptr 虚基类指针，也就是各自有一个地址偏移量，而最终指向的是同一个地址
所以son类继承到这个指针后，也可以拿到那个唯一的属性值，修改 Father1::m_A 和修改 Father2::m_A 是等效的
详细的解释看视频 https://www.bilibili.com/video/BV1et411b73Z?p=134&spm_id_from=pageDriver  13分28秒
*/


/*********************************************************************************************************/



int main_127 () {
    // 是否需要显示中文？
    bool ChineseDisplay = true;
    // bool ChineseDisplay = false;

    if (ChineseDisplay) system("chcp 936");  // to set CMD active code page for Chinese display (the default code page is "chcp 437")
    system("cls");

    test_133_00 ();
    
    system("pause");  // System: send a DOS command, which requires including stdlib.h
    return 0;
}


