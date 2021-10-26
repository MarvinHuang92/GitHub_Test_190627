//s05_struct_P64.cpp

#include <iostream>
#include <stdlib.h>
#include <ctime>  // 用于time函数
#include <cmath>  // 用于数学计算
#include <string>

using namespace std;

/* P55 也可以再看一下，头文件和源文件的格式范例，当然以后想起来再看亦可以 */

// P64 - 定义结构体，本质是一个自定义的数据类型
// 自定义数据类型，这里的struct可以省略
struct Student {
    // 成员列表
    string name;
    int age;
    int score;
};

void defStruct()
{
    // 创建一个变量，struct不能省略
    struct Student s1 = {"Xiaoming", 18, 100};
    // 可以修改值
    s1.score = 80;

    cout << "Name: " << s1.name << endl;

}

// P65 - 结构体数组，其中每一个元素都是结构体
void defStructArray()
{
    // 这里借用了P64里面定义的结构体
    struct Student arr[3] = {
        {"Alice",   18, 100},
        {"Bob",     28, 90},
        {"Charlie", 38, 80}
    };

    // 可以修改值
    arr[2].name = "Dylan";

    // 这样是不可以的，只能改具体属性，不能一次性赋值整个结构体
    // arr[2] = {"Dylan", 48, 60};

    cout << arr[2].name << endl;

}

// P66 - 结构体指针，唯一的区别是属性的连接符号 p->name，而不是s.name
void defStructPointer()
{
    // 这里借用了P64里面定义的结构体
    struct Student s = {"Alice",   18, 100};

    // 常规方式访问属性
    string name1 = s.name;

    // 定义结构体指针
    struct Student * p = &s;

    // 利用指针访问属性
    string name2 = p->name;

    cout << name1 << endl;
    cout << name2 << endl;

}

// P67 - 结构体嵌套
void StructNesting()
{
    // 这里借用了P64里面定义的结构体
    struct Student s1 = {"Alice", 18, 100};
    struct Student s2 = {"Susan", 15, 99};

    // 定义外层结构体 teacher
    struct Teacher {
        string name;
        int id;
        int age;
        struct Student stu1;  // 其中的一个成员是另一个结构体，这里的 struct Student 相当于自定义的数据类型
        struct Student stu2;
    };

    struct Teacher t1 = {"LaoWang", 10000, 50, s1, s2};

    cout << t1.name << "\t" << t1.stu1.name << "\t" << t1.stu2.name << endl;  // 调用内层结构体就多加几个.即可

    // 可以重新赋值
    t1.stu1.score = 200;
    t1.stu2.score = 300;

    cout << t1.stu1.score << "\t" << t1.stu2.score << endl;

}

// P67 - 结构体作为函数参数
// 定义函数，参数是一个结构体，函数打印参数的所有信息
// 函数1：值传递
void PrintAllInfoOfStruct1 (struct Student s)
{
    cout << s.name << endl;
    cout << s.age << endl;
    cout << s.score << endl;

}

// 函数2：地址传递，函数定义时用指针接收参数（形参）
/* 形参用指针，实参用地址 */
void PrintAllInfoOfStruct2 (struct Student * p)
{
    cout << p->name << endl;
    cout << p->age << endl;
    cout << p->score << endl;

}

void StructAsAttribute()
{
    // 这里借用了P64里面定义的结构体
    struct Student s1 = {"Alice", 18, 100};
    struct Student s2 = {"Susan", 15, 99};

    PrintAllInfoOfStruct1(s1);
    PrintAllInfoOfStruct2(&s2);  // 函数调用时传递地址（实参）
}


int main5 () {
    StructAsAttribute ();

    system("pause");  // System: send a DOS command, which requires including stdlib.h
    return 0;
}


