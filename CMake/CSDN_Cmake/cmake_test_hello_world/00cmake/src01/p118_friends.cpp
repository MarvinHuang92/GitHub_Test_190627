// p118_friends.cpp

#include <iostream>
#include <stdlib.h>
#include <ctime>  // 用于time函数
#include <cmath>  // 用于数学计算
#include <string>

using namespace std;


/*
这一章涉及到很多类的 声明和实现 拆分写
因为当一个类中声明另一个类的 成员函数 作为友元，可能会经常报错找不到类成员
因此事先声明很重要
*/

class Building; // 类声明，防止后面找不到（简单的声明，只有一行）
class GoodBoy   // 类声明，防止后面找不到（复杂的声明，需要具体到成员变量和成员函数，后面 P120 单独写“类外实现”）
{
    public:
    Building *b;
    // 成员函数
    void visit();   // 普通的
    void visit_2(); // 被声明成 Building 类的友元的，只有这个可以访问 private 内容
    // 构造函数
    GoodBoy();
};

// P118 友元 Friend
/* 允许一些特殊的函数或者类访问私有变量 */

// 全局函数做友元
class Building 
{
    // 友元声明，允许下面的函数访问私有内容
    friend void goodGay(Building &b);  // 形参列表不可以省略，为了区分函数重载的情况
    friend class GoodGirl;
    friend void GoodBoy::visit_2();

public:
    // 构造函数给属性赋初值
    Building()
    {
        m_sittingRoom = "客厅";
        m_bedRoom = "卧室";
    }

public:
    string m_sittingRoom;  // 客厅：公共
private:
    string m_bedRoom;      // 卧室：私有
};

// 写一个全局函数
void goodGay(Building &b)
{
    cout << "好基友全局函数 正在访问Building类的 " << b.m_sittingRoom << endl;
    cout << "好基友全局函数 正在访问Building类的 " << b.m_bedRoom << endl;  // 这个会报错，因为bedRoom是私有的 【但在类中加上友元声明就好了】
}

void test_118_00()
{
    Building b;
    goodGay(b);
}

// P119 - 类做友元
class GoodGirl
{
public:
    Building *b;
    void visit()
    {
        cout << "好基友类 正在访问Building类的 " << b->m_sittingRoom << endl;
        cout << "好基友类 正在访问Building类的 " << b->m_bedRoom << endl;  // 这个会报错，因为bedRoom是私有的 【但在类中加上友元声明就好了】
    }
    
    // 构造函数
    GoodGirl()
    {
        // Building building;
        // b = &building;
        b = new Building;  // 注意 new 返回的是地址！
        cout << "address of new Building Class: " << b << endl;  // 为了验证上面那句话，new 的地址每次运行都不一样
    }
};

void test_119_00()
{
    GoodGirl mm;
    mm.visit();
}


// P120 - 成员函数做友元
// class GoodBoy 的“类外实现” // 这个类和上面的 GoodGirl 类基本一样，但多了一个成员函数

void GoodBoy::visit()
{
    cout << "好基友类-visit函数 正在访问Building类的 " << b->m_sittingRoom << endl;
    // cout << "好基友类-visit函数 正在访问Building类的 " << b->m_bedRoom << endl;  // 这个会报错，因为bedRoom是私有的 【但在类中加上友元声明就好了】
}

void GoodBoy::visit_2()
{
    cout << "好基友类-visit_2函数 正在访问Building类的 " << b->m_sittingRoom << endl;
    cout << "好基友类-visit_2函数 正在访问Building类的 " << b->m_bedRoom << endl;  // 这个会报错，因为bedRoom是私有的 【但在类中加上友元声明就好了】
}

// 构造函数
GoodBoy::GoodBoy()
{
    // Building building;
    // b = &building;
    b = new Building;  // 注意 new 返回的是地址！
    cout << "address of new Building Class: " << b << endl;  // 为了验证上面那句话，new 的地址每次运行都不一样
}

void test_120_00()
{
    GoodBoy gg;
    gg.visit();
    gg.visit_2();
}

/*********************************************************************************************************/



int main_118 () {
    // 是否需要显示中文？
    bool ChineseDisplay = true;
    // bool ChineseDisplay = false;

    if (ChineseDisplay) system("chcp 936");  // to set CMD active code page for Chinese display (the default code page is "chcp 437")
    system("cls");

    test_120_00 ();
    
    system("pause");  // System: send a DOS command, which requires including stdlib.h
    return 0;
}


