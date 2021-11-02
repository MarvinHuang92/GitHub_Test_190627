// p121_operator_overloading.cpp

#include <iostream>
#include <stdlib.h>
#include <ctime>  // 用于time函数
#include <cmath>  // 用于数学计算
#include <string>

using namespace std;


// P121 运算符重载 (加号 减号)

// 主要是为了适用于不同的数据类型
// 可以利用【成员函数】重载（提供一个参数，和成员自身相加）
// 也可以利用【全局函数】重载（提供两个参数）

// 加号的重载 (例如两个自定义的数据类型 class / struct)
class Person_121
{
public:
    int m_A;
    int m_B;
public:
    // 无参构造函数，用默认值初始化
    Person_121()
    {
        m_A = 0;
        m_B = 0;
    }
    // 有参构造函数，根据输入来初始化
    Person_121(int a, int b)
    {
        m_A = a;
        m_B = b;
    }
    
    // 创造一个【成员函数】，将m_A m_B两个值分别相加，作为 Person_121 这个类的“加法”定义
    // operator+ 这是编译器预留的关键字，可以直接当作 + 使用
    Person_121 operator+(Person_121 &p1)
    {
        Person_121 temp;
        temp.m_A = this->m_A + p1.m_A;
        temp.m_B = this->m_B + p1.m_B;
        return temp;
    }

    // for P125: 重载相等判断的运算符
    bool operator==(Person_121 &p2)
    {
        if ((m_A == p2.m_A) && (m_B == p2.m_B))
        {
            return true;
        }
        return false;
    }
    // 重载不等判断的运算符
    bool operator!=(Person_121 &p2)
    {
        if ((m_A = p2.m_A) && (m_B == p2.m_B))
        {
            return false;
        }
        return true;
    }

};

// 利用【全局函数】重载减号运算符（不用加号作为例子，防止加号重载出现歧义性）
Person_121 operator-(Person_121 &p1, Person_121 &p2)
{
    Person_121 temp;
    temp.m_A = p1.m_A - p2.m_A;
    temp.m_B = p1.m_B - p2.m_B;
    return temp;
}

// 另一种重载：一个 Person类 和一个 int 相加
Person_121 operator+(Person_121 &p1, int num)
{
    Person_121 temp;
    temp.m_A = p1.m_A + num;
    temp.m_B = p1.m_B + num;
    return temp;
}

void test_121_00 ()
{
    Person_121 p1(10, 20);
    Person_121 p2(30, 40);

    cout << p1.m_A << " " << p1.m_B << endl;
    cout << p2.m_A << " " << p2.m_B << endl;

    // 完整的写法【成员函数重载】
    // Person_121 p3 = p1.operator+ (p2);
    // 完整的写法【全局函数重载】
    // Person_121 p4 = operator-(p1, p2);
    // 两种都可以简化为：
    Person_121 p3 = p1 + p2;
    Person_121 p4 = p1 - p2;

    cout << p3.m_A << " " << p3.m_B << endl;
    cout << p4.m_A << " " << p4.m_B << endl;

    Person_121 p5 = p1 + 1000;  // Person类 和 int 的加法

    cout << p5.m_A << " " << p5.m_B << endl;

}


// P122 - 左移的重载 << 
// 可以用 cout 输出自定义的数据类型（例如 打印类的所有属性）

// 这个无法使用【成员函数】来完美实现，因为 “cout << p” 中 cout 在左边，而p类下的成员变量要求 p 在左边
// 所以直接直接用【全局函数】来实现重载
ostream& operator<< (ostream &cout, Person_121 &p)  // ostream是“标准输出流”数据类型，而且cout全局只有一个，只能&引用，而不能创建新的
{
    cout << "m_A = " << p.m_A << "\tm_B = " << p.m_B;
    return cout;  // 确保返回值的类型不变，支持链式表达式
}

void test_122_00 ()
{
    Person_121 p1(10, 20);

    // 简化写法
    cout << p1 << endl;
    // 完整写法
    operator<<(cout, p1) << endl;  // 注意只有第一个运算符是重载的，后一个还是默认的用法

}


// P123 - 递增的重载 ++
// 注意区分 左加 和 右加
// ++a 先自加后参与运算，a++ 先参与运算后自加

// 首先自定义一个新的整形
class MyInteger
{
    // 声明友元，为了让重载左移可以访问私有的 m_Num
    friend ostream& operator<< (ostream &cout, const MyInteger &i);
private:
    int m_Num;
public:
    // 构造函数初始化
    MyInteger(): m_Num(0) {}

    // 利用【成员函数】重载“前置++” 左加
    MyInteger& operator++()  // 返回引用&是为了不创建新的类成员，而是返回调用此函数的成员自身
    {
        m_Num++;
        return *this;
    }

    // 利用【成员函数】重载“后置++” 右加
    MyInteger operator++(int)  // 注意这个形参 int 只有类型没有名字，是“占位参数”，可以用于区分后置运算，只要用int就行，别的不用（char, float这种）
                               // 后置递增不能返回引用& ！！！因为它的返回值是临时变量temp，函数结束后地址会被释放
                               // 另外，【*** 后置++因为返回值是 值传递 而不是 地址传递，所以比前置++更耗时。当两者都可用的时候建议用前置++ ***】
    {
        // 先记录“当前值”，然后再递增
        MyInteger temp = *this;
        m_Num++;
        return temp;  // 返回递增前的值
    }

};
// 重载左移运算，为了输出“自定义整形”
ostream& operator<< (ostream &cout, const MyInteger &i)  // 注意第二个参数前面的const: 如果没有它，前置++可以使用，但后置++会报错
                                                         // 因为后置++返回值是值传递，而不是引用（aka地址传递），因此无法被 Myinteger& 类型接受
                                                         // 【但为什么 const MyInteger & 就可以？】
{
    cout << i.m_Num;
    return cout;
}

void test_123_00 ()
{
    MyInteger int_1;  // 初值为0

    // 利用重载的左移来打印“自定义整形”
    cout << ++(++int_1) << endl;  // 自加两次，应当返回2
    cout << int_1 << endl;

    // 后置递增不能用链式操作（原生的后置++也是个非法操作）
    cout << int_1++ << endl;    // 先返回2再自加
    cout << int_1 << endl;      // 应当返回3

}

// 原生的后置++也是个非法操作 - 验证
void test_123_01 ()
{
    int a = 0;
    // cout << (a++)++ << endl;  // 会报错“第二个++缺少左值” lvalue required as increment operand

}

// P124 - 赋值运算符重载 = 
/*
对于类，除了三个默认函数之外（构造，拷贝构造，析构），还有第四个函数，即赋值运算符本身 "="
如果有属性在 堆区，都会出现深浅拷贝的问题， 参考 P106
*/

class Person_124
{
public:
    int * m_age;  // 这是个指针
    
    // 有参构造
    Person_124(int age)
    {
        m_age = new int(age);  // 注意 new 返回地址，用指针去接受它
    }

    // 析构函数，释放堆区数据
    ~ Person_124()
    {
        if (m_age != NULL)
        {
            delete m_age;
            m_age = NULL;
        }
    }

    // 解决方法：同样是【深拷贝】，由于赋值运算符和【拷贝构造】是一样的，所以对赋值运算符 = 也要进行重载
    // 这个函数写成全局的（两个参数 p1 p2）就会报错，不知道为啥，说“它必须是个非静态成员变量”
    Person_124& operator= (Person_124 &p2)
    {
        // 编译器的行为：浅拷贝
        // m_age = p2.m_age;

        // 深拷贝：
        // 首先判断左值自身是否有属性在堆上，如果有，先释放它
        if (m_age != NULL)
        {
            delete m_age;
            m_age = NULL;
        }

        m_age = new int(*p2.m_age);  // 重新在堆区开辟一个新的内存，其值 等于 p2的m_age地址解引用

        return *this;  // 允许链式反应，连等式
    }
};

void test_124_00 ()
{
    Person_124 p1(18);
    Person_124 p2(20);
    Person_124 p3(30);

    p3 = p2 = p1;  // 赋值操作，此时p2年龄也变成了18，注意这里是【浅拷贝】，所以会指向同一个堆区内存
                   // 连等式是从右往左运行的，最后三个值都是18

    cout << "p1的年龄为： "<< *p1.m_age << endl;
    cout << "p2的年龄为： "<< *p2.m_age << endl;
    cout << "p3的年龄为： "<< *p3.m_age << endl;

    /* 如果没有重载 = 运算符，在这里会崩溃，（析构顺序：先创建的成员后析构）因为p2析构的时候释放了堆区的内存，等到p1析构时就找不到这个地址了 */

}

// P125 - 关系运算符重载 == != <= >=之类，主要是 == 和 !=
// 这里借用已经存在的类 Person_121，它有两个成员变量 int m_A; int m_B;

void test_125_00 ()
{
    Person_121 p1(18, 19);
    Person_121 p2(18, 19);
    Person_121 p3(30, 31);

    cout << "p1："<< p1.m_A << " " << p1.m_B << endl;
    cout << "p2："<< p2.m_A << " " << p2.m_B << endl;
    cout << "p3: "<< p3.m_A << " " << p3.m_B << endl;

    if (p1 == p2)  // ==不能链式使用 （p1==p2 结果是bool，不能和后面的类型做比较）
    {
        cout << "p1 等于 p2" << endl;
    }
    else
    {
        cout << "p1 不等于 p2" << endl;
    }

}


// P126 - 函数调用运算符()重载 - 又叫做“仿函数”

// 先定义一个自己的 打印 【类】
class MyPrint
{
public:
    // 重载函数调用运算符
    void operator() (string test)
    {
        cout << test << endl;
    }
};

// 再定义一个 【全局函数】 作为对比
void myprint2 (string test)
{
    cout << test << endl;
}

void test_126_00 ()
{
    MyPrint myprint; // 创建一个类下面的实例，然后这个 实例 可以直接当作函数使用！
    myprint("Hello World!");   // 这是类里面的【仿函数】
    myprint2("Hello World!");  // 这是真正的【全局函数】
    // 两者的效果是一样的

    // 更进一步的，可以不创建类下面的实例，直接使用【类名称()】本身来实现【仿函数】 - 即【匿名对象】
    // 原因：类下面的成员函数 （无论是否静态函数） 都是随着类本身走的（还有静态成员变量），不依赖于具体的类成员
    MyPrint() ("Hello World!");            // 第一个()是创建了【匿名对象】(只在当前行使用，然后立即释放)，第二个()是【重载的函数调用运算符】
    MyPrint().operator()("Hello World!");  // 完整写法
}



/*********************************************************************************************************/



int main () {
    // 是否需要显示中文？
    bool ChineseDisplay = true;
    // bool ChineseDisplay = false;

    if (ChineseDisplay) system("chcp 936");  // to set CMD active code page for Chinese display (the default code page is "chcp 437")
    system("cls");

    test_126_00 ();
    
    system("pause");  // System: send a DOS command, which requires including stdlib.h
    return 0;
}


