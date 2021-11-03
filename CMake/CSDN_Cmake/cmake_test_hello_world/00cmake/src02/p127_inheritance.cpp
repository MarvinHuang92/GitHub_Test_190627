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
继承方式         父类的内容       子类的内容        父类权限的前两项在子类中不变，父类的private在子类中不可访问
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
};

// 子类/派生类
class SubClass : public BaseClass // 用：表示继承即可，后面的 public 称为【继承方式】
{
public:
    int m_sub_num;
};

void test_127_00()
{
    SubClass sc;
    sc.m_base_num = 0;
    sc.m_sub_num = 1;

    cout << sc.m_base_num << endl;
    cout << sc.m_sub_num << endl;
}



/*********************************************************************************************************/



int main () {
    // 是否需要显示中文？
    bool ChineseDisplay = true;
    // bool ChineseDisplay = false;

    if (ChineseDisplay) system("chcp 936");  // to set CMD active code page for Chinese display (the default code page is "chcp 437")
    system("cls");

    test_127_00 ();
    
    system("pause");  // System: send a DOS command, which requires including stdlib.h
    return 0;
}


