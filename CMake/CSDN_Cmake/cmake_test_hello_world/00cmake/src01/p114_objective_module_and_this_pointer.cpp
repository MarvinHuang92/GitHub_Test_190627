// p114_objective_module_and_this_pointer.cpp

#include <iostream>
#include <stdlib.h>
#include <ctime>  // 用于time函数
#include <cmath>  // 用于数学计算
#include <string>

using namespace std;

// P114 对象模型和this指针
/*
成员变量和成员函数分开存储：
只有非静态的成员变量/函数才位于对象（实例）上
静态的变量/函数和类本身一起（即使这时候没有创建任何对象实例）
*/

class Empty 
{
};

class C1 
{
public:
    int a;                  // 非静态成员变量 （只有它放在具体类实例的地址中）
    static int b;           // 静态成员变量   （后面三种都在全局区）

public:
    int func01 () {};       // 非静态成员函数
    static int func02() {}; // 静态成员函数

    // 下面这两函数留给P115使用
    C1(int a)  // 构造函数：故意写“形参和成员变量同名”，但不建议这么做，成员变量建议用m_开头
    {
        this->a = a; // 前一个a是成员变量(调用此函数的那个对象里面的变量)，后一个是形参
    }

    // 【重要：一开始的返回值要是引用 C1&，而不是类本身 C1】，否则也不会报错，而是会创建一个新的C1类成员！
    C1& PersonAddAge(C1 &c) // 非静态成员函数：让数字a增加“另一个类成员的a的值”
    {
        this->a += c.a;
        return *this;  // 返回值是：调用此函数的成员自身
    }
};

void test_114_00 ()
{
    Empty e;
    cout << "空对象占用的内存空间是： " << sizeof(e) << endl;  // 1个字节，纯粹为了占位，防止不同的空对象占用相同的内存地址

    C1 c1(10);
    cout << "具有一个整形属性的对象占用的内存空间是： " << sizeof(c1) << endl;  // 4个字节，因为只有一个int属性
}

/*
结论：
除了“非静态成员变量”放在类成员实例的内存中（占用具体实例的栈地址长度）
其余三种：静态成员变量，静态/非静态成员函数，都放在全局区，不占用具体实例的地址
因为后三种不需要随着类实例走，整个类都共享一个定义或值即可
*/

// P115 - this指针
// 用来给【非静态成员函数】区分是【哪个成员实例】调用自己 （从函数指向调用的那个对象）

// *** this 指针是跟着成员函数走的，不同的成员函数的 this 指针不是同一个 *** //

// 两种用法：

// 1. 区分形参和成员变量同名的情况
void test_115_01 ()
{
    C1 c1(10); // 看上面类定义中，形参和成员函数重名的情况

    cout << "具有一个整形属性的对象占用的内存空间是： " << sizeof(c1) << endl;  // 4个字节，因为只有一个int属性
}

// 2. 返回对象自身 return *this
void test_115_02 ()
{
    C1 c1(10); 
    C1 c2(10); 

    // 链式编程思想：每一次调用这个函数，返回的值都是c1本身，这样才能继续调用下一个
    c1.PersonAddAge(c2).PersonAddAge(c2).PersonAddAge(c2).PersonAddAge(c2);

    cout << "c1.a = " << c1.a << endl;
    cout << "c2.a = " << c2.a << endl;
}


// P116 - 空指针调用成员函数
class Person_116
{
public:
    int m_age;
public:
    void showClassName()
    {
        cout << "This is Person_116 Class." << endl;
    }
    void showPersonAge()
    {
        // 先增加this的地址检查
        if (this == NULL) 
        {
            cout << "This Ptr is NULL!" << endl;
            return;
        }
        
        cout << "Person Age is " << m_age << endl;
        // 等效于：
        cout << "Person Age is " << this->m_age << endl;
    }
};

void test_116_00 ()
{
    Person_116 *p1 = NULL;  // 空指针 nullptr; 这一行并不会创建一个新成员，除非这个地址上本身就有已经定义好的成员

    p1->showClassName();    // 这个可以在空指针下运行，下一个不可以(如果没有空指针的if检查)
    p1->showPersonAge();   // 因为这个函数会使用到一个非静态成员变量，它必须在一个确切的类成员上

}

// P117 - const 修饰成员函数
// 常函数：this指向的值不可以修改（【此函数内部】使用的成员变量都是常量）
class Person_117
{
public:
    int m_age;
    mutable int m_age2; // 加上mutable的成员变量，可以在常函数中被修改

    // 需要有一个构造函数给成员变量赋初值，防止后面新建常对象报错（没有初始化）
    Person_117 ()
    {
        m_age = 0;
        m_age2 = 1;
    }

public:
    // this 指针本质是个指针常量【指向的地址不能改】
    // 相当于 Person_117 * const this;

    // 在通常情况下，this指向的值可以修改，如果希望【值也不可以改】，就写成下面函数的样子（结尾加const)
    // 相当于 const Person_117 * const this;
    void showPerson() const
    {
        // this->m_age = 100; // 这样会报错，因为函数定义结尾的const
        this->m_age2 = 100; // 这样不会报错，因为m_age2 带有 mutable 定义
    }

    void func_117 (){}  // 随意写一个“不是常函数”
};

// 常对象
// 只能调用其中的常函数
// 内部【所有成员变量】都不可以改（mutable除外）
void test_117_00 ()
{
    const Person_117 p;
    
    // p.m_age = 100;   // 这个不可以，因为常对象不能修改其中任何成员变量的值
    p.m_age2 = 200;  // 这个可以，因为 m_age2 有 mutable

    // p.func_117 ();     // 这个不可以，这个函数不是常函数

    cout << "m_age2 = " << p.m_age2 << endl;
}

/*********************************************************************************************************/



int main_114 () {
    // 是否需要显示中文？
    bool ChineseDisplay = true;
    // bool ChineseDisplay = false;

    if (ChineseDisplay) system("chcp 936");  // to set CMD active code page for Chinese display (the default code page is "chcp 437")
    system("cls");

    test_117_00 ();
    
    system("pause");  // System: send a DOS command, which requires including stdlib.h
    return 0;
}


