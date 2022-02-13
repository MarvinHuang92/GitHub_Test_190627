// p173_func_template_for_class.cpp

#include <iostream>
#include <stdlib.h>
#include <ctime>  // 用于time函数
#include <cmath>  // 用于数学计算
#include <string>

using namespace std;

#include <fstream> // 用于文件操作

// P173 - 模板的局限性 - 对于特殊数据类型的处理（例如：比较两个自定义数据类型是否相等）

// 比较两个数据是否相等
template<class T>
bool MyCompare(T &a, T &b)
{
    if (a == b) return true;
    return false;
}

class Person
{
public:
    Person(string name, int age)
    {
        this->m_name = name;
        this->m_age = age;
    }

    string m_name;
    int m_age;

    /* 方法1：这里如果重载 == 符号，也可以解决问题 */
};

// 方法2：单独“具体化”一个适用于 Person 数据类型的重载函数
template<> bool MyCompare(Person &a, Person &b)
{
    if ((a.m_name == b.m_name) && (a.m_age == b.m_age)) return true;
    return false;
}

// 测试函数
void test_173()
{
    int a = 10;
    int b = 10;
    // int b = 20;
    cout << "a 和 b 相等吗？ " << MyCompare(a, b) << endl;

    Person p1("Tom", 10);
    Person p2("Tom", 10);
    // Person p2("John", 12);
    cout << "p1 和 p2 相等吗？ " << MyCompare(p1, p2) << endl;  // 当推导出来参数类型是 Person 时，会调用重载后的函数
}


/*********************************************************************************************************/



int main_173 () {
    // 是否需要显示中文？
    bool ChineseDisplay = true;
    // bool ChineseDisplay = false;

    if (ChineseDisplay) system("chcp 936");  // to set CMD active code page for Chinese display (the default code page is "chcp 437")
    system("cls");

    test_173 ();
    
    system("pause");  // System: send a DOS command, which requires including stdlib.h
    return 0;
}


