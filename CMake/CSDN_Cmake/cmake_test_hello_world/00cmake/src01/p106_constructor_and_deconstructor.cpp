// p106_constructor_and_deconstructor.cpp

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
    int * m_height;

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

        // m_height = p.m_height; // 编译器自己的实现方式【浅拷贝】，如果 m_height 本身是一个地址值，就不要用这种，不然两个p实例会指向同一块地址
        m_height = new int (*p.m_height);  // 手写的【深拷贝】，先将目标地址解引用成为数值，然后将它 new 到堆区，这样会自动产生一个新的内存地址
        cout << "拷贝构造函数：*p.m_height = " << *p.m_height << endl;
    }

    ~Person()  // 析构函数，类的实例被销毁时运行
               // 析构函数不可以重载，没有参数
    {
        cout << "这是Person类的析构函数" << endl;

        // 将堆区的内存释放
        if (m_height != NULL)
        {
            delete m_height;
            m_height = NULL;  // 注意这里m_height是地址值，*m_height才是实际值，这一行是为了防止留下野指针
        }
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
    p1.m_height = new int(180);

    // 拷贝调用，注意属性是以【值传递】的方式拷贝的。
    Person p2(p1); // 将p1的属性拷贝给p2，在p2的构造函数中可以打印age

    Person p2a = Person(p1);    // 显式的调用。
    Person p2b = p1;            // 隐式的调用。

    system("pause");
}

// P108
/* 如果有一个函数的【参数】是类，当使用【值传递】调用此函数时，这个类的【拷贝构造】函数会被调用 */
/* 如果有一个函数的【返回值】是类，此函数返回值时，这个类的【拷贝构造】函数会被调用 */
/* 因为值传递的本质是复制一个临时变量，所以会发生【拷贝】动作 */

// P109 - 编译器默认提供空实现的构造函数和析构函数
/*  
构造函数有三个层级：
1. 默认无参 Person p;
2. 默认有参 Person p(int a);
3. 拷贝构造 Person p1(Person p0);

如果用户都没有提供，编译器会提供一个空实现的1 和 3
如果用户提供了2，编译器不会提供1，但是会提供3； - 这时候要注意如果无意间创建了无参的新对象 Person p;，会报错。必须给一个参数
如果用户提供了3，编译器不再提供1 和 2 - 注意事项同上一条

析构函数同理，编译器会自动创建一个空实现。
*/

// P110 - 深拷贝和浅拷贝
/* 
如果是编译器自创的【拷贝构造】，使用的就是【浅拷贝】，将所有的值都字面意义的复制，如果属性值是一个指针，这个【地址】也会被简单地复制
可能的问题：【堆区内存在析构时重复释放】
如果两个类实例中的指针指向同一个堆区数据，而且在析构函数中包含“释放堆区”的操作
则【第二个被析构的类实例】会报错，找不到堆区地址——因为已经被第一个析构函数释放过一次了
* 根据类实例在栈区先进后出的规则，第二个被析构的类实例，是第一个定义的实例，通常依次定义了 Person p1; Person p2; 则 p1 比 p2 更晚被析构
具体的解释见插图

解决方法：【深拷贝】
方法：不要让编译器自己创建【拷贝构造函数】，而是自己写一个 

具体看上面代码中的 重载-拷贝构造函数
*/

// P111 - 初始化列表
// 传统方式的初始化：在构造函数中进行 (有参的构造函数)
class Person_2 {
    public:
    int m_a;
    int m_b;
    int m_c;

    public:
    // 利用有参构造函数初始化【传统方法】
    // Person_2 (int a, int b, int c)
    // {
    //     m_a = a;
    //     m_b = b;
    //     m_c = c;
    // }

    // 利用参数列表初始化【新方法】
    // 但有个局限：如果下面三个参数是private会无法初始化
    Person_2(int a, int b, int c): m_a(a), m_b(b), m_c(c)
    {
        // Do nothing here
    }
};

void test02 ()
{
    Person_2 p20(10, 20, 30);

    cout << p20.m_a << p20.m_b << p20.m_c << endl;

    system("pause");
}

// P112 - 对象成员（一个类成员是另一个类的对象）
class Phone
{
public:
    string ph_name;
    float ph_size;
    
    // 构造函数
    Phone(string name, float size): ph_name(name), ph_size(size) 
    {
        cout << "Phone 构造函数被调用" << endl;
    }
};

class Person_3
{
public:
    /* data */
    string m_name;
    Phone m_phone;
public:
    // 构造函数，其中的两个参数和Phone类构造函数中的两个参数相对应
    // 这里省略了一次隐式转换： Phone m_phone = ph_name, ph_size； 创建了一个Phone实例，但它没有自己的名字
    Person_3(string person_name, string ph_name, float ph_size):m_name(person_name), m_phone(ph_name, ph_size) 
    {
        cout << "Person_3 构造函数被调用" << endl;
    }
};

// Phone类是Person_3的成员属性，因此先构建Phone（内部类），再构造Person（外部类）；析构的顺序反过来
void test03 ()
{
    Person_3 p30("Alice", "HUAWEI P30", 6.5);

    cout << p30.m_name << endl; 
    cout << p30.m_phone.ph_name << endl;
    cout << p30.m_phone.ph_size << endl;

    system("pause");
}

// P112.5 - 缺少的一集： https://www.bilibili.com/video/BV1h7411e7wk?from=search&seid=7200463635805732693&spm_id_from=333.788.b_636f6d6d656e74.30
// 静态成员变量
// P113 - 静态成员函数
/* 
所有的类实例都共享同一个数据
在编译阶段就分配了内存，在程序开始之前 
在类内声明，但在类外初始化，不然编译的时候它没有初始值
可以由类名直接访问
静态成员函数只能访问静态的成员变量
*/
class Person_4
{
public:
    static int s_number;  // 类内声明

    static void func()  // 静态成员函数只能访问静态的成员变量 （因为它可能被类名直接调用，如果有非静态变量参与，不知道该用那个类实例下面的变量）
    {
        cout << "静态成员函数 func() 被调用: s_number = " << s_number << endl;
    }
};

// 类外初始化，注意双冒号 ::
int Person_4::s_number = 100;

void test04 ()
{
    Person_4 p40;
    Person_4 p41;

    cout << p40.s_number << endl; 

    p41.s_number = 200;  // 由另一个类的实例修改静态变量

    cout << p41.s_number << endl;  // 可以看到静态变量值确实被改变了

    cout << Person_4::s_number << endl;  // * 特别的，静态变量可以直接由类的名字访问，而不必用具体的类实例（但类名用 :: 分割，而不是 .）

    Person_4::func();  // 通过类名直接调用静态成员函数

    system("pause");
}



/*********************************************************************************************************/



int main_106 () {
    // 是否需要显示中文？
    bool ChineseDisplay = true;
    // bool ChineseDisplay = false;

    if (ChineseDisplay) system("chcp 936");  // to set CMD active code page for Chinese display (the default code page is "chcp 437")
    system("cls");

    test04 ();
    
    system("pause");  // System: send a DOS command, which requires including stdlib.h
    return 0;
}


