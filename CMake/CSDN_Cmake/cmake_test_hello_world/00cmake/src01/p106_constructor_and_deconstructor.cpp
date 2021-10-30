// p106_constructor_and_deconstructor

#include <iostream>
#include <stdlib.h>
#include <ctime>  // 用于time函数
#include <cmath>  // 用于数学计算
#include <string>

using namespace std;

// P106 构造函数和析构函数
// 用于初始化和销毁类中的对象
class Person 
{
    public:
    int age;

    public:
    // 有参构造函数
    Person(string s)    // 构造函数，类的实例创建时自动运行 （类似于 __init__ ）
                        // 构造函数可以重载，可以有参数
    {
        cout << "这是Person类的构造函数 有参构造：" << s << endl;
    }
    // 一种重载：更改参数类型
    Person(int a)
    {
        cout << "这是Person类的构造函数 有参构造：" << a << endl;
    }
    // 一种重载：无参构造函数
    Person() 
    {
        cout << "这是Person类的构造函数 无参构造：" << endl;
    }
    // 另一种重载：拷贝构造函数(将另一个类成员的所有属性都拷贝过来)，注意属性是以【值传递】的方式拷贝的。
    Person(const Person &p)  // 用const防止拷贝之后在该函数中改变了原始对象
    {
        cout << "拷贝构造函数：p.age = " << p.age << endl;
    }

    ~Person()  // 析构函数，类的实例被销毁时运行
               // 析构函数不可以重载，没有参数
    {
        cout << "这是Person类的析构函数" << endl;
    }
};

void test01 ()
{
    // 重要：如果是普通的无参调用，不要写()，不然编译器会和“函数声明”混淆！！！
    // Person p0(); // 这样写错误：不会创建实例
    Person p0;

    // 有参调用
    Person p1("A String.");  // 如果放在main函数中，析构函数不会被执行，因为main程序还没有结束
                            // 放在test01()中，会在该函数结束时候执行析构函数
    
    Person p1a = Person("Another String.");  // 显式的调用。将一个匿名对象赋值给p1a
    // Person p1b = "Another String.";      // 隐式的调用，直接写准备传入的参数即可，但string不支持（这是一个常量），int支持（临时变量）
    string s0 = "Another String 2.";
    Person p1b = s0;                        // 隐式的调用
    Person p1c = 10;                        // 隐式的调用
    
    p1.age = 18;

    // 拷贝调用，注意属性是以【值传递】的方式拷贝的。
    Person p2(p1); // 将p1的属性拷贝给p2，在p2的构造函数中可以打印age

    Person p2a = Person(p1);    // 显式的调用。
    Person p2b = p1;            // 隐式的调用。

    system("pause");
}

/*********************************************************************************************************/



int main () {
    // 是否需要显示中文？
    bool ChineseDisplay = true;
    // bool ChineseDisplay = false;

    if (ChineseDisplay) system("chcp 936");  // to set CMD active code page for Chinese display (the default code page is "chcp 437")
    system("cls");

    test01 ();
    
    system("pause");  // System: send a DOS command, which requires including stdlib.h
    return 0;
}


