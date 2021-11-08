// p143_file_operation.cpp

#include <iostream>
#include <stdlib.h>
#include <ctime>  // 用于time函数
#include <cmath>  // 用于数学计算
#include <string>

using namespace std;

#include <fstream> // 用于文件操作

// P143 - 文件操作：写文件

// 有两种文件类型，文本文件(ASCII)可以用记事本显示的都是
// 二进制文件，记事本打开会有乱码的

void test_143_00()
{
    // 创建一个文件输出流对象   o-out + f-file + stream
    ofstream ofs;
    // 文件路径 + 打开方式
    ofs.open("test.txt", ios::out);
    
    // 写入文件
    ofs << "测试文件写入，ABCDEFG..." << endl;
    ofs << "测试文件写入，HIJKLMN..." << endl;

    // 关闭文件
    ofs.close();
}

// P144 - 读文件
void test_144_00()
{
    // 创建一个文件输入流对象   i-in + f-file + stream
    ifstream ifs;
    // 文件路径 + 打开方式
    ifs.open("test.txt", ios::in);

    // 判断是否打开
    if (! ifs.is_open())
    {
        cout << "文件打开失败，请检查文件路径" << endl;
        return;
    }
    
    // 读数据，一共有四种方法
    // 方法1：直接用右移运算符，逐行读取
    // char buffer_1[1024] = {0};  // 预设一个足够长的空字符数组
    // while(ifs >> buffer_1)
    // {
    //     cout << buffer_1 << endl;
    // }

    // 方法2：使用ifs内部的getline函数
    // char buffer_2[1024] = {0};  // 预设一个足够长的空字符数组
    // while(ifs.getline(buffer_2, sizeof(buffer_2)))
    // {
    //     cout << buffer_2 << endl;
    // }

    // 方法3：使用全局的getline函数【这个看起来最舒服】
    string buffer_3;
    while(getline(ifs, buffer_3))
    {
        cout << buffer_3 << endl;
    }

    // 方法4：逐个字符读取【不推荐，效率不高】
    // char c;
    // while( (c = ifs.get()) != EOF )
    // {
    //     cout << c;  // 这里不用endl; 因为换行符 \n 本身也是一个char可以被读取
    // }


    // 关闭文件
    ifs.close();
}

// P145 - 写二进制文件

class Person
{
public:
    char m_Name[64];  // 这里可以用string 吗？
    int m_Age;
};

// 用二进制写出来的文件，用记事本打开会有乱码，没关系
// 只要下一个函数 P146 能读取正确的信息就行
void test_145_00()
{
    // 创建一个文件输出流对象   o-out + f-file + stream
    ofstream ofs ("person.txt", ios::out | ios::binary);
    // 文件路径 + 打开方式（注意这里有两个属性）
    // 其实打开方式可以省略，和上面的创建 ofs 写在一起
    // ofs.open("person.txt", ios::out | ios::binary);
    
    // 写二进制文件：需要用 ostream & write() 方法，前面将要写入的信息强转成 const char *格式【读不需要const，写需要const】，后面是长度
    Person p = {"张三", 18};
    ofs.write (((const char *) &p), sizeof(Person));  // (const char *) 表示强制格式转换

    // 关闭文件
    ofs.close();

}

// P146 - 读二进制文件

void test_146_00()
{
    // 创建一个文件输入流对象   i-in + f-file + stream
    ifstream ifs;// ("person.txt", ios::in | ios::binary);
    // 文件路径 + 打开方式 【可以和上一步合并】
    ifs.open("person.txt", ios::in | ios::binary);

    // 读取二进制文件：需要用 istream & read() 方法，前面将读取信息强转成 char *格式【读不需要const，写需要const】，后面是长度
    Person p;  // 提供一个空的类对象，其中内容由读取的文件信息赋值
    ifs.read (((char *) &p), sizeof(Person));  // (char *) 表示强制格式转换

    // 判断是否打开成功
    if (! ifs.is_open())
    {
        cout << "文件打开失败，请检查文件路径" << endl;
        return;
    }

    // 将读取的信息显示出来
    cout << "p.m_Name = " << p.m_Name << "\tp.m_Age = " << p.m_Age << endl;

    // 关闭文件
    ifs.close();
}

/*********************************************************************************************************/



int main_143 () {
    // 是否需要显示中文？
    bool ChineseDisplay = true;
    // bool ChineseDisplay = false;

    if (ChineseDisplay) system("chcp 936");  // to set CMD active code page for Chinese display (the default code page is "chcp 437")
    system("cls");

    test_146_00 ();
    
    system("pause");  // System: send a DOS command, which requires including stdlib.h
    return 0;
}


