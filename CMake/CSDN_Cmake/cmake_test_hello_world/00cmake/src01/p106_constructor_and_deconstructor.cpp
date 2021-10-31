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


