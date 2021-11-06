// p135_polymorphic.cpp

#include <iostream>
#include <stdlib.h>
#include <ctime>  // 用于time函数
#include <cmath>  // 用于数学计算
#include <string>

using namespace std;


// P135 多态 - 父类指针接受子类对象

// 【虚函数表】底层原理P136视频： https://www.bilibili.com/video/BV1et411b73Z?p=136&spm_id_from=pageDriver

/*
动态多态 - 满足条件：
1. 有继承关系
2. 子类重写了父类的虚函数（注意重写不是重载，它的函数名和参数都必须完全一致）

另外，如果父类是虚函数，则子类中的同名函数自动会变成虚函数，不需要再次写 virtual 关键字，但写了也没错

动态多态如何实现：
父类指针或者引用，指向子类的对象
*/

class Animal  // 父类，动物
{
public:
    virtual void speak()    // 如果在父类没有加 virtual，执行的结果是"动物在说话"，相当于子类被强制转化成了父类
                            // 因为父类的函数地址“早绑定”，在编译阶段就确定了
                            // 加上virtual以后，就变成了虚函数，其地址会在运行阶段再绑定，可以被子类的同名函数重写
    {
        cout << "动物在说话。" << endl;
    }
};

class Cat: public Animal  // 子类，小猫
{
public:
    void speak()
    {
        cout << "小猫在说话。" << endl;
    }
};

class Dog: public Animal  // 子类，小狗
{
public:
    void speak()
    {
        cout << "小狗在说话。" << endl;
    }
};

// 注意这个全局函数的形参是“动物类” (父类)
void doSpeak (Animal &animal)
{
    animal.speak();
}

void test_135_00()
{
    Cat cat;
    doSpeak(cat);  // 注意这里给函数传递的是“小猫类” （子类）

    Dog dog;
    doSpeak(dog);
}

/* 
如果想实现上述函数结果是“小猫/小狗在说话”：
1. 在父类的speak函数前面加上virtual 然后：
2. 在子类的speak函数后面加上override，表示它可以重写父类同名函数（第二步做不做似乎没有区别？）
*/


/*********************************************************************************************************/



int main () {
    // 是否需要显示中文？
    bool ChineseDisplay = true;
    // bool ChineseDisplay = false;

    if (ChineseDisplay) system("chcp 936");  // to set CMD active code page for Chinese display (the default code page is "chcp 437")
    system("cls");

    test_135_00 ();
    
    system("pause");  // System: send a DOS command, which requires including stdlib.h
    return 0;
}


