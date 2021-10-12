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


int main () {
    defStructPointer ();

    system("pause");  // System: send a DOS command, which requires including stdlib.h
    return 0;
}


