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

    // 构造函数，仅用于展示对象的创建时机，无实际作用
    Animal()
    {
        cout << "Animal类的构造函数调用" << endl;
    }
    // 析构函数，【虚析构，可以令父类析构之前，调用子类的析构函数】
    virtual ~Animal()
    {
        cout << "Animal类的析构函数调用" << endl;
    }
};

class Cat: public Animal  // 子类，小猫
{
public:
    void speak()
    {
        cout << *m_name << "小猫在说话。" << endl;
    }
    
    // 这部分仅用于P140
    string * m_name;
    // 构造函数
    Cat(string name)
    {
        cout << "Cat类的构造函数调用" << endl;
        m_name = new string(name);  // 在构造时，创建一个堆区数据
    }
    // 析构函数
    ~Cat()
    {
        cout << "Cat类的析构函数调用" << endl;
        delete m_name;
        m_name = NULL;
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
    Cat cat("Tom");
    doSpeak(cat);  // 注意这里给函数传递的是“小猫类” （子类）

    Dog dog;
    doSpeak(dog);
}

/* 
如果想实现上述函数结果是“小猫/小狗在说话”：
1. 在父类的speak函数前面加上virtual 然后：
2. 在子类的speak函数后面加上override，表示它可以重写父类同名函数（第二步做不做似乎没有区别？）
*/


// P137 - 多态实现计算器
class Calculator  // 使用传统方法写一个例子先
{
public:
    int m_num1;
    int m_num2;

    int getResult(string oper)
    {
        if(oper == "+")
        {
            return m_num1 + m_num2;
        }
        else if(oper == "-")
        {
            return m_num1 - m_num2;
        }
        else if(oper == "*")
        {
            return m_num1 * m_num2;
        }
        // 暂时不支持除法，因为返回值是int
    }
};
void test_137_00()
{
    Calculator cl;
    string oper;
    cout << "请输入数字1： " << endl;
    cin >> cl.m_num1;
    cout << "请输入操作符：" << endl;
    cin >> oper;
    cout << "请输入数字2： " << endl;
    cin >> cl.m_num2;

    cout << "运算结果： "<< cl.getResult(oper) << endl;

}

// 开闭原则：开放扩展，关闭修改（禁止修改已经写好的源码）
// 使用多态方法实现计算器的方法：

// 抽象的计算器类，虚函数没有功能，只有成员变量
class AbstractCalculator
{
public:
    int m_num1;
    int m_num2;
    // 先提供一个虚函数，本身没有任何功能，只是留给子类去继承它
    virtual int getResult()
    {
        return 0;
    }
};

// 加法计算器类，重写了父类中的getResult函数
class AddCalculator: public AbstractCalculator
{
public:
    int getResult()
    {
        return m_num1 + m_num2;
    }

};

// 减法计算器类
class SubtractCalculator: public AbstractCalculator
{
public:
    int getResult()
    {
        return m_num1 - m_num2;
    }

};

// 乘法计算器类
class MultipleCalculator: public AbstractCalculator
{
public:
    int getResult()
    {
        return m_num1 * m_num2;
    }

};

// 多态：父类的指针指向子类的对象
void test_137_01()
{
    // 加法示例：
    AbstractCalculator * cl_add = new AddCalculator;  // 父类的指针指向子类的对象
    cout << "请输入数字1： " << endl;
    cin >> cl_add->m_num1;
    cout << "请输入数字2： " << endl;
    cin >> cl_add->m_num2;

    cout << "加法运算结果： "<< cl_add->getResult() << endl;

    // 减法
    AbstractCalculator * cl_sub = new SubtractCalculator;  // 父类的指针指向子类的对象
    cout << "请输入数字1： " << endl;
    cin >> cl_sub->m_num1;
    cout << "请输入数字2： " << endl;
    cin >> cl_sub->m_num2;

    cout << "减法运算结果： "<< cl_sub->getResult() << endl;

    // 乘法
    AbstractCalculator * cl_mul = new MultipleCalculator;  // 父类的指针指向子类的对象
    cout << "请输入数字1： " << endl;
    cin >> cl_mul->m_num1;
    cout << "请输入数字2： " << endl;
    cin >> cl_mul->m_num2;

    cout << "乘法运算结果： "<< cl_mul->getResult() << endl;

    // 销毁new出来的对象
    delete cl_add, cl_sub, cl_mul;
    cl_add = NULL;
    cl_sub = NULL;
    cl_mul = NULL;
}

// P138 - 【纯虚函数】和【抽象类】
// 结尾有 = 0 的虚函数，称为【纯虚函数】
// 内部有至少一个纯虚函数的类，称为【抽象类】，它【无法实例化对象】
// 子类必须重写抽象类中的纯虚函数，否则子类依然是抽象类，也无法实例化对象
class AbstractCalculator_Pure
{
public:
    // 【纯虚函数】最后的 = 0 可以代替下面的大括号和return 0
    virtual int getResult() = 0;
    // {
    //     return 0;
    // }
};

// P139 - 纯虚函数实例：制作饮品
class AbstractDrinking
{
public:
    //煮水（纯虚函数）
    virtual void Boil() = 0;
    //冲泡（纯虚函数）
    virtual void Brew() = 0;
    //倒入杯中（纯虚函数）
    virtual void Pour() = 0;
    //加入辅料（纯虚函数）
    virtual void PutSomething() = 0;
    //整合函数：制作饮品
    virtual void makeDrink()
    {
        Boil();
        Brew();
        Pour();
        PutSomething();
    }
};

// 子类：制作咖啡
class MakeCoffee: public AbstractDrinking
{
public:
    //煮水（重写函数）
    virtual void Boil()
    {
        cout << "煮纯净水" << endl;
    }
    //冲泡（重写函数）
    virtual void Brew()
    {
        cout << "冲咖啡" << endl;
    }
    //倒入杯中（重写函数）
    virtual void Pour()
    {
        cout << "倒入杯中" << endl;
    }
    //加入辅料（重写函数）
    virtual void PutSomething()
    {
        cout << "加入糖和牛奶" << endl;
    }
    //整合函数：制作饮品
    virtual void makeDrink()
    {
        Boil();
        Brew();
        Pour();
        PutSomething();
    }
};

// 子类：制作茶
class MakeTea: public AbstractDrinking
{
public:
    //煮水（重写函数）
    virtual void Boil()
    {
        cout << "煮矿泉水" << endl;
    }
    //冲泡（重写函数）
    virtual void Brew()
    {
        cout << "冲茶叶" << endl;
    }
    //倒入杯中（重写函数）
    virtual void Pour()
    {
        cout << "倒入杯中" << endl;
    }
    //加入辅料（重写函数）
    virtual void PutSomething()
    {
        cout << "加入桂花和柠檬" << endl;
    }
    //整合函数：制作饮品
    virtual void makeDrink()
    {
        Boil();
        Brew();
        Pour();
        PutSomething();
    }
};

// 全局函数，形参可以用【抽象类】，但调用时传入的实参必须是【子类】
// 注意【抽象类】只能作为形参使用，在函数内部 new 一个对象是不行的
void doWork(AbstractDrinking * abd)
{
    abd->makeDrink();

    // 销毁new出来的对象
    delete abd;
    abd = NULL;
}

void test_139_00()
{
    // MakeCoffee coffee;
    // MakeTea tea;
    // doWork(&coffee);
    // doWork(&tea);

    // 直接new就可以返回对象的地址，不用单独实例化对象，且不用给对象起名字
    doWork(new MakeCoffee);
    doWork(new MakeTea);
}

// P140 - 虚析构、纯虚析构
// 解决问题：父类指针无法释放子类对象，导致内存泄漏
// 带有【纯虚析构】的类也是【抽象类】，无法实例化对象，只能用在函数的形参中
void test_140_00()
{
    Animal * animal = new Cat("Tom");  // 父类指针指向子类对象，构成多态
    animal->speak();
    // 可以看到，父类的析构函数会被调用，但子类的析构函数没有被调用，这时如果在子类中有堆区数据（本例中的m_name）会无法释放导致内存泄漏
    delete animal;

    // 解决方法：将【父类】的析构换成【虚析构】前面加 virtual 即可
    // 如果结尾再加上 = 0，称为【纯虚析构】必须在【类外】被重写（实现）而【不是在子类中重写】
    /*
    Animal::~Animal()
    {
        // Do something
    }
    */

    // 所以这个很鸡肋，【直接用普通的虚析构就行】
}


/*********************************************************************************************************/



int main_135 () {
    // 是否需要显示中文？
    bool ChineseDisplay = true;
    // bool ChineseDisplay = false;

    if (ChineseDisplay) system("chcp 936");  // to set CMD active code page for Chinese display (the default code page is "chcp 437")
    system("cls");

    test_140_00 ();
    
    system("pause");  // System: send a DOS command, which requires including stdlib.h
    return 0;
}


